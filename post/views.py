from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Tweet, Comment, LikeTweet, DisLikeTweet
from .serializers import TweetSerializer, CommentSerializer
from .permissions import IsAuthorPermission
from .paginations import StandartPagination


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication,  ]
    permission_classes = [IsAuthorPermission, ]
    pagination_class = StandartPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#     authentication_classes = [SessionAuthentication, TokenAuthentication,  ]
#     permission_classes = [IsAuthorPermission, ]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return self.queryset.filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            tweet=get_object_or_404(Tweet, id=self.kwargs['tweet_id'])
        )

class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]


class PostTweetLike(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        try:
            like = LikeTweet.objects.create(tweet=tweet, user=request.user)
        except IntegrityError:
            data = {'error': f'tweet {tweet_id} already liked by {request.user.username}'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            data = {'message' : f'tweet {tweet_id} liked by {request.user.username}'}
            return Response(data, status=status.HTTP_201_CREATED)


class PostTweetDisLike(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        try:
            dislike = DisLikeTweet.objects.create(tweet=tweet, user=request.user)
        except IntegrityError:
            DisLikeTweet.objects.get(tweet=tweet, user=request.user).delete()
            data = {
                'message': f'{request.user.username} already dislike from tweet {tweet_id} '
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': f'tweet {tweet_id} disliked from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)










from rest_framework import serializers

from .models import Tweet, Comment


class TweetSerializer(serializers.ModelSerializer):
    post_username = serializers.ReadOnlyField()
    get_likes = serializers.ReadOnlyField()
    get_dislikes = serializers.ReadOnlyField()

    class Meta:
        model = Tweet
        fields = "__all__"
        read_only_fields = ['user',]

class CommentSerializer(serializers.ModelSerializer):
    post_username = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['user', 'tweet']
from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .models import User
from .serialisers import RegisterSerilaliser

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerilaliser


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

import jwt
import datetime, time

from django.conf import settings
from .models import User
from .serializers import UserSerializer, RetrieveUserSerializer

# Create your views here.
class RegisterUserApi(APIView):
  def post(self, request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user:
      raise exceptions.AuthenticationFailed("Usuário já existe")

    User.objects.create_user(name=name, email=email, password=password)
    return Response(status=status.HTTP_201_CREATED)

class LoginApi(APIView):
  def createToken(self, user): 
    payload = dict(
      id=user.id,
      exp=time.mktime((datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timetuple()) * 1000,
      iat=datetime.datetime.utcnow(),
      isStaff=user.is_staff
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token

  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = authenticate(request, email=email, password=password)
                 
    if user is None:
      raise exceptions.AuthenticationFailed("Credenciais Incorretas")
    
    token = self.createToken(user=user)

    login(request, user)

    return Response(status=status.HTTP_200_OK, data={'jwt': token})

class RetrieveUserApi(APIView):
  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    tokenDecoded = jwt.decode(token, settings.JWT_SECRET,  algorithms="HS256")
    
    user = User.objects.filter(id=tokenDecoded['id']).first()

    serializer = RetrieveUserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutApi(APIView):
  def post(self, request):
    logout(request)

    return Response(status=status.HTTP_200_OK)
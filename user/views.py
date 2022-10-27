from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions

import jwt
import datetime

from django.conf import settings
from .models import User
from .serializers import UserSerializer
from .authentication import CustomUserAuthentication

# Create your views here.
class RegisterUserApi(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)

class LoginApi(APIView):
  def createToken(self, userId: int): 
    payload = dict(
      id=userId,
      exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
      iat=datetime.datetime.utcnow()
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token

  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
      raise exceptions.AuthenticationFailed("Invalid Credentials")
    
    if not user.check_password(raw_password=password):
      raise exceptions.AuthenticationFailed("Unautorized")

    token = self.createToken(userId=user.id) 

    resp = Response(status=status.HTTP_200_OK)

    resp.set_cookie("jwt", token, httponly=True)

    return resp

class RetrieveUserApi(APIView):
  authentication_classes = (CustomUserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request):
    user = request.user
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutApi(APIView):
  authentication_classes = (CustomUserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):
    resp = Response()
    resp.delete_cookie("jwt")
    resp.data = {"message": "loged out successfully"}

    return resp
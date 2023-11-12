from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings


from .utils import createToken, getUserFromToken, createRefresh, getUserFromRefresh, isTokenValid
from .models import User
from .serializers import UserSerializer, RetrieveUserSerializer


class GoogleSignIn(APIView):
  def post(self, request):
    try:
      token = request.data['idToken']
      idInfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
      user = User.objects.filter(email=idInfo['email']).first()
      if not user:
        try:
          user = User.objects.create_user(name=idInfo['name'], email=idInfo['email'])
        except:
          raise exceptions.AuthenticationFailed("Email em uso") 
      
      jwtToken = createToken(user=user)
      refreshToken = createRefresh(user=user)

      return Response(status=status.HTTP_200_OK, data={'access_token': jwtToken, 'refresh_token': refreshToken, 'is_staff': user.is_staff})
    except ValueError:
      raise exceptions.AuthenticationFailed("Token inválido")

class RegisterUserApi(APIView):
  def post(self, request):
    email = request.data['email']
    user = User.objects.filter(email=email).first()

    if user:
      raise exceptions.AuthenticationFailed("Email em uso")

    serializser = UserSerializer(data=request.data)

    if serializser.is_valid():
      user = User.objects.create_user(
        name=serializser.data['name'],
        email=serializser.data['email'],
        password=serializser.data['password']
      )
      user.lattes = serializser.data['lattes']
      user.googleScholar = serializser.data['googleScholar']
      user.researchGate = serializser.data['researchGate']
      user.orcid = serializser.data['orcid']
      user.github = serializser.data['github']
      user.category = serializser.data['category']
      user.oia = bool(serializser.data['oia'])

      user.save()
    else:
      raise exceptions.APIException('Dados inválidos')

    return Response(status=status.HTTP_201_CREATED)

class LoginApi(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, email=email, password=password)
                 
    if user is None:
      raise exceptions.AuthenticationFailed("Credenciais Incorretas")
    
    jwtToken = createToken(user=user)
    refreshToken = createRefresh(user=user)
    login(request, user)

    return Response(status=status.HTTP_200_OK, data={'access_token': jwtToken, 'refresh_token': refreshToken, 'is_staff': user.is_staff})

class RetrieveUserApi(APIView):
  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']  
    if not isTokenValid(token):
      return Response({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

    user = getUserFromToken(token)

    if not user:
      raise exceptions.AuthenticationFailed("Usuário não autenticado")

    serializer = RetrieveUserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

class RefresUserApi(APIView):
  def post(self, request):
    token = request.data['refresh_token']
    user = getUserFromRefresh(token)
    if user:
      token = createToken(user)
      return Response(status=status.HTTP_200_OK, data={'access_token': token})
    raise exceptions.AuthenticationFailed("Não autorizado")

class LogoutApi(APIView):
  def post(self, request):
    logout(request)

    return Response(status=status.HTTP_200_OK)
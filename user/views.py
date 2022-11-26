from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate



from .utils import createToken, getUserFromToken
from .models import User
from .serializers import UserSerializer, RetrieveUserSerializer

# Create your views here.
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
    
    token = createToken(user=user)

    login(request, user)

    return Response(status=status.HTTP_200_OK, data={'jwt': token})

class RetrieveUserApi(APIView):
  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")

    serializer = RetrieveUserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutApi(APIView):
  def post(self, request):
    logout(request)

    return Response(status=status.HTTP_200_OK)
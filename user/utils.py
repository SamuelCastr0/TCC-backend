import jwt
import datetime, time
from django.conf import settings
from .models import User
from rest_framework.response import Response
from rest_framework import status


def createToken(user): 
    payload = dict(
        id=user.id,
        exp=time.mktime((datetime.datetime.now() + datetime.timedelta(hours=24)).timetuple()) * 1000,
        iat=datetime.datetime.now(),
        isStaff=user.is_staff
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token

def createRefresh(user):
    payload = dict(
        id=user.id,
        exp=time.mktime((datetime.datetime.now() + datetime.timedelta(days=365)).timetuple()) * 1000,
        iat=datetime.datetime.now(),
        isStaff=user.is_staff
    )
    token = jwt.encode(payload, settings.REFRESH_SECRET, algorithm="HS256")

    return token

def getUserFromToken(token):
    tokenDecoded = jwt.decode(token, settings.JWT_SECRET,  algorithms="HS256")
    user = User.objects.filter(id=tokenDecoded['id']).first()

    if user:
        return user
    return None

def getUserFromRefresh(token):
    tokenDecoded = jwt.decode(token, settings.REFRESH_SECRET,  algorithms="HS256")
    user = User.objects.filter(id=tokenDecoded['id']).first()

    if user:
        return user
    return None

def isTokenExpired(token):
    tokenDecoded = jwt.decode(token, settings.JWT_SECRET,  algorithms="HS256")
    expTime = tokenDecoded['exp']
    expDate = datetime.datetime.fromtimestamp(expTime/1000.0)
    currentDate = datetime.datetime.now()

    if expDate < currentDate:
        return True
    return False

def validateAndRetrieveUser(token):
  if isTokenExpired(token):
    return None

  user = getUserFromToken(token)

  if not user:
    return None
  
  return user

def validateStaffUser(token):
  user = validateAndRetrieveUser(token)
  
  if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'Token inválido'})

  if not user.is_staff:
    return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'Usuário não tem permissão'})
  
  return None

def validateSuperUser(token):
  user = validateAndRetrieveUser(token)
  
  if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'Token inválido'})

  if not user.is_superuser:
    return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'Usuário não tem permissão'})
  
  return None
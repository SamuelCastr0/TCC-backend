import math
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions

from user.utils import getUserFromToken

from .models import LearningObject
from .serializers import CreateLearningObjectSerializer, LearningObjectSerializer


class LearningObjectAPI(APIView):
  def filterObjects(self, objects, filter):
    if filter == 'published':
      objects = objects.filter(isPublished=True)
    if filter == 'not-published':
      objects = objects.filter(isPublished=False)
    return objects

  def getLearningObjects(self):
    filter = self.request.GET.get('filter')
    search = self.request.GET.get('search')
    learningObjects = []

    if search: 
      learningObjects = LearningObject.objects.filter(Q(name__icontains=search)).values()
    else: 
      learningObjects = LearningObject.objects.all()
    
    filteredObjects = self.filterObjects(learningObjects, filter)

    return filteredObjects

  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")
    
    if not user.is_staff:
      raise exceptions.NotAuthenticated("Usuário não tem permissão")

    page = 1 if self.request.GET.get('search') else int(self.request.GET.get('page', 1))
    pageSize = int(self.request.GET.get('page_size', 8))

    learningObjects = self.getLearningObjects()

    # pagination
    count = learningObjects.count()
    start = (page - 1) * pageSize
    end = page * pageSize

    serializer = LearningObjectSerializer(learningObjects[start:end], many=True)

    return Response({
      'results': serializer.data,
      'count': count,
      'page': page,
      'page_count': math.ceil(count/pageSize)
      }, 
      status=status.HTTP_200_OK)
  
  def post(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")
    
    if not user.is_staff:
      raise exceptions.NotAuthenticated("Usuário não tem permissão")

    serializer = CreateLearningObjectSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()

    return Response(status=status.HTTP_201_CREATED)
  
  def put(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")
    
    if not user.is_superuser:
      raise exceptions.NotAuthenticated("Usuário não tem permissão")

    learningObject = LearningObject.objects.get(id=int(id))
    serializer = LearningObjectSerializer(instance=learningObject, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(status=status.HTTP_200_OK)

  def delete(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")
    
    if not user.is_superuser:
      raise exceptions.NotAuthenticated("Usuário não tem permissão")

    learningObject = LearningObject.objects.get(id=id)
    learningObject.delete()

    return Response(status=status.HTTP_200_OK)

class PublishLearningObject(APIView):
  def put(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token)

    if not user:
      raise exceptions.NotAuthenticated("Usuário não autenticado")
    
    if not user.is_superuser:
      raise exceptions.NotAuthenticated("Usuário não tem permissão")
    
    learningObject = LearningObject.objects.get(id=int(id))
    learningObject.isPublished = not learningObject.isPublished
    learningObject.save()

    return Response(status=status.HTTP_200_OK)
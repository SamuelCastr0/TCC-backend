import math
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.utils import validateStaffUser, validateSuperUser
from .models import LearningObject
from .serializers import CreateLearningObjectSerializer, LearningObjectSerializer

def paginateObjects(objects, request, Serializer):
  page = int(request.GET.get('page', 1))
  pageSize = int(request.GET.get('page_size', 8))

  count = objects.count()
  start = (page - 1) * pageSize
  end = page * pageSize

  serializer = Serializer(objects[start:end], many=True)

  return Response({
      'results': serializer.data,
      'count': count,
      'page': page,
      'page_count': math.ceil(count/pageSize)
    }, 
    status=status.HTTP_200_OK)

class LearningObjectAPI(APIView):
  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateStaffUser(token)

    if validationResponse:
      return validationResponse

    learningObjects = self.getLearningObjects()
    paginatedResponse = paginateObjects(learningObjects, request, LearningObjectSerializer)
    
    return paginatedResponse
  
  def post(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateStaffUser(token)

    if validationResponse:
      return validationResponse

    serializer = CreateLearningObjectSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()

    return Response(status=status.HTTP_201_CREATED)
  
  def put(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateSuperUser(token)

    if validationResponse:
      return validationResponse

    learningObject = LearningObject.objects.get(id=int(id))
    serializer = LearningObjectSerializer(instance=learningObject, data=request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(status=status.HTTP_200_OK)

  def delete(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateSuperUser(token)

    if validationResponse:
      return validationResponse

    learningObject = LearningObject.objects.get(id=id)
    learningObject.delete()

    return Response(status=status.HTTP_200_OK)

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

class PublishLearningObjectAPI(APIView):
  def put(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateSuperUser(token)

    if validationResponse:
      return validationResponse
    
    learningObject = LearningObject.objects.get(id=int(id))
    learningObject.isPublished = not learningObject.isPublished
    learningObject.save()

    return Response(status=status.HTTP_200_OK)

class SearchObjectsAPI(APIView):
  def get(self, request):
    search = request.GET.get('search')
    learningObjects = LearningObject.objects.filter(Q(name__icontains=search) & Q(isPublished=True))
    paginatedResponse = paginateObjects(learningObjects, request, LearningObjectSerializer)
    print(paginatedResponse.data)

    return paginatedResponse
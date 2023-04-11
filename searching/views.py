import math
from django.db.models import Q
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.utils import validateStaffUser, validateSuperUser, getUserFromToken
from .models import LearningObject, Course, CourseLearningObject
from .serializers import CreateLearningObjectSerializer, LearningObjectSerializer, CourseSerializer, CourseLearningObjectSerializer

def paginate(objects, request, Serializer):
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
    paginatedResponse = paginate(learningObjects, request, LearningObjectSerializer)
    
    return paginatedResponse
  
  def post(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateStaffUser(token)

    if validationResponse:
      return validationResponse

    serializer = CreateLearningObjectSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(createdBy=getUserFromToken(token))

    return Response(status=status.HTTP_201_CREATED)
  
  def put(self, request, id):
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateSuperUser(token)

    if validationResponse:
      return validationResponse

    learningObject = LearningObject.objects.get(id=int(id))
    serializer = LearningObjectSerializer(instance=learningObject, data=request.data)
    
    if serializer.is_valid():
        serializer.save(editedBy=getUserFromToken(token))

    return Response(status=status.HTTP_200_OK)

  def delete(self, request, id):
    print(request.META['HTTP_AUTHORIZATION'])
    token = request.META['HTTP_AUTHORIZATION']
    validationResponse = validateSuperUser(token)
    print('ola')

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
    paginatedResponse = paginate(learningObjects, request, LearningObjectSerializer)

    return paginatedResponse

class CourseAPI(APIView):
  def get(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token).id
    search = self.request.GET.get('search')
    courses = []

    if search: 
      courses = Course.objects.filter(Q(name__icontains=search, user=user))
    else: 
      courses = Course.objects.filter(user=user)
    
    paginatedResponse = paginate(courses, request, CourseSerializer)

    return paginatedResponse

  def post(self, request):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token).id
    with transaction.atomic():
      course = Course.objects.create(name=request.data['name'], user_id=user)
      index = 0
      for object in request.data['objects']:
        CourseLearningObject.objects.create(course_id=course.id, learningObject_id=object['id'], index=index)
        index += 1

      return Response(status=status.HTTP_200_OK)
  
  def patch(self, request, course):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token).id
    course = Course.objects.filter(id=course, user=user).first()
    
    serializer = CourseSerializer(instance=course, data=request.data, partial=True)

    if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


  def delete(self, request, course):
    token = request.META['HTTP_AUTHORIZATION']
    user = getUserFromToken(token).id
    course = Course.objects.filter(id=course, user=user).first()
    course.delete()

    return Response(status=status.HTTP_200_OK)


class ObjectsFromCoursesAPI(APIView):
  def get(self, request, course):
    relationships = CourseLearningObject.objects.filter(course=course)
    objects = []
    for relationship in relationships:
      objects.append(relationship.learningObject)
    serializer = LearningObjectSerializer(objects, many=True)

    return Response(serializer.data , status=200)

class CouseLearningObjectsAPI(APIView):
  def get(self, request, course):
    relationships = CourseLearningObject.objects.filter(course=course)
    serializer = CourseLearningObjectSerializer(instance=relationships, many=True)

    return Response(status=status.HTTP_200_OK, data=serializer.data)

class ToogleObjectInCouseAPI(APIView):
  def post(self, request):
    course = request.data['course']
    learningObject = request.data['object']
    relationship = CourseLearningObject.objects.filter(course=course, learningObject=learningObject).first()
    relationship.isCompleted = not relationship.isCompleted
    relationship.save()

    return Response(status=status.HTTP_200_OK)
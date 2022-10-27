import math
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LearningObject
from .serializers import LearningObjectSerializer


class LearningObjectAPI(APIView):
  def getLearningObjects(self):
    search = self.request.GET.get('search')
    if search: 
      return LearningObject.objects.filter(Q(name__icontains=search)).values()

    return LearningObject.objects.all()

  def get(self, request):
      page = int(self.request.GET.get('page', 1))
      pageSize = int(self.request.GET.get('page_size', 8))
      id = self.request.GET.get('id')
      if id:
        learningObject = LearningObject.objects.get(id=int(id))
        serializer = LearningObjectSerializer(learningObject, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
    serializer = LearningObjectSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()

    return Response(status=status.HTTP_201_CREATED)
  
  def put(self, request):
    id = self.request.GET.get('id')
    learningObject = LearningObject.objects.get(id=int(id))
    serializer = LearningObjectSerializer(instance=learningObject, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(status=status.HTTP_200_OK)

  def delete(self, request):
    id = request.GET.get('id')
    learningObject = LearningObject.objects.get(id=id)
    learningObject.delete()

    return Response(status=status.HTTP_200_OK)

  
from rest_framework import serializers
from .models import LearningObject, Course

class LearningObjectSerializer(serializers.ModelSerializer):
  class Meta:
    read_only_fields = ('id',)
    model = LearningObject
    fields = '__all__'

class CreateLearningObjectSerializer(serializers.ModelSerializer):
  class Meta:
    read_only_fields = ('id',)
    model = LearningObject
    exclude = ('isPublished', )

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = '__all__'


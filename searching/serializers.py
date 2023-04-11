from rest_framework import serializers
from .models import LearningObject, Course, CourseLearningObject

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
  progression = serializers.SerializerMethodField()

  class Meta:
    model = Course
    fields = '__all__'

  def get_progression(self, course):
    relationships = CourseLearningObject.objects.filter(course=course)
    completedCoursesCont = 0
    for relatinship in relationships:
      if relatinship.isCompleted:
        completedCoursesCont += 1
    
    return completedCoursesCont / len(relationships)


class CourseLearningObjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = CourseLearningObject
    fields = ['learningObject', 'isCompleted']

from rest_framework import serializers
from .models import LearningObject

class LearningObjectSerializer(serializers.ModelSerializer):
  class Meta:
    read_only_fields = ('id',)
    model = LearningObject
    fields = '__all__'
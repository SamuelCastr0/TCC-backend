from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    read_only_fields = ('is_active', 'is_staff', 'is_admin', 'id')
    fields = '__all__'
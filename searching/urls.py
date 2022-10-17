from django.urls import path

from . import views

urlpatterns = [
  path('learning-objects', views.LearningObjectAPI.as_view(), name='learning-objects')
]
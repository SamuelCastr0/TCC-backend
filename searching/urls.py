from django.urls import path

from . import views

urlpatterns = [
  path('learning-objects/', views.LearningObjectAPI.as_view(), name='learning-objects'),
  path('learning-objects/<int:id>/', views.LearningObjectAPI.as_view(), name='learning-objects'),
  path('toggle-publish/<int:id>/', views.PublishLearningObject.as_view(), name='toggle-publish'),
]
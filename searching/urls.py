from django.urls import path

from . import views

urlpatterns = [
  path('learning-objects/', views.LearningObjectAPI.as_view(), name='learning-objects'),
  path('learning-objects/<int:id>/', views.LearningObjectAPI.as_view(), name='learning-objects'),
  path('toggle-publish/<int:id>/', views.PublishLearningObjectAPI.as_view(), name='toggle-publish'),
  path('search-objects/', views.SearchObjectsAPI.as_view(), name='published-objects'),
  path('course/', views.CourseAPI.as_view(), name='couse'),
  path('course/<int:course>/', views.CourseAPI.as_view(), name='couse'),
  path('course-objects/<int:course>/', views.ObjectsFromCoursesAPI.as_view(), name='couse-objects'),
  path('course-objects-progression/<int:course>/', views.CouseLearningObjectsAPI.as_view(), name='couse-object-relation'),
  path('course-toogle-object/', views.ToogleObjectInCouseAPI.as_view(), name='couse-toogle-object'),
]
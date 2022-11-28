from django.urls import path

from . import views

urlpatterns = [
  path('create/', views.RegisterUserApi.as_view(), name='register'),
  path('login/', views.LoginApi.as_view(), name='login'),
  path('login/google/', views.GoogleSignIn.as_view(), name='google-login'),
  path('me/', views.RetrieveUserApi.as_view(), name='me'),
  path('logout/', views.LogoutApi.as_view(), name='logout')
]
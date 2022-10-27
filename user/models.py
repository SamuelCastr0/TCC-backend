from django.db import models
from django.contrib.auth import models as authModels


class UserManeger(authModels.BaseUserManager):
  def create_user(self, name: str, email: str, password: str = None, is_staff=False, is_superuser=False) -> "User":
    if not email:
      raise ValueError("User must have an email")
    if not name:
      raise ValueError("User must have an name")
    
    user = self.model(email=self.normalize_email(email))
    user.name = name
    user.set_password(password)
    user.is_Active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
  
  def create_user(self, name: str, email: str, password: str = None, is_staff=False, is_superuser=False) -> "User":
    if not email:
      raise ValueError("User must have an email")
    if not name:
      raise ValueError("User must have an name")
    
    user = self.model(email=self.normalize_email(email))
    user.name = name
    user.set_password(password)
    user.is_Active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()

    return user

  def create_superuser(self, name: str, email: str, password: str = None) -> "User":
    user = self.create_user(
      name=name,
      email=email,
      password=password,
      is_staff=True,
      is_superuser=True
    )
    user.save()

    return user

class User(authModels.AbstractUser):
  id = models.BigAutoField(primary_key=True)
  name = models.CharField(verbose_name="Name", max_length=150)
  email = models.EmailField(verbose_name="Email", max_length=150, unique=True)
  password = models.CharField(max_length=150)

  first_name = None
  last_name = None
  username = None

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['name']

  objects = UserManeger()
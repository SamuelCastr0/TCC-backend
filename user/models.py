from django.db import models
from django.contrib.auth import models as authModels


class UserManeger(authModels.BaseUserManager):
    def create_user(
        self,
        name: str,
        email: str,
        password: str = None,
        is_staff=False,
        is_superuser=False
    ) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not name:
            raise ValueError("User must have an name")

        user = self.model(email=self.normalize_email(email))
        user.name = name
        if password:
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
    CATEGORY_CHOICES = [
        ('GRADUATE', 'Graduate Student'),
        ('MASTERING', 'Mastering Student'),
        ('PHD', 'PHD Student'),
        ('PROFESSOR', 'Professor'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True, default=None)
    lattes = models.URLField(max_length=100, null=True, blank=True)
    googleScholar = models.URLField(max_length=100, null=True, blank=True)
    researchGate = models.URLField(max_length=100, null=True, blank=True)
    orcid = models.URLField(max_length=100, null=True, blank=True)
    github = models.URLField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, default='GRADUATE', max_length=50, blank=True)
    oia = models.BooleanField(default=False, blank=True)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    objects = UserManeger()

from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import User

# Register your models here.
admin.site.register(get_user_model())
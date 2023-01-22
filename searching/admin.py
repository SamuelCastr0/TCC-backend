from django.contrib import admin

from .models import LearningObject,Course, CourseLearningObject

# Register your models here.
admin.site.register(LearningObject)
admin.site.register(CourseLearningObject)
admin.site.register(Course)
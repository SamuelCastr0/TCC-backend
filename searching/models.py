from django.db import models
from user.models import User

class LanguageTypes:
  ENGLISH = 'ENGLISH'
  PORTUGUESE = 'PORTUGUESE'

  choices = [
    (ENGLISH, 'english'),
    (PORTUGUESE, 'portuguese')
  ]

class LearningObject(models.Model):
  id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=5000)
  keywords = models.CharField(max_length=100)
  link = models.CharField(max_length=500)
  durationMin = models.IntegerField(null=True, default=None)
  language = models.CharField(choices=LanguageTypes.choices, max_length=10)
  isPublished = models.BooleanField(default=False)
  createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='createdBy')
  editedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='editedBy')

  def __str__(self) -> str:
    return self.title

  class Meta:
    ordering = ['title']

class Course(models.Model):
  id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=30)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courseUser')
  createdAt = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['createdAt']

  def __str__(self):
    return self.name

class CourseLearningObject(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  learningObject = models.ForeignKey(LearningObject, on_delete=models.CASCADE)
  index = models.IntegerField()
  isCompleted = models.BooleanField(default=False)

  class Meta:
    ordering = ['index']

  def __str__(self):
    return self.course.name + '-' + self.learningObject.name
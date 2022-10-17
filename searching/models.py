from django.db import models


class LearningObject(models.Model):
  id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=30)

  def __str__(self) -> str:
    return self.name

  class Meta:
    ordering = ['name']

import uuid
from django.db import models

# Create your models here.
class Activity(models.Model):
  context = models.CharField(max_length=50)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  creator = models.CharField(max_length=20)
  email = models.CharField(max_length=20)
  expire_on = models.DateField()
  def __str__(self):
    return self.context

class Choice(models.Model):
  activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name
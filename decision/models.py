import uuid
from django.db import models
import random

# function
def __generate_token__():
  l = '1234567890qwertyuiopasdfghjklzxcvbnm'
  token = ""
  for i in range(8):
    x = random.randint(0, len(l) - 1)
    token += l[x]
  return token

# Create your models here.
class Activity(models.Model):
  context = models.CharField(max_length=50)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  creator = models.CharField(max_length=20)
  email = models.CharField(max_length=20)
  admin_token = models.TextField(default=__generate_token__())
  description = models.TextField(default='Do you think this is a greate idea?')
  expire_on = models.DateField()
  def __str__(self):
    return self.context


class Choice(models.Model):
  activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
  name = models.CharField(max_length=100, unique=True)
  votes_count = models.IntegerField(default=0)
  def __str__(self):
    return self.name
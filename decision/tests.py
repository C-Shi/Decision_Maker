import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Activity, Choice

def create_fake_activity(context):
    creator = 'admin'
    email = 'admin@admin.com'
    description = 'this is a basic test'
    expire_on = timezone.now() + datetime.timedelta(days=7)
    return Activity(context=context, creator=creator, email=email, description=description, expire_on=expire_on)

# Create your tests here.
class ActivityModelTests(TestCase):
  def test_create_activity(self):
    context = 'create activity'
    activity = create_fake_activity(context)
    activity.save()
    self.assertEqual(activity, Activity.objects.get(context=context))
  
  def test_unique_id_auto_generate(self):
    context = 'check uuid';
    new_activity = create_fake_activity(context)
    new_activity.save()
    activity = Activity.objects.get(context=context);
    self.assertTrue(activity.id)

class ChoiceModelTests(TestCase):
  def choice_create_on_activity(self):
    context = 'choice create activity'
    activity = create_fake_activity(context);
    activity.save()
    activity.choice_set.create(name="This is choice 1")
    choice_list = activity.choice_set.all()
    print('hello')
    self.assertTrue(choice_list)


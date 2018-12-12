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

def create_fake_choice(activity):
  activity.choice_set.create(name="This is choice 1")
  return activity.choice_set.all()
  

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
  # test name should start with test
  def test_choice_create_on_activity(self):
    context = 'choice create activity'
    activity = create_fake_activity(context);
    activity.save()
    choice_list = create_fake_choice(activity)
    self.assertTrue(choice_list)
  
  def test_choice_default_vote(self):
    context = 'choice default vote'
    activity = create_fake_activity(context);
    activity.save()
    choice_list = create_fake_choice(activity)
    for choice in choice_list:
      self.assertEqual(choice.votes_count, 0)


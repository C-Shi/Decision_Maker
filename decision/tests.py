import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

class IndexViewTests(TestCase):
  def test_get_index_page(self):
    response = self.client.get(reverse('decision:index'))
    self.assertEqual(response.status_code, 200)

class NewRouteTest(TestCase):
  def test_new_page(self):
    response = self.client.get(reverse('decision:new'))
    self.assertEqual(response.status_code, 200)
  
  def test_new_page_elements(self):
    response = self.client.get(reverse('decision:new'))
    self.assertContains(response, 'Activity')
    self.assertContains(response, 'Your Name')
    self.assertContains(response, 'Email')
    self.assertContains(response, 'Description')
  
  def test_create_new_activity_redirect(self):
    response = self.client.post(reverse('decision:create'), data={'context': 'Hello World', 'creator': 'admin', 'email':'admin@home.com', 'description': 'description'})
    self.assertEqual(response.status_code, 302)



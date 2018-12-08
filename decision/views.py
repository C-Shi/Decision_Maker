from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Activity


# Create your views here.

# RESTFUL index page
def index(request):
  return render(request, 'decision/index.html')

# RESTFUL get NEW form page
def new(request):
  return render(request, 'decision/new.html')

# RESTFUL post Create page
def create(request):
  # collect information from /new form
  context = request.POST['context']
  creator = request.POST['creator']
  email = request.POST['email']
  description = request.POST['description']

  # take all existing options and put into a list
  options_list = request.POST.getlist('option')

  # auto-set the expire day of this activity to 7 days from now unless specified
  expire_on = timezone.now() + datetime.timedelta(days=7)

  # save posted data into Activity Model
  new_activity = Activity(context=context, creator=creator, email=email, description=description, expire_on=expire_on)
  new_activity.save()

  # add choice to newly created activity
  for i in range(len(options_list)):
    option = options_list[i]
    new_activity.choice_set.create(name=option)

  return HttpResponseRedirect('/')

# RESTFUL show route for individual decision
# this app does not have route for seeing all activity
# only accessible with known token
def show(request, activity_id):
  activity = Activity.objects.get(pk=activity_id)
  choice_list = activity.choice_set.all()
  return render(request, 'decision/show.html', {'activity': activity, 'choice_list': choice_list})

def vote(request, activity_id):
  activity = Activity.objects.get(pk=activity_id)
  choice_list = activity.choice_set.all()
  print(request.POST['choice'])
  try:
    selected_choice = activity.choice_set.all()
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'decision/show.html', {'activity': activity, 'choice_list': choice_list, 'error_message': 'You did not select anything'})
  else:
    return HttpResponseRedirect(reverse('decision:success', args=(activity.id,)))

def success(request, activity_id):
  activity = Activity.objects.get(pk=activity_id)
  choice_list = activity.choice_set.all()
  return render(request, 'decision/success.html')

# RESTFUL post route to delete
def delete(request, decision):
  pass
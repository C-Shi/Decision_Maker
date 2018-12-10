from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
import json
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

# this route handles anything happens after user votes for an options
def vote(request, activity_id):
  activity = Activity.objects.get(pk=activity_id)
  choice_list = activity.choice_set.all()
  print(request.POST['choice'])
  try:
    selected_choice = activity.choice_set.get(name=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'decision/show.html', {'activity': activity, 'choice_list': choice_list, 'error_message': 'You did not select anything'})
  else:
    selected_choice.votes_count += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('decision:success', args=(activity.id,)))

def success(request, activity_id):
  activity = Activity.objects.get(pk=activity_id)
  choice_list = list(activity.choice_set.all().values('name', 'votes_count'))

  return render(request, 'decision/success.html', {'choice_list': choice_list, 'activity': activity })

# RESFUL get page of admin
def admin(request, admin_token):
  activity = get_object_or_404(Activity, admin_token=admin_token)
  choice_list = list(activity.choice_set.all().values('name', 'votes_count'))
  print(activity.context)
  if request.GET['email'] == activity.email:
    return render(request, 'decision/admin.html', {'activity': activity, 'choice_list': choice_list})
  else:
    return HttpResponse('Denied! You do not have access')

# RESFUL update route
def update(request, activity_id):
  activity = get_object_or_404(Activity, pk=activity_id)

  old_choice_list = activity.choice_set.all()
  new_choice_list = request.POST.getlist('option')

  # remove old choice if it does not exist in updatelist anymore - also remove all related votes
  for old_choice in old_choice_list:
    try:
      print(new_choice_list.index(old_choice.name))
    except:
      old_choice.delete()
    else:
      pass

  # add new choice if it does not exist
  for new_choice in new_choice_list:
    try:
      choice = activity.choice_set.get(name=new_choice)
    except:
      # add this choice only if it does not equals to nothing
      if new_choice != '':
        activity.choice_set.create(name=new_choice)
    else:
      pass
  
  # remove choice that does not need anymore
  return HttpResponse('update')


# RESTFUL post route to delete
def delete(request, decision):
  pass
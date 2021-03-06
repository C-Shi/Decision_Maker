from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
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

  message = {
    'title': 'You have create an activity',
    'content': 'The secret link has been sent to you through email. You will be able to forward link to whoever needs to know. Voting session will be closed on expired date'
  }

  # this only send a fake email
  send_mail(
      'Subject here',
      f'You have created an activity {new_activity.context}, your admin token is {new_activity.admin_token}, your voting linke is: localhost:8000/show/{new_activity.id} ',
      'from@example.com',
      ['to@example.com'],
      fail_silently=True,
  )

  return render(request, 'decision/info.html', {'message': message})

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

  success_message = f'Thank you for voting. The final results will be released on {activity.expire_on}'
  return render(request, 'decision/success.html', {'choice_list': choice_list, 'activity': activity, 'message': success_message})

# RESFUL get page of admin
def admin(request, admin_token):
  activity = get_object_or_404(Activity, admin_token=admin_token)
  choice_list = list(activity.choice_set.all().values('name', 'votes_count'))
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
      new_choice_list.index(old_choice.name)
    except:
      old_choice.delete()


  # add new choice if it does not exist
  for new_choice in new_choice_list:
    try:
      # if found then this activity will not be added
      choice = activity.choice_set.get(name=new_choice)
    except:
      # add this choice only if it does not equals to nothing
      if new_choice != '':
        activity.choice_set.create(name=new_choice)

  
  choice_list = activity.choice_set.all()
  
  success_message = 'You have updated your activity. Thank You !'

  # this only send a fake email
  send_mail(
      'Subject here',
      'Thanks ! Your activity has been updated!',
      'from@example.com',
      ['to@example.com'],
      fail_silently=True,
  )
  # remove choice that does not need anymore
  return render(request, 'decision/success.html', {'activity': activity, 'choice_list': choice_list, 'message': success_message})


# RESTFUL post route to delete
def delete(request, activity_id):
  activity = get_object_or_404(Activity, pk=activity_id)
  activity_context = activity.context
  activity.delete()

  send_mail(
      'Subject here',
      f'Your activity \'{activity_context}\' has been deleted. All associated votes has been remoted as well',
      'from@example.com',
      ['to@example.com'],
      fail_silently=True,
  )

  message = {
    'title': 'You have delete an activity',
    'content': 'You have just deleted an activity. All related votes has been removed as well'
  }
  return render(request, 'decision/info.html', {'message': message})


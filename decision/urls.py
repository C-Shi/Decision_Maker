from django.urls import path
from . import views

app_name = 'decision'
urlpatterns = [
  path('', views.index, name='index')
]
from django.urls import path
from . import views

app_name = 'decision'
urlpatterns = [
  path('', views.index, name='index'),
  path('new/', views.new, name='new'),
  path('create/', views.create, name='create'),
  path('show/<str:activity_id>', views.show, name='show'),
  path('vote/<str:activity_id>', views.vote, name='vote'),
  path('success/<str:activity_id>', views.success, name="success"),
  path('admin/<str:admin_token>', views.admin, name='admin'),
  path('update/<str:activity_id>', views.update, name='update'),
  path('delete/<str:activity_id>', views.delete, name='delete')
]
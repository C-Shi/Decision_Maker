from django.contrib import admin

from .models import Activity, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


class ActivityAdmin(admin.ModelAdmin):
  list_display= ('context', 'creator', 'email', 'id')
  inlines = [ChoiceInline]



admin.site.register(Activity, ActivityAdmin)
from django.shortcuts import render

# Create your views here.

# RESTFUL index page
def index(request):
  return render(request, 'decision/index.html')

# RESTFUL get NEW form page
def new(request):
  return render(request, 'decision/new.html')

# RESTFUL post Create page
def create(request):
  pass

# RESTFUL show route for individual decision
def show(request, decision_id):
  pass

# RESTFUL post route to delete
def delete(request, decision):
  pass
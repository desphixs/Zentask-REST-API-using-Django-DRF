# We import the path tool from Django's URL library.
from django.urls import path

# We import our new TaskListView from our views.py file.
from .views import TaskListView

# We define the list of URL patterns for the 'tasks' app.
urlpatterns = [
    # We create a route that points to our TaskListView.
    # When someone visits '/tasks/', the 'as_view()' method turns our class 
    # into a function that Django can run to handle the request.
    path('tasks/', TaskListView.as_view(), name='task-list'),
]

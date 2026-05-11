# We import the path tool from Django's URL library.
from django.urls import path

# We import our TaskListView and TaskDetailView from our views.py file.
from .views import TaskListView, TaskDetailView

# We define the list of URL patterns for the 'tasks' app.
urlpatterns = [
    # Route for the list of all tasks.
    path('tasks/', TaskListView.as_view(), name='task-list'),
    
    # Route for a single specific task.
    # The '<int:pk>' part tells Django: "Expect a whole number here, 
    # and pass it into the view as a variable called 'pk'."
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]


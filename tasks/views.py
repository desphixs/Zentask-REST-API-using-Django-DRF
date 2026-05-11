# We import APIView, which is the base class for building custom API endpoints.
from rest_framework.views import APIView

# We import Response, which is the standard way to return data from a DRF view.
from rest_framework.response import Response

# We import our Task model so we can fetch data from the database.
from .models import Task

# We import our TaskSerializer so we can translate our Python objects into JSON.
from .serializers import TaskSerializer

# We define a new class called TaskListView that inherits from APIView.
class TaskListView(APIView):
    
    # We define a 'get' method, which Django REST Framework will automatically 
    # call whenever someone sends an HTTP GET request to this view's URL.
    def get(self, request):
        
        # We use Django's database tools to fetch every single Task record from our filing cabinet.
        tasks = Task.objects.all()
        
        # We hand our list of tasks to the translator (TaskSerializer).
        # 'many=True' is crucial here! It tells the translator: 
        # "I am handing you a whole bunch of tasks in a list, not just a single one."
        serializer = TaskSerializer(tasks, many=True)
        
        # We return the translated JSON data wrapped in a Response object.
        # This sends the data back through the internet to whoever asked for it.
        return Response(serializer.data)


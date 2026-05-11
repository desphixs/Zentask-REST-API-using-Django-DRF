# We import APIView, which is the base class for building custom API endpoints.
from rest_framework.views import APIView

# We import Response, which is the standard way to return data from a DRF view.
from rest_framework.response import Response

# We import status, which gives us the standard HTTP status codes (like 201 Created or 400 Bad Request).
from rest_framework import status

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

    # We define a 'post' method, which DRF will call whenever someone sends an HTTP POST request.
    # This is how we allow users to CREATE new tasks in our system.
    def post(self, request):
        
        # We take the raw JSON data that the user sent us (request.data) 
        # and hand it to our translator (TaskSerializer).
        serializer = TaskSerializer(data=request.data)
        
        # We ask the translator to double-check the data (validation).
        # Does the title exist? Is it too long? This prevents bad data from entering our database.
        if serializer.is_valid():
            
            # If the data is good, we tell the serializer to save it as a new Task record.
            serializer.save()
            
            # We return the newly created task's data so the user can see it worked.
            # We also send a '201 Created' status code, which is the standard way 
            # of saying "Hey, I successfully built that thing you asked for!"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the data was bad (e.g. they forgot the title), we return the error messages.
        # We send a '400 Bad Request' status code, which tells the user's app: 
        # "Something is wrong with the data you sent me."
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


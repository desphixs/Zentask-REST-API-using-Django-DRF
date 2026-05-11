# We import Http404, which is a standard way to tell Django that a specific page doesn't exist.
from django.http import Http404

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


# We define a new class called TaskDetailView that inherits from APIView.
# This receptionist handles requests for a SINGLE specific task.
class TaskDetailView(APIView):
    
    # We create a helper method to find a specific task based on its ID (pk).
    # If the task doesn't exist, it will automatically raise a 404 error.
    def get_object(self, pk):
        try:
            # We try to fetch the task from the database using its primary key (pk).
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            # If the task isn't found, we raise the standard "Not Found" error.
            raise Http404

    # We define a 'get' method that takes 'pk' as an argument.
    # This will handle GET requests for a specific task (e.g., /api/tasks/1/).
    def get(self, request, pk):
        
        # We use our helper method to find the task.
        task = self.get_object(pk)
        
        # We hand the single task to our translator (TaskSerializer).
        # Notice we DON'T use many=True here, because we are only translating ONE item.
        serializer = TaskSerializer(task)
        
        # We return the translated JSON data to the user.
        return Response(serializer.data)

    # We define a 'put' method to handle HTTP PUT requests.
    # This is how we allow users to UPDATE an existing task.
    def put(self, request, pk):
        
        # 1. We use our helper method to find the specific task we want to change.
        task = self.get_object(pk)
        
        # 2. We hand the existing task AND the new data from the user to our translator.
        # By passing both, the serializer knows it should update the existing record
        # rather than creating a brand new one.
        # 'partial=True' allows the user to update just one field (like 'is_completed') 
        # without having to send the entire task data again.
        serializer = TaskSerializer(task, data=request.data, partial=True)
        
        # 3. We check if the new data is valid.
        if serializer.is_valid():
            
            # 4. If it's valid, we save the changes to the database.
            serializer.save()
            
            # 5. We return the updated task data to the user.
            return Response(serializer.data)
            
        # 6. If the data was bad, we return the error messages.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # We define a 'delete' method to handle HTTP DELETE requests.
    # This is how we allow users to REMOVE a task from the system forever.
    def delete(self, request, pk):
        
        # 1. We use our helper method to find the specific task we want to delete.
        task = self.get_object(pk)
        
        # 2. We tell the task object to delete itself from the database.
        task.delete()
        
        # 3. We return a special '204 No Content' status code.
        # This tells the user: "Success! I deleted it, and there is nothing left to show you."
        return Response(status=status.HTTP_204_NO_CONTENT)



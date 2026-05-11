# We import the serializers module from Django REST Framework.
# This module provides the base classes for converting complex data like models into JSON.
from rest_framework import serializers

# We import our Task model so the serializer knows which data structure it is working with.
from .models import Task

# We define a new class called TaskSerializer.
# By inheriting from 'serializers.ModelSerializer', we tell Django REST Framework
# to automatically generate a serializer based on our Task model.
class TaskSerializer(serializers.ModelSerializer):
    
    # The Meta class is used to configure how the serializer behaves.
    class Meta:
        # We specify which model this serializer is tied to.
        model = Task
        
        # We use '__all__' to tell the serializer to include every single field
        # from our Task model (id, title, description, is_completed, created_at).
        fields = '__all__'
        
        # We specify fields that should be "read-only".
        # This means the user can see these fields in the response, 
        # but they cannot manually change them when creating or updating a task.
        # 'id' is managed by the database, and 'created_at' is managed by Django.
        read_only_fields = ['id', 'created_at']

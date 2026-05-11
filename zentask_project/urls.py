"""
URL configuration for zentask_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# We import include so we can link to the URL files in our individual apps.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # We use 'include' to tell Django: "If a URL starts with 'api/', 
    # go look inside the tasks app's urls.py file to find the rest of the path."
    path('api/', include('tasks.urls')),
]


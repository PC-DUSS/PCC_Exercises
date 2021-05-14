"""Define URL patterns for Django"""
from django.urls import path, include
from . import views

app_name = 'users'
# Remember, the absolute root path for all the url patterns here is 'users/'.
urlpatterns = [
    # Include default Django auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]

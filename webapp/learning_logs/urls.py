"""
Define URL patterns for learning_logs
"""
from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    # Page to display all available topics.
    path("topics/", views.topics, name="topics"),
    # Individual pages for each topic.
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    # Page for the user to create a new topic.
    path("new_topic/", views.new_topic, name="new_topic"),
    ]

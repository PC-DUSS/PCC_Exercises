"""
Define URL patterns for learning_logs
"""
from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # Always end a non-empty path with '/' character.

    # Home page.
    path('', views.index, name='index'),
    # Page to display all available topics.
    path("topics/", views.topics, name="topics"),
    # Individual pages for each topic.
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    # Page for the user to create a new topic.
    path("new_topic/", views.new_topic, name="new_topic"),
    # Page for the user to add a new entry.
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    # Page for editing an existing entry.
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    ]

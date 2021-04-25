from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    """Form for users to fill out information on Topics"""
    class Meta:
        model = Topic
        fields = ['text']
        # This tells Django not to give a label to the 'text' field.
        labels = {'text': ''}

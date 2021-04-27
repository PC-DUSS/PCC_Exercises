from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Form for users to fill out information on Topics"""
    class Meta:
        model = Topic
        fields = ['text']
        # This tells Django not to give a label to the 'text' field.
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    """Form for users to add entries to an existing topic."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

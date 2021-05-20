from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Form for users to fill out information on Topics"""
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {'text': '', 'public': 'Set Topic to public?'}


class EntryForm(forms.ModelForm):
    """Form for users to add entries to an existing topic."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

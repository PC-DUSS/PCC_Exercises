"""
Forms using pre-existing Models.
"""

from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        """Include metadata from the BlogPost class."""
        model = BlogPost
        fields = ['title', 'text']

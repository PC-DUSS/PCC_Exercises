from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
Whenever we want to modify the data that Learning Log manages, we’ll
follow these three steps: modify 'models.py', call 'makemigrations' on
learning_logs, and tell Django to 'migrate' the project.
"""


class Topic(models.Model):
    """A topic the user is learning about."""
    # Link each topic to its owner (a user). Many-to-one relationship.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # Give user the choice if the topic is to be public insead of private.
    public = models.BooleanField(default=False)
    # Create a small text field for the topic to enter.
    text = models.CharField(max_length=200)
    # Save the date&time the topic was added.
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned for a given topic."""
    # Make a many-to-one relationship with the 'Topic' object.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # Create a larger text field to write the entry.
    text = models.TextField()
    # Save the date&time the entry was entered.
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Specify the plural name for the 'Entry' object.
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"

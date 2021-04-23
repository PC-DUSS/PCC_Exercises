from django.db import models

# Create your models here.

"""
Whenever we want to modify the data that Learning Log manages, we’ll
follow these three steps: modify 'models.py', call 'makemigrations' on
learning_logs, and tell Django to 'migrate' the project.
"""


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned for a given topic."""
    # Make a many-to-one relationship with the 'Topic' object.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta():
        # Specify the plural name for the 'Entry' object.
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"

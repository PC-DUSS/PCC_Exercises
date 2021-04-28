from django.db import models

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.title}: {self.text[:50]}..."
        else:
            return f"{self.title}: {self.text}"

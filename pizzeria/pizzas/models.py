from django.db import models

# Create your models here.


class Pizza(models.Model):
    """Customizable pizza. Template for more specific types of pizza."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topping(models.Model):
    """Toppings to be put on a pizza."""
    name = models.CharField(max_length=100)
    pizza = models.ManyToManyField(Pizza)

    def __str__(self):
        return self.name

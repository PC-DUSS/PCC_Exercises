"""URL patterns for 'pizzas'."""
from django.urls import path

from . import views

app_name = 'pizzas'

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page to list entered topics
    path('pizzas/', views.pizzas, name='pizzas'),
    # A page for each topic
    path('pizzas/<int:pizza_id>', views.toppings, name='toppings'),
]

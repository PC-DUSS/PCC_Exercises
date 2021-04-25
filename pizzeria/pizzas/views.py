from django.shortcuts import render

from .models import Pizza

# Create your views here.


def index(request):
    """Home page for Pizzeria"""
    return render(request, 'pizzas/index.html')


def pizzas(request):
    """Page listing all types of pizzas"""
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)


def toppings(request, pizza_id):
    """Page listing all toppings for a pizza type"""
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.all()
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/toppings.html', context)

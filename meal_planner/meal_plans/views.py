from django.shortcuts import render

# Create your views here.


def index(request):
    """Return the home page for Meal Planner"""
    return render(request, 'meal_plans/index.html')

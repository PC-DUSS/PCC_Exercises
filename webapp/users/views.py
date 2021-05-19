"""
Pierre-Charles Dussault
May 10, 2021

View functions for html templates in the 'users' app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()

            # Now log the user in, and show homepage.
            login(request, new_user)
            return redirect('learning_logs:index')
    else:
        form = UserCreationForm()  # Blank form

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

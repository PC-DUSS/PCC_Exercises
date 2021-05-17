from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """The home page for learning_logs."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Page to display all available topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Page to display one specific topic and its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure only the owner can view his topics and no one else.
    check_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Page to create a new topic.
    The new_topic() function needs to handle two different situations: initial
    requests for the new_topic page (in which case it should show a blank form)
    and the processing of any data submitted in the form."""
    if request.method != "POST":
        # No data submitted, create blank form.
        form = TopicForm()
    else:
        # POST data was submitted, process the data into a form.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            # Associate the new topic with the current user.
            new_topic.owner = request.user
            new_topic.save()
            # When new topic is saved, redirect to a page generated by the
            # 'topics' view in 'views.py'.
            return redirect("learning_logs:topics")

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a specific topic."""
    topic = Topic.objects.get(id=topic_id)
    check_owner(topic.owner, request.user)
    if request.method != 'POST':
        # If form is empty or invalid, create a new blank EntryForm...
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # This saves the entry locally, so we can attribute it to its topic
            # before making the final save.
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # Redirect to the same topic's page generated by the 'topic' view
            # in 'views.py'.
            return redirect("learning_logs:topic", topic_id=topic_id)
            # Notice how we pass it the 'topic_id' variable, as it is needed
            # in 'views.py' to show the appropriate topic page.

    # Give the template for a new blank form the context variables and let it
    # display the blank form to the user.
    context = {'topic': topic, 'form': form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry. When it receives a GET request, it returns a
    form for editing the entry. When it receives a POST request, it saves the
    modified text into the database."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_owner(topic.owner, request.user)
    if request.method != "POST":
        # Initial request, pre-fill the form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # Process the filled form's data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, "learning_logs/edit_entry.html", context)


def check_owner(owner, current_user):
    """Checks if current user is the owner of the item he wishes to see or
    modify."""
    if owner != current_user:
        raise Http404

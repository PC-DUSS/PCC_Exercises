from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm

# Create your views here.


def index(request):
    """The home page for learning_logs."""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Page to display all available topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Page to display one specific topic and its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


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
            form.save()
            # When new topic is saved, redirect user to the list of topics.
            return redirect("learning_logs:topics")

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)

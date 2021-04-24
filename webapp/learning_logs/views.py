from django.shortcuts import render

from .models import Topic

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

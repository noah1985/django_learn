from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import TopicForm, EntryForm
from .models import Topic, Entry


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    tops = Topic.objects.order_by('date_added')
    context = {'topics': tops}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    top = Topic.objects.get(id=topic_id)
    entries = top.entry_set.order_by('-date_added')
    context = {'topic': top, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    top = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            e.topic = top
            e.save()

        return HttpResponseRedirect(
            reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': top, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    top = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[top.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

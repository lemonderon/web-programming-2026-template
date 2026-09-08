from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from todolist.forms import NewTaskForm


def index(request):
    return render(request, 'todolist/index.html', {'todolist': request.session.get('tasks', [])})


def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            if 'tasks' not in request.session:
                request.session['tasks'] = []
            request.session['tasks'].append(task)
            return HttpResponseRedirect(reverse('todolist:tasks_list'))
        else:
            return render(request, 'todolist/add.html', {'form': form})
    return render(request, 'todolist/add.html', {'form': NewTaskForm()})


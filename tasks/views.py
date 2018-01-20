from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from tasks.models import Task, TaskRequest
from polity.models import Polity
from tasks.forms import TaskForm

def task_list(request, polity_id):
    polity = get_object_or_404(Polity, id=polity_id)
    tasks = polity.task_set.order_by('-created')

    ctx = {
        'polity': polity,
        'tasks': tasks,
        'user_is_member': polity.is_member(request.user),
        'user_is_officer': polity.is_officer(request.user),
        'user_is_wrangler': polity.is_wrangler(request.user),
    }
    return render(request, 'tasks/task_list.html', ctx)


@login_required
def task_add_edit(request, polity_id, task_id=None):
    polity = get_object_or_404(Polity, id=polity_id)
    if not (polity.is_member(request.user) or polity.is_wrangler(request.user)):
        raise PermissionDenied()

    if task_id:
        task = get_object_or_404(Task, id=task_id, polity=polity)
        # We don't want to edit anything that has already done.
        if task.is_done:
            raise PermissionDenied()
    else:
        task = Task(polity=polity)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect(reverse('task_detail', args=(polity_id, task.id)))
    else:
        form = TaskForm(instance=task)

    ctx = {
        'polity': polity,
        'form': form,
        'user_is_member': polity.is_member(request.user),
        'user_is_officer': polity.is_officer(request.user),
        'user_is_wrangler': polity.is_wrangler(request.user),
    }
    return render(request, 'tasks/task_add_edit.html', ctx)


def task_detail(request, polity_id, task_id):
    polity = get_object_or_404(Polity, id=polity_id)
    task = get_object_or_404(Task, id=task_id, polity=polity)
    has_applied = TaskRequest.objects.filter(task=task, user=request.user).first() or False

    if request.method == 'POST' and not has_applied:
        whyme = request.POST.get('whyme')
        if whyme.strip() != '':
            tr = TaskRequest()
            tr.task = task
            tr.user = request.user
            tr.whyme = whyme
            tr.save()
            has_applied = True

    ctx = {
        'polity': polity,
        'task': task,
        'has_applied': has_applied,
        'user_is_member': polity.is_member(request.user),
        'user_is_officer': polity.is_officer(request.user),
        'user_is_wrangler': polity.is_wrangler(request.user),
    }
    return render(request, 'tasks/task_detail.html', ctx)


def task_applications(request, polity_id):
    polity = get_object_or_404(Polity, id=polity_id)
    if not (polity.is_member(request.user) or polity.is_wrangler(request.user)):
        raise PermissionDenied()

    show_done = False

    tasks = polity.task_set.filter(is_done=show_done).order_by('-created')

    ctx = {
        'polity': polity,
        'tasks': tasks,
        'user_is_member': polity.is_member(request.user),
        'user_is_officer': polity.is_officer(request.user),
        'user_is_wrangler': polity.is_wrangler(request.user),
    }
    return render(request, 'tasks/task_applications.html', ctx)

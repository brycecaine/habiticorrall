from . import service
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render


@login_required
def index(request):
    user_list = service.get_user_data()
    chat_list = service.get_chat_data()

    return render(request, 'index.html', locals())


@login_required
def score(request, username, task_id):
    result_msg = service.score_task(username, task_id)
    messages.info(request, result_msg)

    # return redirect('/dashboard')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def tasks(request, username):
    curr_person = service.get_person(username)
    persons = service.get_persons()
    dailies, habits, todos = service.get_tasks(username)

    return render(request, 'tasks.html', locals())


@login_required
def profile(request, username):
    curr_person = service.get_person(username)
    persons = service.get_persons()
    user_data = service.get_items(username)

    return render(request, 'profile.html', locals())
from . import service
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def index(request):
    user_list = service.get_user_data()
    chat_list = service.get_chat_data()

    return render(request, 'index.html', locals())


@login_required
def score(request, user_id, task_id):
    result_msg = service.score_task(user_id, task_id)
    messages.info(request, result_msg)

    return redirect('/dashboard')
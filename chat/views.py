from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from chat.forms import ChatmessageCreateForm
from chat.models import ChatGroup

@login_required
def chat_view(request, chatroom_name='public_group'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'chat/partials/chat_message_p.html', context)
    return render(request, 'chat/chat.html', {'chat_messages': chat_messages, 'form': form})

from django.shortcuts import render, get_object_or_404

from .models import Message

def index(request):
    latest_messages_list = Message.objects.order_by("-time")
    context = {"latest_messages_list": latest_messages_list}
    return render(request, "chat/index.html", context)

def detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, "chat/detail.html", {"message": message})
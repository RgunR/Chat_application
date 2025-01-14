from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .models import Message

def home(request):
    return HttpResponse("Welcome to the home page!")

@login_required
def chat(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat.html', {'users': users})

@login_required
def chat_with_user(request, user_id):
    receiver = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    )
    messages = messages.order_by('timestamp')
    return render(request, 'chat_with_user.html', {'receiver': receiver, 'messages': messages})

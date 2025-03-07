from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

@login_required
def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, 'chat/room.html', {
        'room': room,
        'username': request.user.username
    })
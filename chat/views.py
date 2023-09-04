from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat
from agents.models import AgentDB

class ChatReadView(View):

    def get(self, request, agent_id:int):
        agent = get_object_or_404(AgentDB, id=agent_id)
        chats = Chat.objects.filter(agent=agent)
        context = {"agent": agent, "chats": chats}
        return render(request, "chat/chat.html", context)
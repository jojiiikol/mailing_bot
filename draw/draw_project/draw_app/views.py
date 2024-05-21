import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import *
import requests


class MainView(View):
    model = DrawUsers
    template_name = 'index.html'
    queryset = DrawUsers.objects.filter(joined_to_chanel=True)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'users': self.queryset})

    def post(self, request, *args, **kwargs):
        winner = self.queryset.filter(joined_to_chanel=True, winner=False).order_by('?').first()
        if winner:
            winner.winner = True
            winner.save()
            req = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
            data = {
                'chat_id': winner.tg_id,
                'text': 'Поздравляю, ты победил, просим тебя подняться на сцену'
            }
            requests.post(req, data=data)
            return render(request, self.template_name, {'users': winner})
        else:
            return HttpResponse("Нет победителя")

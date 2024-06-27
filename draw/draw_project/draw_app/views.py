import os
import random

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import *
import requests
from .serializers import *


class WheelsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'draw_app/whell.html'

    def get(self, request, *args, **kwargs):
        return Response()


class GetCountView(APIView):
    def get(self, request, *args, **kwargs):
        data = DrawUsers.objects.filter(winner=False, joined_to_chanel=True)
        serializer = UsersSerializer(data, many=True)
        return Response(
            {
                'users': serializer.data,
            }
        )


class Action(APIView):
    def get(self, request, *args, **kwargs):
        data = DrawUsers.objects.filter(winner=False, joined_to_chanel=True)
        user_winner = random.choice(data)
        winner_index = list(data).index(user_winner)
        data[winner_index].winner = True
        serializer = UsersSerializer(data, many=True)

        user_winner.winner = True
        user_winner.save()



        return Response(
            {
                'users': serializer.data,
            }
        )

class Mailing(APIView):
    def post(self, request, *args, **kwargs):
        user_winner = DrawUsers.objects.get(tg_name=request.data['tg_name'])
        req = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
        data = {
            'chat_id': user_winner.tg_id,
            'text': 'Поздравляем, ты выиграл в розыгрыше, просим тебя подняться на сцену!'
        }
        requests.post(req, data=data)

        return Response({'status': 'Ok'})
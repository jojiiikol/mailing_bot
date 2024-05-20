from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import *


class MainView(View):
    model = DrawUsers
    template_name = 'index.html'
    queryset = DrawUsers.objects.filter(joined_to_chanel=True)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'users': self.queryset})

    def post(self, request, *args, **kwargs):
        winner = self.queryset.order_by('?').first()
        return render(request, self.template_name, {'users': winner})

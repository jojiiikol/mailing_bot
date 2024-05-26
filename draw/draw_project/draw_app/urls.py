from django.urls import path
from .views import *

urlpatterns = [
    path('get_winner/', Action.as_view(), name='test'),
    path('', WheelsView.as_view()),
    path('get_count/', GetCountView.as_view()),
    path('mailing/', Mailing.as_view())
]
from rest_framework.serializers import ModelSerializer
from .models import *

class UsersSerializer(ModelSerializer):
    class Meta:
        model = DrawUsers
        fields = ('id', 'tg_name', 'winner', 'sex')

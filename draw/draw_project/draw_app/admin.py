from django.contrib import admin
from .models import *

@admin.register(DrawUsers)
class DrawUsersAdmin(admin.ModelAdmin):
    list_display = ['tg_name', 'joined_to_chanel', 'winner']

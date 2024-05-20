from django.db import models


class DrawUsers(models.Model):
    tg_id = models.BigIntegerField()
    tg_name = models.CharField(max_length=1024)
    joined_to_chanel = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.tg_name

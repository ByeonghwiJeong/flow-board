from django.db import models


class FreeBoard(models.Model):
    password   = models.CharField(max_length=200)
    title      = models.CharField(max_length=20)
    content    = models.CharField(max_length=200)
    weather    = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'freeboard'

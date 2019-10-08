from django.db import models

class VideoGame(models.Model):
    platform = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    developer = models.CharField(max_length=100)

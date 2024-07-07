# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# class Player(models.Model):
#     name = models.CharField(max_length=100)
#     position = models.CharField(max_length=50)
#     team = models.CharField(max_length=50)
#     stats = models.JSONField()


# class Draft(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     team_name = models.CharField(max_length=100)
#     players = models.ManyToManyField(Player)
#     favorited_players = models.ManyToManyField(Player, related_name="favorited_by")

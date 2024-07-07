# Create your views here.
from django.shortcuts import render

from .models import Player


def home(request):
    players = Player.objects.all()
    return render(request, "draft/home.html", {"players": players})


def mock_draft(request):
    return render(request, "draft/mock_draft.html")


def live_draft(request):
    return render(request, "draft/live_draft.html")


def statistics(request):
    return render(request, "draft/statistics.html")

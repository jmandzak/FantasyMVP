# Create your views here.
from django.conf import settings
from django.shortcuts import render

from .parse_csv import read_player_stats


def home(request):
    return render(request, "draft/home.html")


def mock_draft(request):
    return render(request, "draft/mock_draft.html")


def live_draft(request):
    return render(request, "draft/live_draft.html")


def statistics(request):
    players = read_player_stats(settings.CSV_FILE_PATH)
    return render(request, "draft/statistics.html", {"players": players.values()})

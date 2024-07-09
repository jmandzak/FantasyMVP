# Create your views here.
from django.conf import settings
from django.shortcuts import render

from .parse_csv import read_player_stats
from .player import BasicInfo, StandardStats


def home(request):
    return render(request, "draft/home.html")


def mock_draft(request):
    return render(request, "draft/mock_draft.html")


def live_draft(request):
    return render(request, "draft/live_draft.html")


def statistics(request):
    players = read_player_stats(settings.CSV_FILE_PATH).values()
    row_values = [
        p.basic_info.get_values_as_list() + p.standard_stats.get_values_as_list()
        for p in players
    ]
    row_headers = BasicInfo.all_stat_labels() + StandardStats.all_stat_labels()

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )

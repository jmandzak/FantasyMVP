# Create your views here.
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .parse_csv import read_player_stats, sort_players
from .player import *


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "draft/home.html")


def mock_draft(request: HttpRequest) -> HttpResponse:
    return render(request, "draft/mock_draft.html")


def live_draft(request: HttpRequest) -> HttpResponse:
    return render(request, "draft/live_draft.html")


def all_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
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


def all_ppr_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, True).values()
    row_values = [
        p.basic_info.get_values_as_list() + p.ppr_stats.get_values_as_list()
        for p in players
    ]
    row_headers = BasicInfo.all_stat_labels() + PPRStats.all_stat_labels()

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def qb_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "QB"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.quarterback_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + PassingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def rb_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "RB"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.standard_stats.get_values_as_list()
        + p.runningback_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + RushingStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def rb_ppr_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, True).values()
    players = [p for p in players if p.basic_info.position == "RB"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.runningback_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + RushingStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def wr_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "WR"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.standard_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def wr_ppr_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, True).values()
    players = [p for p in players if p.basic_info.position == "WR"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def te_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "TE"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.standard_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def te_ppr_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, True).values()
    players = [p for p in players if p.basic_info.position == "TE"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.receiver_stats.get_values_as_list()
        + p.redzone_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
        + RedzoneStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def k_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "K"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.kicker_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + KickerStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )


def def_statistics(request: HttpRequest) -> HttpResponse:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = sort_players(players, False).values()
    players = [p for p in players if p.basic_info.position == "DEF"]
    row_values = [
        p.basic_info.get_values_as_list()
        + p.ppr_stats.get_values_as_list()
        + p.defense_stats.get_values_as_list()
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + DefenseStats.all_stat_labels()
    )

    return render(
        request,
        "draft/statistics.html",
        {"players": row_values, "headers": row_headers},
    )

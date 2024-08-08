# Create your views here.
from django.conf import settings
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .parse_csv import read_player_stats, sort_players
from .player import *

PPR = False
MY_DRAFTED_PLAYERS: typing.List[str] = []
OTHER_DRAFTED_PLAYERS: typing.List[str] = []


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "draft/home.html")


def mock_draft(request: HttpRequest) -> HttpResponse:
    return render(request, "draft/mock_draft.html")


def _get_players(position) -> typing.List[Player]:
    players = read_player_stats(settings.CSV_FILE_PATH)
    players = list(sort_players(players, False).values())
    if position != "all":
        players = [p for p in players if p.basic_info.position.lower() == position]
    players = [
        p
        for p in players
        if p.basic_info.name not in MY_DRAFTED_PLAYERS + OTHER_DRAFTED_PLAYERS
    ]
    return players


def _get_row_values(
    players: typing.List[Player], position: str
) -> typing.List[typing.List[str]]:
    row_values = [
        p.basic_info.get_values_as_list() + p.scoring_based_stats(PPR) for p in players
    ]
    if position != "all":
        for row, player in zip(row_values, players):
            row.extend(player.position_based_stats())
    return row_values


def _get_column_headers(
    players: typing.List[Player], position: str
) -> typing.List[str]:
    header_labels = BasicInfo.all_stat_labels() + players[0].scoring_based_labels(PPR)
    if position != "all":
        header_labels.extend(players[0].position_based_labels())
    return header_labels


def _add_player_to_my_drafted_players(player_name: str):
    global MY_DRAFTED_PLAYERS
    MY_DRAFTED_PLAYERS.append(player_name)


def _add_player_to_other_drafted_players(player_name: str):
    global OTHER_DRAFTED_PLAYERS
    OTHER_DRAFTED_PLAYERS.append(player_name)


@csrf_exempt
def draft_player(request):
    if request.method == "POST":
        global MY_DRAFTED_PLAYERS
        player_name = request.POST.get("player_name")
        position = request.POST.get("position")
        _add_player_to_my_drafted_players(player_name)
        players = _get_players(position)
        row_values = _get_row_values(players, position)
        header_labels = _get_column_headers(players, position)

        return JsonResponse({"players": row_values, "headers": header_labels})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def remove_player(request):
    if request.method == "POST":
        global OTHER_DRAFTED_PLAYERS
        player_name = request.POST.get("player_name")
        position = request.POST.get("position")
        _add_player_to_other_drafted_players(player_name)
        players = _get_players(position)
        row_values = _get_row_values(players, position)
        header_labels = _get_column_headers(players, position)

        return JsonResponse({"players": row_values, "headers": header_labels})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def change_position(request):
    if request.method == "POST":
        position = request.POST.get("position")
        players = _get_players(position)
        row_values = _get_row_values(players, position)
        header_labels = _get_column_headers(players, position)

        return JsonResponse({"players": row_values, "headers": header_labels})

    return JsonResponse({"error": "Invalid request"}, status=400)


def live_draft(request: HttpRequest) -> HttpResponse:
    errors = []
    global PPR

    if request.method == "POST":
        total_teams = request.POST["total_teams"]
        draft_position = request.POST["draft_position"]
        ppr = request.POST["ppr"]

        try:
            total_teams = int(total_teams)
            draft_position = int(draft_position)
            if total_teams < 1 or total_teams > 32:
                raise ValidationError("Total teams must be between 1 and 32.")
            if draft_position < 1 or draft_position > total_teams:
                raise ValidationError(
                    "Draft position must be between 1 and the total number of teams."
                )
            if ppr not in ["yes", "no"]:
                raise ValidationError("PPR must be 'yes' or 'no'.")
            PPR = ppr == "yes"

            form_data = {
                "total_teams": total_teams,
                "draft_position": draft_position,
                "ppr": ppr,
            }
        except (ValueError, ValidationError) as e:
            errors.append(str(e))
    else:
        form_data = {}

    players = read_player_stats(settings.CSV_FILE_PATH)
    players = list(sort_players(players, False).values())
    row_values = [
        p.basic_info.get_values_as_list() + p.scoring_based_stats(PPR) for p in players
    ]
    row_headers = BasicInfo.all_stat_labels() + players[0].scoring_based_labels(PPR)

    return render(
        request,
        "draft/live_draft.html",
        {"players": row_values, "headers": row_headers, "form_data": form_data},
    )


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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + PassingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + RushingStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + RushingStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + StandardStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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
        for p in players
    ]
    row_headers = (
        BasicInfo.all_stat_labels()
        + PPRStats.all_stat_labels()
        + ReceivingStats.all_stat_labels()
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

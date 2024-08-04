import os
from typing import Dict

import numpy as np
import pandas as pd

from .player import Player


def read_player_stats(filename: str) -> Dict[str, Player]:
    df = pd.read_csv(filename)
    player_stats = {}
    for _, row in df.iterrows():
        temp = row.to_dict()
        player = Player(temp)
        player_stats[player.basic_info.name] = player

    players = _clean_players(player_stats)
    return players


def sort_players(players: Dict[str, Player], ppr: bool) -> Dict[str, Player]:
    if ppr:
        return dict(sorted(players.items(), key=lambda x: x[1].ppr_stats.adp))
    return dict(sorted(players.items(), key=lambda x: x[1].standard_stats.adp))


def _clean_players(players: Dict[str, Player]) -> Dict[str, Player]:
    player_values = list(players.values())
    for player in player_values:
        if _contains_nan(player):
            players.pop(player.basic_info.name)
    return players


def _contains_nan(player: Player) -> bool:
    return (
        np.isnan(player.standard_stats.average_rank)
        or np.isnan(player.ppr_stats.average_rank)
        or np.isnan(player.standard_stats.fantasy_points)
        or np.isnan(player.ppr_stats.fantasy_points)
    )

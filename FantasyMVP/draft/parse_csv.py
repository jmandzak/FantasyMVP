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
    return _sort_players(player_stats)


# sort players by average rank
def _sort_players(players: Dict[str, Player]) -> Dict[str, Player]:
    return dict(sorted(players.items(), key=lambda x: x[1].basic_info.average_rank))


def _clean_players(players: Dict[str, Player]) -> Dict[str, Player]:
    player_values = list(players.values())
    for player in player_values:
        if np.isnan(player.basic_info.average_rank):
            players.pop(player.basic_info.name)
    return players

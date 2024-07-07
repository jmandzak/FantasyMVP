from __future__ import annotations

import dataclasses
import typing


class Player:
    def __init__(self, csv_row: typing.Dict[str, typing.Any]) -> None:
        self.basic_info = BasicInfo.from_csv_row(csv_row)
        self.position_stats = PositionStats.from_csv_row(csv_row)
        self.ppr_stats = PPRStats.from_csv_row(csv_row)
        self.quarterback_stats = PassingStats.from_csv_row(csv_row)
        self.runningback_stats = RushingStats.from_csv_row(csv_row)
        self.receiver_stats = ReceivingStats.from_csv_row(csv_row)
        self.defense_stats = DefenseStats.from_csv_row(csv_row)
        self.kicker_stats = KickerStats.from_csv_row(csv_row)


@dataclasses.dataclass
class PassingStats:
    attempts: int
    completions: int
    interceptions: int
    completion_percent: float
    touchdowns: int
    yards: int
    average_attempts: float
    average_completions: float
    average_interceptions: float
    average_completion_percent: float
    average_touchdowns: float
    average_yards: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Passing Attempts",
            "Passing Completions",
            "Passing Interceptions",
            "Passing Completion Percent",
            "Passing Touchdowns",
            "Passing Yards",
            "Average Passing Attempts",
            "Average Passing Completions",
            "Average Passing Interceptions",
            "Average Passing Completion Percent",
            "Average Passing Touchdowns",
            "Average Passing Yards",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> PassingStats:
        return PassingStats(
            attempts=row["PASS_ATT"],
            completions=row["PASS_COMP"],
            interceptions=row["INT"],
            completion_percent=row["PASS_PCT"],
            touchdowns=row["PASS_TDS"],
            yards=row["PASS_YDS"],
            average_attempts=row["AVG_PASS_ATT"],
            average_completions=row["AVG_PASS_COMP"],
            average_interceptions=row["AVG_PASS_INT"],
            average_completion_percent=row["AVG_PASS_PCT"],
            average_touchdowns=row["AVG_PASS_TDS"],
            average_yards=row["AVG_YDS"],
        )


@dataclasses.dataclass
class RushingStats:
    attempts: int
    touchdowns: int
    yards: int
    average_attempts: float
    average_touchdowns: float
    average_yards: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Rushing Attempts",
            "Rushing Touchdowns",
            "Rushing Yards",
            "Average Rushing Attempts",
            "Average Rushing Touchdowns",
            "Average Rushing Yards",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> RushingStats:
        return RushingStats(
            attempts=row["RUSH_ATT"],
            touchdowns=row["RUSH_TDS"],
            yards=row["RUSH_YDS"],
            average_attempts=row["AVG_RUSH_ATT"],
            average_touchdowns=row["AVG_RUSH_TDS"],
            average_yards=row["AVG_RUSH_YDS"],
        )


@dataclasses.dataclass
class ReceivingStats:
    receptions: int
    touchdowns: int
    yards: int
    targets: int
    average_receptions: float
    average_touchdowns: float
    average_yards: float
    average_targets: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Receiving Receptions",
            "Receiving Touchdowns",
            "Receiving Yards",
            "Receiving Targets",
            "Average Receiving Receptions",
            "Average Receiving Touchdowns",
            "Average Receiving Yards",
            "Average Receiving Targets",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> ReceivingStats:
        return ReceivingStats(
            receptions=row["REC"],
            touchdowns=row["REC_TDS"],
            yards=row["REC_YDS"],
            targets=row["TGT"],
            average_receptions=row["AVG_REC"],
            average_touchdowns=row["AVG_REC_TDS"],
            average_yards=row["AVG_REC_YDS"],
            average_targets=row["AVG_TGT"],
        )


@dataclasses.dataclass
class DefenseStats:
    blocked_kicks: int
    touchdowns: int
    fumble_recoveries: int
    interceptions: int
    points_against: int
    return_touchdowns: int
    sacks: int
    safeties: int
    average_blocked_kicks: float
    average_touchdowns: float
    average_fumble_recoveries: float
    average_interceptions: float
    average_points_against: float
    average_return_touchdowns: float
    average_sacks: float
    average_safeties: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Blocked Kicks",
            "Touchdowns",
            "Fumble Recoveries",
            "Interceptions",
            "Points Against",
            "Return Touchdowns",
            "Sacks",
            "Safeties",
            "Average Blocked Kicks",
            "Average Touchdowns",
            "Average Fumble Recoveries",
            "Average Interceptions",
            "Average Points Against",
            "Average Return Touchdowns",
            "Average Sacks",
            "Average Safeties",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> DefenseStats:
        return DefenseStats(
            blocked_kicks=row["BLK KICK"],
            touchdowns=row["DEF TD"],
            fumble_recoveries=row["FUMR"],
            interceptions=row["INT"],
            points_against=row["PTS VS."],
            return_touchdowns=row["RET TD"],
            sacks=row["SACK"],
            safeties=row["SAFE"],
            average_blocked_kicks=row["AVG_BLK KICK"],
            average_touchdowns=row["AVG_DEF TD"],
            average_fumble_recoveries=row["AVG_FUMR"],
            average_interceptions=row["AVG_INT"],
            average_points_against=row["AVG_PTS VS."],
            average_return_touchdowns=row["AVG_RET TD"],
            average_sacks=row["AVG_SACK"],
            average_safeties=row["AVG_SAFE"],
        )


@dataclasses.dataclass
class KickerStats:
    field_goals_made: int
    extra_points_made: int
    extra_points_attempted: int
    average_extra_points_made: float
    average_extra_points_attempted: float
    average_field_goals_made: float
    fg_0_19: int
    fg_20_29: int
    fg_30_39: int
    fg_40_49: int
    fg_50_plus: int
    fg_0_19_average: float
    fg_20_29_average: float
    fg_30_39_average: float
    fg_40_49_average: float
    fg_50_plus_average: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Field Goals Made",
            "Extra Points Made",
            "Extra Points Attempted",
            "Average Extra Points Made",
            "Average Extra Points Attempted",
            "Average Field Goals Made",
            "FG 0-19",
            "FG 20-29",
            "FG 30-39",
            "FG 40-49",
            "FG 50+",
            "FG 0-19 Average",
            "FG 20-29 Average",
            "FG 30-39 Average",
            "FG 40-49 Average",
            "FG 50+ Average",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> KickerStats:
        fgm = row["0-19"] + row["20-29"] + row["30-39"] + row["40-49"] + row["50+"]
        xpa = row["XPA"]
        xpm = row["XPM"]
        average_xpa = row["AVG_XPA"]
        average_xpm = row["AVG_XPM"]
        if average_xpa == 0:
            average_fgm = 0
        else:
            games = xpa / average_xpa
            average_fgm = fgm / games
        return KickerStats(
            field_goals_made=fgm,
            extra_points_made=xpm,
            extra_points_attempted=xpa,
            average_extra_points_made=average_xpm,
            average_extra_points_attempted=average_xpa,
            average_field_goals_made=average_fgm,
            fg_0_19=row["0-19"],
            fg_20_29=row["20-29"],
            fg_30_39=row["30-39"],
            fg_40_49=row["40-49"],
            fg_50_plus=row["50+"],
            fg_0_19_average=row["AVG_0-19"],
            fg_20_29_average=row["AVG_20-29"],
            fg_30_39_average=row["AVG_30-39"],
            fg_40_49_average=row["AVG_40-49"],
            fg_50_plus_average=row["AVG_50+"],
        )


@dataclasses.dataclass
class PositionStats:
    average_rank: float
    best_rank: float
    worst_rank: float
    rank: float
    standard_deviation: float
    tier: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Position Average Rank",
            "Position Best Rank",
            "Position Worst Rank",
            "Position Rank",
            "Position Standard Deviation",
            "Position Tier",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> PositionStats:
        return PositionStats(
            average_rank=row["POS_AVG."],
            best_rank=row["POS_BEST"],
            worst_rank=row["POS_WORST"],
            rank=row["POS_RK"],
            standard_deviation=row["POS_STD.DEV"],
            tier=row["POS_TIERS"],
        )


@dataclasses.dataclass
class PPRStats:
    average_rank: float
    best_rank: float
    worst_rank: float
    rank: float
    tier: float
    standard_deviation: float
    position_average_rank: float
    position_best_rank: float
    position_worst_rank: float
    position_rank: float
    position_tier: float
    position_std_dev: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "PPR Average Rank",
            "PPR Best Rank",
            "PPR Worst Rank",
            "PPR Rank",
            "PPR Tier",
            "PPR Standard Deviation",
            "PPR Position Average Rank",
            "PPR Position Best Rank",
            "PPR Position Worst Rank",
            "PPR Position Rank",
            "PPR Position Tier",
            "PPR Position Standard Deviation",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> PPRStats:
        return PPRStats(
            average_rank=row["PPR_AVG_RK"],
            best_rank=row["PPR_BEST_RK"],
            worst_rank=row["PPR_WORST_RK"],
            rank=row["PPR_RK"],
            tier=row["PPR_TIERS"],
            standard_deviation=row["PPR_STD.DEV_RK"],
            position_average_rank=row["PPR_POS_AVG."],
            position_best_rank=row["PPR_POS_BEST"],
            position_worst_rank=row["PPR_POS_WORST"],
            position_rank=row["PPR_POS_RK"],
            position_tier=row["PPR_POS_TIERS"],
            position_std_dev=row["PPR_POS_STD.DEV"],
        )


@dataclasses.dataclass
class BasicInfo:
    name: str
    position: str
    team: str
    season_sos: float
    full_sos: float
    playoff_sos: float
    boom: float
    bust: float
    starter: float
    fantasy_points: float
    average_fantasy_points: float
    depth: int
    average_rank: float
    best_rank: float
    worst_rank: float
    rank: float
    standard_deviation: float
    tier: float

    @property
    def all_stat_labels(self) -> typing.List[str]:
        return [
            "Name",
            "Position",
            "Team",
            "Season SOS",
            "Full SOS",
            "Playoff SOS",
            "Boom",
            "Bust",
            "Starter",
            "Fantasy Points",
            "Average Fantasy Points",
            "Depth",
            "Average Rank",
            "Best Rank",
            "Worst Rank",
            "Rank",
            "Standard Deviation",
            "Tier",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> BasicInfo:
        return BasicInfo(
            name=_clean_name(row["PLAYER NAME"]),
            position=row["POS"],
            team=row["TEAM"],
            season_sos=row["SEASON_SOS"],
            full_sos=row["FULL_SOS"],
            playoff_sos=row["PLAYOFF_SOS"],
            boom=row["BOOM"],
            bust=row["BUST"],
            starter=row["STARTER"],
            fantasy_points=row["FAN PTS"],
            average_fantasy_points=row["AVG_FAN PTS"],
            depth=row["DEPTH"],
            average_rank=row["AVG_RK"],
            best_rank=row["BEST_RK"],
            worst_rank=row["WORST_RK"],
            rank=row["RK"],
            standard_deviation=row["STD.DEV_RK"],
            tier=row["TIERS"],
        )


def _clean_name(name: str) -> str:
    # Currently names are all CAPS, so just make them title case where dashes count as spaces when doing the titling
    return name.title()

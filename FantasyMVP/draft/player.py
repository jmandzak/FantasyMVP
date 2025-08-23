from __future__ import annotations

import dataclasses
import math
import typing

import numpy as np


class Player:
    def __init__(self, csv_row: typing.Dict[str, typing.Any]) -> None:
        csv_row = _clean_dict(csv_row)
        self.basic_info = BasicInfo.from_csv_row(csv_row)
        self.standard_stats = StandardStats.from_csv_row(csv_row)
        self.ppr_stats = PPRStats.from_csv_row(csv_row)
        if self.basic_info.position in ["QB", "DEF", "K"]:
            self.ppr_stats = self.standard_stats
        self.quarterback_stats = PassingStats.from_csv_row(csv_row)
        self.runningback_stats = RushingStats.from_csv_row(csv_row)
        self.receiver_stats = ReceivingStats.from_csv_row(csv_row)
        self.defense_stats = DefenseStats.from_csv_row(csv_row)
        self.kicker_stats = KickerStats.from_csv_row(csv_row)
        self.snap_share_stats = SnapShareStats.from_csv_row(csv_row)
        self.team_target_share_stats = TeamTargetShareStats.from_csv_row(csv_row)
        self.advanced_receiver_stats = AdvancedReceivingStats.from_csv_row(csv_row)

    def scoring_based_stats(self, ppr: bool) -> typing.List[typing.Any]:
        if ppr:
            return self.ppr_stats.get_values_as_list()
        return self.standard_stats.get_values_as_list()

    def position_based_stats(self) -> typing.List[typing.Any]:
        if self.basic_info.position == "QB":
            return (
                self.quarterback_stats.get_values_as_list()
                + self.runningback_stats.get_values_as_list()
            )
        if self.basic_info.position == "RB":
            return (
                self.runningback_stats.get_values_as_list()
                + self.receiver_stats.get_values_as_list()
                + self.snap_share_stats.get_values_as_list()
                + self.team_target_share_stats.get_values_as_list(
                    self.basic_info.position
                )
            )
        if self.basic_info.position in ["WR", "TE"]:
            return (
                self.receiver_stats.get_values_as_list()
                + self.snap_share_stats.get_values_as_list()
                + self.advanced_receiver_stats.get_values_as_list()
                + self.team_target_share_stats.get_values_as_list(
                    self.basic_info.position
                )
            )
        if self.basic_info.position == "DEF":
            return self.defense_stats.get_values_as_list()
        if self.basic_info.position == "K":
            return self.kicker_stats.get_values_as_list()
        assert False, f"Unknown position: {self.basic_info.position}"

    def scoring_based_labels(self, ppr: bool) -> typing.List[str]:
        if ppr:
            return PPRStats.all_stat_labels()
        return StandardStats.all_stat_labels()

    def position_based_labels(self) -> typing.List[str]:
        if self.basic_info.position == "QB":
            return PassingStats.all_stat_labels() + RushingStats.all_stat_labels()
        if self.basic_info.position == "RB":
            return (
                RushingStats.all_stat_labels()
                + ReceivingStats.all_stat_labels()
                + SnapShareStats.all_stat_labels()
            )
        if self.basic_info.position in ["WR", "TE"]:
            return ReceivingStats.all_stat_labels() + SnapShareStats.all_stat_labels()
        if self.basic_info.position == "DEF":
            return DefenseStats.all_stat_labels()
        if self.basic_info.position == "K":
            return KickerStats.all_stat_labels()
        assert False, f"Unknown position: {self.basic_info.position}"


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
    pass_air_yds: int
    pass_air_yds_per_att: float
    pass_10_yds: int
    pass_20_yds: int
    pass_30_yds: int
    pass_40_yds: int
    pass_50_yds: int
    pocket_time: float
    blitz: int
    poor_pass: int
    avg_pass_10_yds: float
    avg_pass_20_yds: float
    avg_pass_30_yds: float
    avg_pass_40_yds: float
    avg_pass_50_yds: float
    avg_blitz: float
    avg_poor_pass: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.attempts,
            self.completions,
            self.interceptions,
            self.completion_percent,
            self.touchdowns,
            self.yards,
            self.average_attempts,
            self.average_completions,
            self.average_interceptions,
            self.average_completion_percent,
            self.average_touchdowns,
            self.average_yards,
            self.pass_air_yds,
            self.pass_air_yds_per_att,
            self.pass_10_yds,
            self.pass_20_yds,
            self.pass_30_yds,
            self.pass_40_yds,
            self.pass_50_yds,
            self.pocket_time,
            self.blitz,
            self.poor_pass,
            self.avg_pass_10_yds,
            self.avg_pass_20_yds,
            self.avg_pass_30_yds,
            self.avg_pass_40_yds,
            self.avg_pass_50_yds,
            self.avg_blitz,
            self.avg_poor_pass,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
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
            "Pass Air Yards",
            "Pass Air Yards per Attempt",
            "Passes 10+ Yards",
            "Passes 20+ Yards",
            "Passes 30+ Yards",
            "Passes 40+ Yards",
            "Passes 50+ Yards",
            "Pocket Time",
            "Blitz",
            "Poor Pass",
            "Avg Passes 10+ Yards",
            "Avg Passes 20+ Yards",
            "Avg Passes 30+ Yards",
            "Avg Passes 40+ Yards",
            "Avg Passes 50+ Yards",
            "Avg Blitz",
            "Avg Poor Pass",
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
            pass_air_yds=row["PASS_AIR_YDS"],
            pass_air_yds_per_att=row["PASS_AIR_YDS_PER_ATT"],
            pass_10_yds=row["PASS_10_YDS"],
            pass_20_yds=row["PASS_20_YDS"],
            pass_30_yds=row["PASS_30_YDS"],
            pass_40_yds=row["PASS_40_YDS"],
            pass_50_yds=row["PASS_50_YDS"],
            pocket_time=row["POCKET_TIME"],
            blitz=row["BLITZ"],
            poor_pass=row["POOR_PASS"],
            avg_pass_10_yds=row["AVG_PASS_10_YDS"],
            avg_pass_20_yds=row["AVG_PASS_20_YDS"],
            avg_pass_30_yds=row["AVG_PASS_30_YDS"],
            avg_pass_40_yds=row["AVG_PASS_40_YDS"],
            avg_pass_50_yds=row["AVG_PASS_50_YDS"],
            avg_blitz=row["AVG_BLITZ"],
            avg_poor_pass=row["AVG_POOR_PASS"],
        )


@dataclasses.dataclass
class RushingStats:
    attempts: int
    touchdowns: int
    yards: int
    average_attempts: float
    average_touchdowns: float
    average_yards: float
    rush_attempts_20: int
    rush_attempts_10: int
    rush_attempts_5: int
    rush_percent_20: float
    rush_percent_10: float
    rush_percent_5: float
    yds_before_contact: int
    avg_yds_before_contact: float
    yds_after_contact: int
    avg_yds_after_contact: float
    broken_tackles: int
    tackle_loss: int
    tackle_loss_yds: int
    run_10_yds: int
    run_20_yds: int
    run_30_yds: int
    run_40_yds: int
    run_50_yds: int
    longest_run: int
    avg_broken_tackles: float
    avg_run_10_yds: float
    avg_run_20_yds: float
    avg_run_30_yds: float
    avg_run_40_yds: float
    avg_run_50_yds: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.attempts,
            self.touchdowns,
            self.yards,
            self.average_attempts,
            self.average_touchdowns,
            self.average_yards,
            self.rush_attempts_20,
            self.rush_attempts_10,
            self.rush_attempts_5,
            self.rush_percent_20,
            self.rush_percent_10,
            self.rush_percent_5,
            self.yds_before_contact,
            self.avg_yds_before_contact,
            self.yds_after_contact,
            self.avg_yds_after_contact,
            self.broken_tackles,
            self.tackle_loss,
            self.tackle_loss_yds,
            self.run_10_yds,
            self.run_20_yds,
            self.run_30_yds,
            self.run_40_yds,
            self.run_50_yds,
            self.longest_run,
            self.avg_broken_tackles,
            self.avg_run_10_yds,
            self.avg_run_20_yds,
            self.avg_run_30_yds,
            self.avg_run_40_yds,
            self.avg_run_50_yds,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Rushing Attempts",
            "Rushing Touchdowns",
            "Rushing Yards",
            "Average Rushing Attempts",
            "Average Rushing Touchdowns",
            "Average Rushing Yards",
            "Rush Attempts from 20",
            "Rush Attempts from 10",
            "Rush Attempts from 5",
            "Rush Percent from 20",
            "Rush Percent from 10",
            "Rush Percent from 5",
            "Yards Before Contact",
            "Avg Yards Before Contact",
            "Yards After Contact",
            "Avg Yards After Contact",
            "Broken Tackles",
            "Tackle for Loss",
            "Tackle for Loss Yards",
            "Runs 10+ Yards",
            "Runs 20+ Yards",
            "Runs 30+ Yards",
            "Runs 40+ Yards",
            "Runs 50+ Yards",
            "Longest Run",
            "Avg Broken Tackles",
            "Avg Runs 10+ Yards",
            "Avg Runs 20+ Yards",
            "Avg Runs 30+ Yards",
            "Avg Runs 40+ Yards",
            "Avg Runs 50+ Yards",
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
            rush_attempts_20=row["20_YD_ATT"],
            rush_attempts_10=row["10_YD_ATT"],
            rush_attempts_5=row["5_YD_ATT"],
            rush_percent_20=row["20_YD_%RUSH"],
            rush_percent_10=row["10_YD_%RUSH"],
            rush_percent_5=row["5_YD_%RUSH"],
            yds_before_contact=row["YDS_BEFORE_CONTACT"],
            avg_yds_before_contact=row["AVG_YDS_BEFORE_CONTACT"],
            yds_after_contact=row["YDS_AFTER_CONTACT"],
            avg_yds_after_contact=row["AVG_YDS_AFTER_CONTACT"],
            broken_tackles=row["BROKEN_TACKLES"],
            tackle_loss=row["TACKLE_LOSS"],
            tackle_loss_yds=row["TACKLE_LOSS_YDS"],
            run_10_yds=row["RUN_10_YDS"],
            run_20_yds=row["RUN_20_YDS"],
            run_30_yds=row["RUN_30_YDS"],
            run_40_yds=row["RUN_40_YDS"],
            run_50_yds=row["RUN_50_YDS"],
            longest_run=row["LONGEST_RUN"],
            avg_broken_tackles=row["AVG_BROKEN_TACKLES"],
            avg_run_10_yds=row["AVG_RUN_10_YDS"],
            avg_run_20_yds=row["AVG_RUN_20_YDS"],
            avg_run_30_yds=row["AVG_RUN_30_YDS"],
            avg_run_40_yds=row["AVG_RUN_40_YDS"],
            avg_run_50_yds=row["AVG_RUN_50_YDS"],
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
    targets_20: int
    targets_10: int
    targets_percent_20: float
    targets_percent_10: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.receptions,
            self.touchdowns,
            self.yards,
            self.targets,
            self.average_receptions,
            self.average_touchdowns,
            self.average_yards,
            self.average_targets,
            self.targets_20,
            self.targets_10,
            self.targets_percent_20,
            self.targets_percent_10,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Receptions",
            "Receiving Touchdowns",
            "Receiving Yards",
            "Targets",
            "Average Receptions",
            "Average Receiving Touchdowns",
            "Average Receiving Yards",
            "Average Targets",
            "Targets from 20",
            "Targets from 10",
            "Targets Percent from 20",
            "Targets Percent from 10",
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
            targets_20=row["20_YD_TGT"],
            targets_10=row["10_YD_TGT"],
            targets_percent_20=row["20_YD_%TGT"],
            targets_percent_10=row["10_YD_%TGT"],
        )


@dataclasses.dataclass
class AdvancedReceivingStats:
    yds_before_catch: int
    avg_yds_before_catch: float
    rec_air_yds: int
    avg_rec_air_yds: float
    yac: int
    avg_yac: float
    yacon: int
    avg_yacon: float
    tgt_share: float
    catchable: int
    drop: int
    rec_10_yds: int
    rec_20_yds: int
    rec_30_yds: int
    rec_40_yds: int
    rec_50_yds: int
    longest_rec: int
    avg_catchable: float
    avg_drop: float
    avg_rec_10_yds: float
    avg_rec_20_yds: float
    avg_rec_30_yds: float
    avg_rec_40_yds: float
    avg_rec_50_yds: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.yds_before_catch,
            self.avg_yds_before_catch,
            self.rec_air_yds,
            self.avg_rec_air_yds,
            self.yac,
            self.avg_yac,
            self.yacon,
            self.avg_yacon,
            self.tgt_share,
            self.catchable,
            self.drop,
            self.rec_10_yds,
            self.rec_20_yds,
            self.rec_30_yds,
            self.rec_40_yds,
            self.rec_50_yds,
            self.longest_rec,
            self.avg_catchable,
            self.avg_drop,
            self.avg_rec_10_yds,
            self.avg_rec_20_yds,
            self.avg_rec_30_yds,
            self.avg_rec_40_yds,
            self.avg_rec_50_yds,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Yards Before Catch",
            "Avg Yards Before Catch",
            "Receiving Air Yards",
            "Avg Receiving Air Yards",
            "Yards After Catch",
            "Avg Yards After Catch",
            "Yards After Contact",
            "Avg Yards After Contact",
            "Target Share %",
            "Catchable Passes",
            "Drops",
            "Receptions 10+ Yards",
            "Receptions 20+ Yards",
            "Receptions 30+ Yards",
            "Receptions 40+ Yards",
            "Receptions 50+ Yards",
            "Longest Reception",
            "Avg Catchable Passes",
            "Avg Drops",
            "Avg Receptions 10+ Yards",
            "Avg Receptions 20+ Yards",
            "Avg Receptions 30+ Yards",
            "Avg Receptions 40+ Yards",
            "Avg Receptions 50+ Yards",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> AdvancedReceivingStats:
        return AdvancedReceivingStats(
            yds_before_catch=row["YDS_BEFORE_CATCH"],
            avg_yds_before_catch=row["AVG_YDS_BEFORE_CATCH"],
            rec_air_yds=row["REC_AIR_YDS"],
            avg_rec_air_yds=row["AVG_REC_AIR_YDS"],
            yac=row["YAC"],
            avg_yac=row["AVG_YAC"],
            yacon=row["YACON"],
            avg_yacon=row["AVG_YACON"],
            tgt_share=row["TGT_SHARE"],
            catchable=row["CATCHABLE"],
            drop=row["DROP"],
            rec_10_yds=row["REC_10_YDS"],
            rec_20_yds=row["REC_20_YDS"],
            rec_30_yds=row["REC_30_YDS"],
            rec_40_yds=row["REC_40_YDS"],
            rec_50_yds=row["REC_50_YDS"],
            longest_rec=row["LONGEST_REC"],
            avg_catchable=row["AVG_CATCHABLE"],
            avg_drop=row["AVG_DROP"],
            avg_rec_10_yds=row["AVG_REC_10_YDS"],
            avg_rec_20_yds=row["AVG_REC_20_YDS"],
            avg_rec_30_yds=row["AVG_REC_30_YDS"],
            avg_rec_40_yds=row["AVG_REC_40_YDS"],
            avg_rec_50_yds=row["AVG_REC_50_YDS"],
        )


@dataclasses.dataclass
class TeamTargetShareStats:
    wr_tgt_share_pct: float
    rb_tgt_share_pct: float
    te_tgt_share_pct: float

    def get_values_as_list(self, position: str) -> typing.List[typing.Any]:
        position = position.upper()
        if position == "WR":
            return [self.wr_tgt_share_pct]
        elif position == "RB":
            return [self.rb_tgt_share_pct]
        elif position == "TE":
            return [self.te_tgt_share_pct]
        else:
            raise ValueError(f"Unknown position: {position}")

    @staticmethod
    def all_stat_labels(position: str) -> typing.List[str]:
        position = position.upper()
        if position == "WR":
            return ["WR Target Share %"]
        elif position == "RB":
            return ["RB Target Share %"]
        elif position == "TE":
            return ["TE Target Share %"]
        else:
            raise ValueError(f"Unknown position: {position}")

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> TeamTargetShareStats:
        return TeamTargetShareStats(
            wr_tgt_share_pct=row["TEAM_WR_TGT_SHARE_PCT"],
            rb_tgt_share_pct=row["TEAM_RB_TGT_SHARE_PCT"],
            te_tgt_share_pct=row["TEAM_TE_TGT_SHARE_PCT"],
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

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.blocked_kicks,
            self.touchdowns,
            self.fumble_recoveries,
            self.interceptions,
            self.points_against,
            self.return_touchdowns,
            self.sacks,
            self.safeties,
            self.average_blocked_kicks,
            self.average_touchdowns,
            self.average_fumble_recoveries,
            self.average_interceptions,
            self.average_points_against,
            self.average_return_touchdowns,
            self.average_sacks,
            self.average_safeties,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
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

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.field_goals_made,
            self.extra_points_made,
            self.extra_points_attempted,
            self.average_extra_points_made,
            self.average_extra_points_attempted,
            self.average_field_goals_made,
            self.fg_0_19,
            self.fg_20_29,
            self.fg_30_39,
            self.fg_40_49,
            self.fg_50_plus,
            self.fg_0_19_average,
            self.fg_20_29_average,
            self.fg_30_39_average,
            self.fg_40_49_average,
            self.fg_50_plus_average,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
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
            average_fgm = round(fgm / games, 2)
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
class SnapShareStats:
    snaps_per_game: float
    snap_pct: float
    util_pct: float
    pts_100_snap: float
    ppr_pts_100_snap: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.snaps_per_game,
            self.snap_pct,
            self.util_pct,
            self.pts_100_snap,
            self.ppr_pts_100_snap,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Snaps per Game",
            "Snap %",
            "Utilization %",
            "Points per 100 Snaps",
            "PPR Points per 100 Snaps",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> SnapShareStats:
        return SnapShareStats(
            snaps_per_game=row["SNAPS_PER_GAME"],
            snap_pct=row["SNAP_PCT"],
            util_pct=row["UTIL_PCT"],
            pts_100_snap=row["PTS_100_SNAP"],
            ppr_pts_100_snap=row["PPR_PTS_100_SNAP"],
        )


@dataclasses.dataclass
class PPRStats:
    boom: float
    bust: float
    starter: float
    fantasy_points: float
    average_fantasy_points: float
    average_rank: float
    best_rank: float
    worst_rank: float
    rank: float
    standard_deviation: float
    tier: float
    position_average_rank: float
    position_best_rank: float
    position_worst_rank: float
    position_rank: float
    position_tier: float
    position_std_dev: float
    adp: float

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.boom,
            self.bust,
            self.starter,
            self.fantasy_points,
            self.average_fantasy_points,
            self.average_rank,
            self.best_rank,
            self.worst_rank,
            self.rank,
            self.standard_deviation,
            self.tier,
            self.position_average_rank,
            self.position_best_rank,
            self.position_worst_rank,
            self.position_rank,
            self.position_tier,
            self.position_std_dev,
            self.adp,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Boom",
            "Bust",
            "Starter",
            "Fantasy Points",
            "Average Fantasy Points",
            "Average Rank",
            "Best Rank",
            "Worst Rank",
            "Rank",
            "Standard Deviation",
            "Tier",
            "Position Average Rank",
            "Position Best Rank",
            "Position Worst Rank",
            "Position Rank",
            "Position Tier",
            "Position Standard Deviation",
            "ADP",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> PPRStats:
        return PPRStats(
            boom=row["PPR_BOOM"],
            bust=row["PPR_BUST"],
            starter=row["PPR_STARTER"],
            fantasy_points=row["PPR_FAN PTS"],
            average_fantasy_points=row["PPR_AVG_FAN PTS"],
            average_rank=row["PPR_AVG_RK"],
            best_rank=row["PPR_BEST_RK"],
            worst_rank=row["PPR_WORST_RK"],
            rank=row["PPR_RK"],
            standard_deviation=row["PPR_STD.DEV_RK"],
            tier=row["PPR_TIERS"],
            position_average_rank=row["PPR_POS_AVG."],
            position_best_rank=row["PPR_POS_BEST"],
            position_worst_rank=row["PPR_POS_WORST"],
            position_rank=row["PPR_POS_RK"],
            position_tier=row["PPR_POS_TIERS"],
            position_std_dev=row["PPR_POS_STD.DEV"],
            adp=row["PPR_ADP"],
        )


@dataclasses.dataclass
class StandardStats(PPRStats):
    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> StandardStats:
        return StandardStats(
            boom=row["BOOM"],
            bust=row["BUST"],
            starter=row["STARTER"],
            fantasy_points=row["FAN PTS"],
            average_fantasy_points=row["AVG_FAN PTS"],
            average_rank=row["AVG_RK"],
            best_rank=row["BEST_RK"],
            worst_rank=row["WORST_RK"],
            rank=row["RK"],
            standard_deviation=row["STD.DEV_RK"],
            tier=row["TIERS"],
            position_average_rank=row["POS_AVG."],
            position_best_rank=row["POS_BEST"],
            position_worst_rank=row["POS_WORST"],
            position_rank=row["POS_RK"],
            position_tier=row["POS_TIERS"],
            position_std_dev=row["POS_STD.DEV"],
            adp=row["STANDARD_ADP"],
        )


@dataclasses.dataclass
class BasicInfo:
    name: str
    position: str
    team: str
    season_sos: float
    full_sos: float
    playoff_sos: float
    depth: int

    def get_values_as_list(self) -> typing.List[typing.Any]:
        return [
            self.name,
            self.position,
            self.team,
            self.season_sos,
            self.full_sos,
            self.playoff_sos,
            self.depth,
        ]

    @staticmethod
    def all_stat_labels() -> typing.List[str]:
        return [
            "Name",
            "Position",
            "Team",
            "Season SOS",
            "Full SOS",
            "Playoff SOS",
            "Depth",
        ]

    @staticmethod
    def from_csv_row(row: typing.Dict[str, typing.Any]) -> BasicInfo:
        info = BasicInfo(
            name=_clean_name(row["PLAYER NAME"]),
            position=row["POS"],
            team=row["TEAM"],
            season_sos=row["SEASON_SOS"],
            full_sos=row["FULL_SOS"],
            playoff_sos=row["PLAYOFF_SOS"],
            depth=row["DEPTH"],
        )
        if info.depth == 0:
            info.depth = 10
        return info


def _clean_name(name: str) -> str:
    # Currently names are all CAPS, so just make them title case where dashes count as spaces when doing the titling
    return name.title()


def _clean_dict(row: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    COLS_TO_SET_TO_500 = ["RK", "TIER", "STD.DEV"]
    for k, v in row.items():
        if isinstance(v, float) and math.isnan(v):
            if np.any([col in k for col in COLS_TO_SET_TO_500]):
                row[k] = 500
            else:
                row[k] = 0
    return row

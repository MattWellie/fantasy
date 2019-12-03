import pandas as pd
import numpy as np
import logging
from collections import defaultdict


"""
A quick script to read in fantasy scores and do some analysis of them
"""


def does_team_have_winning_record():
    """
    for this week, does this opposition team have a winning record?
    Requires a df which shows the teams who played each week
    :return:
    """
    pass


if __name__ == "__main__":

    logging.basicConfig(level=logging.WARNING)

    logging.debug("yaas queen")  # yes, logging is working

    # load all the scores
    score_df = pd.read_csv(open("score_frame.csv"), index_col="team_name")
    logging.debug(score_df)

    # how about those wins
    win_df = pd.read_csv(open("wins_frame.csv"), index_col="team_name")
    logging.debug(win_df)

    teams_real_wins = defaultdict(float)
    teams_sim_wins = defaultdict(float)
    team_scores = dict()

    # all team names - this is the index value
    teams = score_df.index.values
    logging.debug("teams:", list(map(str, teams)))

    # obtain the weeks in number form - columns must be called "week#" for this to work
    weeks = sorted(map(int, score_df.columns))
    logging.debug("weeks", list(map(str, weeks)))

    # iterate over teams, and for each one, pick up the scores for other teams only
    for team in teams:

        logging.info(f"now checking {team}")

        scores = score_df.loc[team]
        team_scores[team] = {
            "mean": np.mean(scores),
            "max": np.max(scores),
            "min": np.min(scores),
        }

        team_scores[team]["range"] = team_scores[team]["max"] - team_scores[team]["min"]

        # get all teams other than this one
        opposition = [x for x in teams if x != team]
        logging.debug(opposition)

        # full data frame for every team except this one
        opposition_df = score_df[~score_df.index.isin([team])]

        # iterate over weeks
        for week in weeks:

            week_index = str(week)

            # for this week and team, what was the score?
            my_team_score = score_df.loc[[team], week_index]

            # apply this score as a challenge to all scores in this week - this returns a series. Replace the opposition
            # dataframe slice for this week with the Boolean result - causes a warning
            opposition_df[week_index] = opposition_df.loc[:, week_index].apply(
                lambda x: x < my_team_score
            )

            # can't get my head around the warning free way to do this...
            # opposition_df[:, [f'week{week}']] = weekly_scores.apply(lambda x: x < my_team_score)  # nope
            # opposition_df.loc[:, (f'week{week}')] = weekly_scores.apply(lambda x: x < my_team_score)  # nope

            logging.debug(opposition_df)

        logging.debug(opposition_df)

        total_contests = opposition_df.size
        logging.info(f"contests, {total_contests}")
        total_wins = np.sum(np.sum(opposition_df))
        logging.info(f"total_wins: {total_wins}")

        # how many actual wins? - applied row-wise to count number of 1/True for this team across season (so far)
        real_wins = int(np.sum(win_df.loc[team, :]))

        sim_ratio = total_wins / total_contests
        real_ratio = real_wins / len(weeks)

        teams_real_wins[team] = real_ratio
        teams_sim_wins[team] = sim_ratio

        # some output of first check
        print(
            f"Team: {team}\t"
            f"Real Wins: {real_wins}\t"
            f"Real Ratio: {real_ratio:.2f}\t"
            f"SimWins: {total_wins}\t"
            f"SimLosses: {total_contests - total_wins}\t"
            f"SimRatio: {sim_ratio:.2f}"
        )

    print(teams_real_wins)
    print(teams_sim_wins)

    team_score_df = pd.DataFrame(team_scores)
    team_score_df.to_csv('team_scores.csv')
    print(team_score_df)
    # print(team_scores)

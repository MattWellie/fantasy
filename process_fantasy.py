import pandas as pd
import numpy as np
import logging


"""
A quick script to read in fantasy scores and do some analysis of them
"""

if __name__ == "__main__":

    logging.basicConfig(level=logging.WARNING)

    logging.debug('yaas queen')  # yes, logging is working

    # load all the scores
    score_df = pd.read_csv(open('score_frame.csv'), index_col='team_name')
    logging.debug(score_df)

    # how about those wins
    win_df = pd.read_csv(open('wins_frame.csv'), index_col='team_name')
    logging.debug(win_df)

    # all team names - this is the index value
    teams = score_df.index.values
    logging.debug('teams:', list(map(str, teams)))

    # obtain the weeks in number form - columns must be called "week#" for this to work
    weeks = sorted([int(x.replace('week', '')) for x in score_df.columns])
    logging.debug('weeks', list(map(str, weeks)))

    # iterate over teams, and for each one, pick up the scores for other teams only
    for team in teams:

        logging.info(f'now checking {team}')

        # get all teams other than this one
        opposition = [x for x in teams if x != team]
        logging.debug(opposition)

        # full data frame for every team except this one
        opposition_df = score_df[~score_df.index.isin([team])]

        # iterate over weeks
        for week in weeks:

            # for this week and team, what was the score?
            my_team_score = score_df.loc[[team], f'week{week}']

            # apply this score as a challenge to all scores in this week - this returns a series. Replace the opposition
            # dataframe slice for this week with the Boolean result - causes a warning
            opposition_df[f'week{week}'] = opposition_df.loc[:, f'week{week}'].apply(lambda x: x < my_team_score)

            # can't get my head around the warning free way to do this...
            # opposition_df[:, [f'week{week}']] = weekly_scores.apply(lambda x: x < my_team_score)  # nope
            # opposition_df.loc[:, (f'week{week}')] = weekly_scores.apply(lambda x: x < my_team_score)  # nope

            logging.debug(opposition_df)

        logging.debug(opposition_df)

        total_contests = opposition_df.size
        logging.info(f'contests, {total_contests}')
        total_wins = np.sum(np.sum(opposition_df))
        logging.info(f'total_wins: {total_wins}')

        # how many actual wins? - applied row-wise to count number of 1/True for this team across season (so far)
        real_wins = int(np.sum(win_df.loc[team, :]))

        # some output of first check
        print(f'Team: {team}\t'
              f'Real Wins: {real_wins}\t'
              f'Real Ratio: {real_wins / len(weeks):.2f}\t'
              f'SimWins: {total_wins}\t'
              f'SimLosses: {total_contests - total_wins}\t'
              f'SimRatio: {total_wins / total_contests:.2f}')

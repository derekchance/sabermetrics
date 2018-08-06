# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np


games = 14.5
teams = 8
total_games = games * teams

stats_df = pd.read_excel('C:/labl_stats.xlsx')
guts_df = pd.read_csv('C:/Users/derek/Sabermetrics/xWAR/fg_guts.csv')
rpg_df = pd.read_excel('C:/rpg.xlsx')
rpg_df.set_index('Runs per game', inplace=True)

rpg_df.rename(columns={'Single': '1B',
                       'Double': '2B',
                       'Triple': '3B',
                       'Walk': 'BB'}, inplace=True)

rpg = stats_df.R.sum() / total_games
weights = rpg_df.loc[7]
weights -= weights.loc['Out']

stats_df['1B'] = stats_df['H'] - stats_df['2B'] - stats_df['3B'] - stats_df['HR']
stats_df['OPS'] = stats_df['OBP'] + stats_df['SLG']
stats_df['PA'] = stats_df['AB'] + stats_df['BB'] + stats_df['HBP'] + stats_df['SF']

w_col = ['1B', '2B', '3B', 'HR', 'BB', 'HBP']

totals_df = stats_df.sum().loc['AVG':]
totals_df['AVG'] = totals_df.H / totals_df.AB
totals_df['OBP'] = (totals_df.H + totals_df.BB + totals_df.HBP) / totals_df.PA
totals_df['SLG'] = totals_df.TB / totals_df.AB
totals_df['OPS'] = totals_df.OBP + totals_df.SLG

stats_df['wOBA'] = stats_df[w_col].dot(weights[w_col]) / stats_df.PA
totals_df['wOBA'] = totals_df[w_col].dot(weights[w_col]) / totals_df.PA

wOBA_scale = 1.1
RtW = 13

stats_df['wRAA'] = ((stats_df.wOBA - totals_df.wOBA)/wOBA_scale) * stats_df.PA
stats_df['wRC+'] = (stats_df.wOBA / totals_df.wOBA * 100).astype(int)
stats_df['rep_R'] = 20 * (stats_df.PA / 600)
stats_df['oRAR'] = stats_df.wRAA + stats_df.rep_R
stats_df['oWAR'] = stats_df.oRAR / RtW
stats_df.sort_values('oWAR', ascending=False, inplace=True)

ms_df = stats_df.set_index('Team').loc['South LA Mariners'][['Name',
                                                             'GP',
                                                             'PA',
                                                             'H',
                                                             '2B',
                                                             '3B',
                                                             'HR',
                                                             'RBI',
                                                             'SB',
                                                             'AVG',
                                                             'OBP',
                                                             'OPS',
                                                             'wOBA',
                                                             'wRC+',
                                                             'oWAR']]

ms_df.sort_values('oWAR', ascending=False, inplace=True)




# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from labl.scraper import get_player_stats, get_runs_per_game
import sabermetrics.sabermetrics as saber


stats_df = get_player_stats()
stats_df['1B'] = saber.singles(stats_df)
stats_df['OPS'] = saber.ops(stats_df)
stats_df['PA'] = saber.pa(stats_df)
stats_df['wOBA'] = saber.woba(stats_df, league='labl')
stats_df['wRAA'] = saber.wraa(stats_df, league='labl')
stats_df['wRC'] = saber.wrc(stats_df, league='labl')
stats_df['wRC+'] = saber.wrc_plus(stats_df, league='labl')
stats_df['oRAR'] = saber.off_rar(stats_df)
stats_df['oWAR'] = saber.off_war(stats_df, league='labl')

stats_df.sort_values('oWAR', ascending=False, inplace=True)

ms_df = stats_df.loc['South LA Mariners'][['Name',
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
                                           'oRAR',
                                           'oWAR']]

ms_df.sort_values('oWAR', ascending=False, inplace=True)
ms_df.to_excel('out/ms_leaderboard.xlsx')
stats_df.reset_index().to_excel('out/labl_leaderboard.xlsx')

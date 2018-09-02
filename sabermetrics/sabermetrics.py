# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 18:21:37 2018

@author: derek
"""

import pandas as pd
import numpy as np
from labl.scraper import get_runs_per_game


def singles(df):
    '''
    Returns series with number of Singles
    '''

    return df['H'] - df['2B'] - df['3B'] - df['HR']


def ops(df):
    '''
    Returns series with OPS
    '''
    return df['OBP'] + df['SLG']


def pa(df):
    '''
    Returns series with number of Plate Appearances
    '''
    return df['AB'] + df['BB'] + df['HBP'] + df['SF']


def batting_avg(df):
    '''
    Returns series with Batting Average
    '''
    return df['H'] / df['AB']


def obp(df):
    '''
    Returns Series with On-Base Percentage
    '''
    return (df['H'] + df['BB'] + df['HBP']) / df['PA']


def slg(df):
    '''
    Returns Series with Slugging Percentage
    '''
    return df['TB'] / df['AB']


def run_weights(runs):
    '''
    Returns Series of event run weights based on run environment
    '''
    df = pd.read_pickle('bin/run_per_game_weights.pkl')
    df.rename(columns={'Single': '1B',
                       'Double': '2B',
                       'Triple': '3B',
                       'Walk': 'BB'}, inplace=True)
    df['idx'] = df.index.astype(float)
    df.set_index('idx', inplace=True)
    df = df.T
    df[runs] = np.nan
    df = df.T.sort_index()
    df.interpolate(method='index', inplace=True)
    s = df.loc[runs]
    s -= s.loc['Out']
    return s


def woba(df, league):
    '''
    Returns series with wOBA
    '''
    w_col = ['1B', '2B', '3B', 'HR', 'BB', 'HBP']

    if league == 'labl':
        runs = get_runs_per_game()
        weights = run_weights(runs)

    return df[w_col].dot(weights[w_col]) / df.PA


def wraa(df, league):
    '''
    Returns series with wRAA
    '''
    if league == 'labl':
        woba_scale = 1.1
    sum_df = df.sum()
    sum_df['wOBA'] = woba(sum_df, league)
    try:
        return ((df['wOBA'] - sum_df['wOBA'])/woba_scale) * df['PA']
    except:
        return ((woba(df, league) - sum_df['wOBA'])/woba_scale) * df['PA']


def wrc(df, league):
    '''
    Returns series with wRC
    '''
    if league == 'labl':
        woba_scale = 1.1
        rpg = get_runs_per_game()
    sum_df = df.sum()
    sum_df['wOBA'] = woba(sum_df, league)
    rpa = sum_df['R'] / sum_df['PA']
    try:
        return (((df['wOBA'] - sum_df['wOBA'])/woba_scale) + rpa) * df['PA']
    except:
        return (((woba(df, league) - sum_df['wOBA'])/woba_scale) + rpa) * df['PA']


def wrc_plus(df, league):
    '''
    Returns series with wRC+
    '''
    sum_df = df.sum()
    sum_df['wOBA'] = woba(sum_df, league)
    rpa = sum_df['R'] / sum_df['PA']
    try:
        numerator = (df['wRAA'] / df['PA']) + rpa
    except:
        numerator = (wraa(df, league) / df['PA']) + rpa
    try:
        denominator = sum_df['wRC'] / sum_df['PA']
    except:
        denominator = (wrc(sum_df, league).sum() / sum_df['PA'])
    return (numerator / denominator) * 100.0


def off_rar(df):
    '''
    Returns series with oRAR
    '''
    replacement = 20.0 * (df['PA'] / 600.0)
    try:
        return df['wRAA'] + replacement
    except:
        return wraa(df, 'labl') + replacement


def off_war(df, league):
    '''
    Returns series with oWAR
    '''
    if league == 'labl':
        rtw = 13
    try:
        return df['oRAR'] / rtw
    except:
        return off_rar(df) / rtw

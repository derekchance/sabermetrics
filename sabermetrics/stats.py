# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 18:21:37 2018

@author: derek
"""

import pandas as pd


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
    df['AB'] + df['BB'] + df['HBP'] + df['SF']


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
    df['idx'] = df.index.astype(float)
    df.set_index('idx', inplace=True)
    df = df.T
    df[runs] = np.nan
    df = df.T.sort_index()
    df.interpolate(method='index', inplace=True)
    s = df.loc[runs]
    s -= s.loc['Out']
    return s

df['wOBA'] = df[w_col].dot(weights[w_col]) / df.PA
df['wOBA'] = df[w_col].dot(weights[w_col]) / df.PA
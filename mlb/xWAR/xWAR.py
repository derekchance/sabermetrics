# -*- coding: utf-8 -*-
"""
Created on Sun May  6 19:20:59 2018

@author: Derek
"""

import pandas as pd
import numpy as np
import pybaseball as pb
import requests
import io
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import binom

# %%

nl_teams = ['Braves',
            'Dodgers',
            'Nationals',
            'Diamondbacks',
            'Cubs',
            'Pirates',
            'Cardinals',
            'Giants',
            'Mets',
            'Brewers',
            'Phillies',
            'Reds',
            'Padres',
            'Rockies',
            'Marlins',
            ]

comb_fields = ['player_id',
               'player_name',
               'Team',
               'League',
               'Season',
               'xwoba',
               'PA',
               'R',
               'wRAA',
               'wRC',
               'Bat',
               'Fld',
               'Rep',
               'Pos',
               'RAR',
               'WAR',
               'Spd',
               'wRC+']


# %%

url = 'https://baseballsavant.mlb.com/statcast_search/csv?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_pas=150#results'
s = requests.get(url).content
xwOBA_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
#xwOBA_df = pd.read_csv('xWAR/savant_data_xwOBA_20180506.csv')
fg_df = pb.batting_stats(2018)
pf_df = pd.read_csv('mlb/xWAR/park_factors.csv', usecols=['Team', 'Basic'])
guts_df = pd.read_csv('mlb/xWAR/fg_guts.csv', usecols=['Season', 'wOBA', 'wOBAScale', 'R/PA', 'R/W'])
fg_df['League'] = np.where(fg_df.Team.isin(nl_teams), 'NL', 'AL')
pf_df['dec_pf'] = pf_df.Basic / 100
guts_df.rename(columns={'wOBA': 'lg_wOBA', 'wOBAScale': 'wOBA_scale'}, inplace=True)

# %%

df = xwOBA_df.merge(fg_df, left_on='player_name', right_on='Name')[comb_fields]
df = df.merge(pf_df, how='left', on='Team')
df = df.merge(guts_df, on='Season')

# %%

al_r = df[df.League == 'AL'].wRC.sum() / df[df.League == 'AL'].PA.sum()
nl_r = df[df.League == 'NL'].wRC.sum() / df[df.League == 'NL'].PA.sum()
df['lg_adj'] = np.where(df.League == 'NL', nl_r, al_r)

# %%

df['xwRAA'] = df.PA * (df['xwoba'] - df['lg_wOBA'])/df['wOBA_scale']
df['park_runs'] = (df['R/PA'] - (df['dec_pf']*df['R/PA']))*df['PA']
df['league_runs'] = (df['R/PA'] - df['lg_adj'])*df['PA']
df['xBat'] = df['xwRAA'] + df['park_runs'] + df['league_runs']
df['xRAR'] = df['RAR'] - df['Bat'] +df['xBat']
df['xWAR'] = df['xRAR'] / df['R/W']

# %%

plt.figure(figsize=(14,10))
ax = sns.regplot('WAR', 'xWAR', data=df, truncate=True)
plt.title('xWAR vs WAR (Min. 150 PAs)')


# %%

def_df = pd.read_csv('mlb/xWAR/fg_2017_defense.csv')
plt.figure(figsize=(14,10))
def_ax = sns.regplot('DRS', 'UZR', data=def_df, truncate=True)
plt.title('UZR vs DRS - 2017 (Qual. Players)')
plt.axhline(y=0)
plt.axvline(x=0)


# %%

uzr = def_df['UZR'].dropna()
drs = def_df['DRS'].dropna()

plt.figure(figsize=(14,10))
dist_ax = sns.distplot(uzr, label='UZR')
sns.distplot(drs, ax=dist_ax, label='DRS', axlabel='+/- (runs)')
dist_ax.legend()
plt.title('+/- run distribution (UZR and DRS)')

# %%

plt.figure(figsize=(14,10))
dist = binom(32, (1/32))
x = np.arange(-1,10)
plt.plot(x, dist.pmf(x))

plt.title('Cleveland Browns - True Win Total Probability')

# %%

lb_df = df[['player_name','xWAR', 'WAR']].sort_values(by='xWAR', ascending=False)
lb_df['Diff'] = lb_df.xWAR - lb_df.WAR

#%%

plt.figure(figsize=(14,10))
dist_ax = sns.distplot(df['xWAR'], label='xWAR')
sns.distplot(df['WAR'], ax=dist_ax, label='WAR', axlabel='Wins')
dist_ax.legend()
plt.title('Win Distribution')
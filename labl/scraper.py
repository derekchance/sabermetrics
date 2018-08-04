# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:25:40 2018

@author: derek
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_df(soup):
    '''
    Converts soup object from labl stats page into a pandas dataframe
    '''
    table = []
    cols = []
    
    for th in soup.find('tr').find_all('th')[1:]:
        cols.append(th.find('a').contents[0])
    for tr in soup.find_all('tr')[2: len(soup.find_all('tr'))-1]:
        tds = []
        for td in tr.find_all('td')[1:]:
            try:
                tds.append(td.find('a').contents[0])
            except:
                try: 
                    tds.append(td.contents[0])
                except: tds.append(0)
        table.append(tds)
        
    df = pd.DataFrame(table,
                      columns=cols)
    
    return df


def get_teams():
    '''
    returns list of teams with team_id as keys
    '''    
    url = 'https://www.leaguelineup.com/standings_baseball.asp?url=labaseballleague&divisionid=816248&listtype=4'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    team_dict = {}
    
    for tr in soup.find_all('tr')[3: len(soup.find_all('tr'))-1]:
        team_name = tr.find('td').find('a').contents[0]
        team_id = tr.find('td').find('a').get('href').split('=')[2]
        team_dict[team_id] = team_name
    return team_dict



def get_player_stats():
    '''
    Returns stats for all rostered labl National division players
    '''
    team_dict = get_teams()
    dfs = []
    
    for team_id in team_dict:
        url = f'https://www.leaguelineup.com/teams_baseball.asp?url=labaseballleague&Teamid={team_id}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dfs.append(scrape_df(soup))
    
    return pd.concat(dfs, keys=list(team_dict.values()))
        
        
###########################################################################
## The following code utilizes StatsBomb Open Data repository on Git Hub ##
## in order to scrape and maniuplate soccer passing, dribbling, and shot ##
## data for various players on FC Barcelona in La Liga                   ##
## https://github.com/statsbomb/open-data                                ##
###########################################################################
import statsbomb as sb
import pandas as pd
import numpy as np

#update following variables to toggle between data
player = 'Lionel Andrés Messi Cuccittini'
team, event = 'Barcelona', '11'
    
def getMatchIds(id):
    #get match data for single season, filter season in main()
    matches = sb.Matches(event_id = event, season_id = str(id))
    df = matches.get_dataframe()
    
    #extract match_id from match data
    match_ids = df['match_id']
    match_ids = np.array(match_ids)
    
    return match_ids

def getDataFrame(match_ids, type, result):
    #scrape event data using match_ids
    for id in match_ids:
        events = sb.Events(event_id = str(id))
        df = events.get_dataframe(event_type = type)
        result.append(df)

    return pd.concat(result)
    
def getShotData(match_ids):    
    df = getDataFrame(match_ids, 'shot', [])
    
    #filter data by team and player
    is_Barcelona = df['possession_team'] == team
    df2 = df[is_Barcelona]

    is_player = df2['player'] == player
    df3 = df2[is_player]

    #extract shot locations from data 
    df4 = df3[['outcome', 'start_location_x', 'start_location_y']]
    df4.to_excel("shot_data.xlsx")
    
def getPassData(match_ids):
    df = getDataFrame(match_ids, 'pass', [])
    
    #filter data by team and player
    is_Barcelona = df['possession_team'] == team
    df2 = df[is_Barcelona]
    
    #filter data by player passing
    is_player = df2['player'] == player
    df3 = df2[is_player]
    df3.to_excel("pass_made.xlsx")
    
    #filter data by player receiving
    is_Suarez = df2['recipient'] == player
    df4 = df2[is_Suarez]
    df4.to_excel("pass_received.xlsx")

def getDribbleData(match_ids):
    df = getDataFrame(match_ids, 'dribble', [])
   
    #filter data by team and player
    is_Barcelona = df['possession_team'] == team
    df2 = df[is_Barcelona]
    
    is_player = df2['player'] == player
    df3 = df2[is_player]

    #extract shot locations from data 
    df4 = df3[['outcome', 'start_location_x', 'start_location_y']]
    df4.to_excel("dribble_data.xlsx")
    
def main():
    seasons = {37:'2004/2005',
               38:'2005/2006',
               39:'2006/2007',
               40:'2007/2008',
               41:'2008/2009',
               21:'2009/2010',
               22:'2010/2011',
               23:'2011/2012',
               24:'2012/2013',
               25:'2013/2014',
               26:'2014/2015',
               2:'2016/2017',
               1:'2017/2018',
               4:'2018/2019'}
    
    #use keys in seasons to pull data for that season (default is 4)
    match_ids = getMatchIds(4)
    
    #use match_ids to pull shot, pass, and dribbling data
    getShotData(match_ids)
    getPassData(match_ids)
    getDribbleData(match_ids)
    
main()
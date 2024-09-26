import pandas as pd
import requests
import json
from credentials import x_auth_token


#Functions
def pretty_print_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

#id da competição brasileirao = 2013

def request_footbal_data(request_url):

    #headers = {"X-Auth-Token": "YOUR_API_KEY"}  # Replace with your actual API key

    response = requests.get(url = request_url
                            ,headers = {'X-Auth-Token' : x_auth_token}
                            ,timeout = 10)

    if response.status_code == 200:
        data = response.json()
        #pretty_print_json(data)
        #print("Retrieved data succesfully")
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")



def season_games():

    matches = 'https://api.football-data.org/v4/competitions/2013/matches'
    
    all_matches = request_footbal_data(request_url = matches)
    
    match_list = []
    
    for i in all_matches['matches']:
        match_list.append({'matchday': i['matchday']
                        ,'match': i['id']
                        ,'homeTeam' : i['homeTeam']['shortName']
                        ,'homeTeamShort' : i['homeTeam']['tla']
                        ,'homeTeamSymbol' : i['homeTeam']['crest']
                        ,'homeTeamScore' : i['score']['fullTime']['home']
                        ,'awayTeam' : i['awayTeam']['shortName']
                        ,'awayTeamShort' : i['awayTeam']['tla']
                        ,'awayTeamSymbol' : i['awayTeam']['crest']
                        ,'awayTeamScore' : i['score']['fullTime']['away']
                        ,'result' : i['score']['winner']
                        ,'score' : i['score']['fullTime']
                        }
                    )
    
    brasileirao_teams = ['Fluminense'
                         ,'Mineiro'
                         ,'Grêmio'
                         ,'Paranaense'
                         ,'Palmeiras'
                         ,'Botafogo'
                         ,'Cruzeiro'
                         ,'São Paulo'
                         ,'Bahia'
                         ,'Corinthians'
                         ,'Vasco da Gama'
                         ,'Vitória'
                         ,'Flamengo'
                         ,'Fortaleza'
                         ,'AC Goianiense'
                         ,'Criciúma'
                         ,'Juventude'
                         ,'Bragantino'
                         ,'Cuiabá EC'
                         ,'Internacional']
    
    season_performance = []

    for team in brasileirao_teams:
    
        win = 0
        loss = 0
        draw = 0
        matches = 0
        points = 0
        team_symbol = ''
            
        for match in match_list:
            
            if match['homeTeam'] == team and match['result'] == 'HOME_TEAM':
                win += 1
                team_symbol = match['homeTeamSymbol']
            
            elif match['homeTeam'] == team and match['result'] == 'AWAY_TEAM':
                loss += 1
                team_symbol = match['homeTeamSymbol']
            
            elif match['homeTeam'] == team and match['result'] == 'DRAW':
                draw += 1
                team_symbol = match['homeTeamSymbol']
            
            elif match['awayTeam'] == team and match['result'] == 'AWAY_TEAM':
                win += 1

            elif match['awayTeam'] == team and match['result'] == 'HOME_TEAM':
                loss += 1
            
            elif match['awayTeam'] == team and match['result'] == 'DRAW':
                draw += 1
        

        matches = win + loss + draw
        points = (win * 3) + (draw * 1)

        season_performance.append({'team_name' : team
                                ,'win' : win
                                ,'loss' : loss
                                ,'draw' : draw 
                                ,'matches' : matches
                                ,'points' : points
                                ,'team_symbol' : team_symbol
                                })
        
    
    season_performance_sorted = sorted(season_performance, key = lambda d: d['points'], reverse = True)
    return season_performance_sorted
#imports
import pandas as pd
import requests
import json

#pretty_print function
def pretty_print_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

#request_data function
def request_data(url,querystring=None):

    headers = {
        "x-rapidapi-key": "abeaab9485msh1f659a81b5a21fbp1793edjsn99032cb17312",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        pretty_print_json(data)
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

#calculate_season_points function
def calculate_season_points(df):
    # Create a dictionary to keep track of team points
    team_points = {}
    
    # Create new columns for points
    df['home_points'] = 0
    df['away_points'] = 0
    df['home_cumulative_points'] = 0
    df['away_cumulative_points'] = 0
    
    # Iterate through matches chronologically
    for index, row in df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        
        # Initialize teams in dictionary if not present
        if home_team not in team_points:
            team_points[home_team] = 0
        if away_team not in team_points:
            team_points[away_team] = 0
        
        # Calculate points for current match
        if row['home_win']==True:
            points_home = 3
            points_away = 0
        elif row['away_win']==True:
            points_home = 0
            points_away = 3
        else:  # Draw
            points_home = 1
            points_away = 1
        
        # Update team points
        team_points[home_team] += points_home
        team_points[away_team] += points_away
        
        # Store points for current match
        df.at[index, 'home_points'] = points_home
        df.at[index, 'away_points'] = points_away
        
        # Store cumulative points
        df.at[index, 'home_cumulative_points'] = team_points[home_team]
        df.at[index, 'away_cumulative_points'] = team_points[away_team]
    
    return df.reset_index()

#calculate_wins_draws_losses function
def calculate_wins_draws_losses(df):
    # Create a dictionary to keep track of team points
    team_wins = {}
    team_draws = {}
    team_losses = {}
    
    # Create new columns for wins,draws,losses
    df['home_wins'] = 0
    df['home_draws'] = 0
    df['home_losses'] = 0
    
    df['away_wins'] = 0
    df['away_draws'] = 0
    df['away_losses'] = 0

    df['home_cumulative_wins'] = 0
    df['home_cumulative_draws'] = 0
    df['home_cumulative_losses'] = 0

    df['away_cumulative_wins'] = 0
    df['away_cumulative_draws'] = 0
    df['away_cumulative_losses'] = 0

    # Iterate through matches chronologically
    for index, row in df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        
        # Initialize teams in dictionary if not present
        if home_team not in team_wins:
            team_wins[home_team] = 0
        if away_team not in team_wins:
            team_wins[away_team] = 0

        if home_team not in team_draws:
            team_draws[home_team] = 0
        if away_team not in team_draws:
            team_draws[away_team] = 0

        if home_team not in team_losses:
            team_losses[home_team] = 0
        if away_team not in team_losses:
            team_losses[away_team] = 0
        
        
        # Calculate points for current match
        if row['home_win']==True:
            team_wins[home_team] += 1
            team_losses[away_team] += 1
            
            df.at[index, 'home_wins'] = 1
            df.at[index, 'away_wins'] = 0
            
            df.at[index, 'home_cumulative_wins'] = team_wins[home_team]
            df.at[index, 'away_cumulative_wins'] = team_wins[away_team]

            df.at[index, 'home_cumulative_draws'] = team_draws[home_team]
            df.at[index, 'away_cumulative_draws'] = team_draws[away_team]

            df.at[index, 'home_cumulative_losses'] = team_losses[home_team]
            df.at[index, 'away_cumulative_losses'] = team_losses[away_team]

        elif row['away_win']==True:
            team_wins[away_team] += 1
            team_losses[home_team] +=1
            
            df.at[index, 'home_wins'] = 0 
            df.at[index, 'away_wins'] = 1
            
            df.at[index, 'home_cumulative_wins'] = team_wins[home_team]
            df.at[index, 'away_cumulative_wins'] = team_wins[away_team]

            df.at[index, 'home_cumulative_draws'] = team_draws[home_team]
            df.at[index, 'away_cumulative_draws'] = team_draws[away_team]

            df.at[index, 'home_cumulative_losses'] = team_losses[home_team]
            df.at[index, 'away_cumulative_losses'] = team_losses[away_team]

        else:  # Draw
            team_draws[home_team] += 1
            team_draws[away_team] += 1
            
            df.at[index, 'home_draws'] = 1
            df.at[index, 'away_draws'] = 1

            df.at[index, 'home_cumulative_wins'] = team_wins[home_team]
            df.at[index, 'away_cumulative_wins'] = team_wins[away_team]

            df.at[index, 'home_cumulative_draws'] = team_draws[home_team]
            df.at[index, 'away_cumulative_draws'] = team_draws[away_team]

            df.at[index, 'home_cumulative_losses'] = team_losses[home_team]
            df.at[index, 'away_cumulative_losses'] = team_losses[away_team]
        
    
    return df






# packages
import requests
from flask import Flask, jsonify
from flask_cors import CORS

# functions
from positions.goalkeeper import calculate_rating as goalkeeper_rating
from positions.defender import calculate_rating as defender_rating
from positions.midfielder import calculate_rating as midfielder_rating
from positions.forward import calculate_rating as forward_rating
from helper import compute_stats_min_max
from helper import calculate_team_data

# initialize Flask app as the backend
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) 

# fetch data from the official Fantasy Premier League (FPL) API
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/")
# converts data into JSON
d = data.json()  
f = fixtures.json()

players = d["elements"] # all the players from the API response 


team_data = calculate_team_data(d, f) # calculating team specific data, for later use

# seperate players by position, for more efficient stat calculations 
# goalkeepers
goalkeepers = [player for player in players if player["element_type"] == 1]
stats_min_max_gk = compute_stats_min_max(goalkeepers, team_data)
# defenders
defenders = [player for player in players if player["element_type"] == 2]
stats_min_max_def = compute_stats_min_max(defenders, team_data)
# midfielders
midfielders = [player for player in players if player["element_type"] == 3]
stats_min_max_mid = compute_stats_min_max(midfielders, team_data)
# forwards
forwards = [player for player in players if player["element_type"] == 4]
stats_min_max_fwd = compute_stats_min_max(forwards, team_data)

player_ratings = {}
for player in players: # loop through all the players and giving each one a rating
    position = player["element_type"] 
    team_code = player["team_code"] 
    team = team_data[team_code] # fetch precomputed team specific data from the player's team
    
    # splitting into specific position, for utilizing the appropriate rating calculations
    if position == 1:
        rating = goalkeeper_rating(player, stats_min_max_gk, team)
    elif position == 2:
        rating = defender_rating(player, stats_min_max_def, team)
    elif position == 3:
        rating = midfielder_rating(player, stats_min_max_mid, team)
    elif position == 4:
        rating = forward_rating(player, stats_min_max_fwd, team)

    chance_of_playing = player.get("chance_of_playing_next_round", None)
    is_starting = chance_of_playing == 100 # True or False depending on if the player start or not
        
    if rating > 1: 
        player_ratings[player["id"]] = {"name": player["web_name"] , "rating": int(rating), "position": player["element_type"], "is_starting": is_starting}

# storing player ratings based on positions
goalkeeper_ratings = {}
defender_ratings = {}
midfielder_ratings = {}
forward_ratings = {}

# map position codes to specific rating dictionaries
position_map = {
    1: goalkeeper_ratings, 
    2: defender_ratings,
    3: midfielder_ratings,
    4: forward_ratings
}

# storing the best player ratings based on positions
good_goalkeepers = {}
good_defenders = {}
good_midfielders = {}
good_forwards = {}

# populate the rating dictionaries
for player_id, info in player_ratings.items():
    position = info["position"]
    rating = info["rating"]
    
    # add player to the appropriate position dictionary using their ID
    position_map[position][player_id] = {"name": info["name"], "rating": rating}

# print sorted by position and their ratings
for position_name, position_dict in [("goalkeepers", goalkeeper_ratings),
                               ("defenders", defender_ratings), 
                               ("midfielders", midfielder_ratings), 
                               ("forwards", forward_ratings)]:
    print(f"\nthe best {position_name}")
    # sort players by rating and print their name and rating
    for player_id, player_info in sorted(position_dict.items(), key=lambda x: x[1]["rating"], reverse=True):
        print(f"ID {player_id}: {player_info['name']} - Rating: {player_info['rating']}")
        
        # add to the position-specific dictionaries
        if position_name == "goalkeepers":
            good_goalkeepers[player_id] = player_info
        elif position_name == "defenders":
            good_defenders[player_id] = player_info
        elif position_name == "midfielders":
            good_midfielders[player_id] = player_info
        elif position_name == "forwards":
            good_forwards[player_id] = player_info
    
# define API endpoints for retrieving specific positions

@app.route('/api/players/goalkeepers')
def get_goalkeepers():
    return jsonify(good_goalkeepers)

@app.route('/api/players/defenders')
def get_defenders():
    return jsonify(good_defenders)

@app.route('/api/players/midfielders')
def get_midfielders():
    return jsonify(good_midfielders)

@app.route('/api/players/forwards')
def get_forwards():
    return jsonify(good_forwards)

# start the flask app if this script is executed directly 
if __name__ == "__main__":
    app.run(debug=True)
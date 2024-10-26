import requests
from positions.goalkeeper import calculate_rating as goalkeeper_rating
from positions.defender import calculate_rating as defender_rating
from positions.midfielder import calculate_rating as midfielder_rating
from positions.forward import calculate_rating as forward_rating
from helper import compute_stats_min_max

# pulling the data from api end point
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
d = data.json() 

players = d["elements"]
player_ratings = {}
for player in players:
    position = player["element_type"]
    stats_min_max = compute_stats_min_max(players, position)
    # splitting into specific position
    if position == 1:
        rating = goalkeeper_rating(player, stats_min_max)
    elif position == 2:
        rating = defender_rating(player, stats_min_max)
    elif position == 3:
        rating = midfielder_rating(player, stats_min_max)
    elif position == 4:
        rating = forward_rating(player, stats_min_max)
    
    name = player["web_name"]
    if rating > 1: # storing all good expected players
        player_ratings[name] = {"rating": rating, "position": player["element_type"]}

# storing player ratings based on position
goalkeeper_ratings = {}
defender_ratings = {}
midfielder_ratings = {}
forward_ratings = {}

position_map = {
    1: goalkeeper_ratings, 
    2: defender_ratings,
    3: midfielder_ratings,
    4: forward_ratings
}

for player, info in player_ratings.items():
    position_map[info["position"]][player] = info["rating"]

# print sorted by position and their ratings
print("player ratings by position:")
for position_name, ratings in [("goalkeepers", goalkeeper_ratings),
                               ("defenders", defender_ratings), 
                               ("midfielders", midfielder_ratings), 
                               ("forwards", forward_ratings)]:
    print(f"\nthe best {position_name}")
    for player, rating in sorted(ratings.items(), key=lambda x: x[1], reverse=True): # gotten from chatgpt
        print(f"{player}: {rating}")
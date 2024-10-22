import requests
from positions.goalkeeper import calculate_rating as goalkeeper_rating
from positions.defender import calculate_rating as defender_rating
from positions.midfielder import calculate_rating as midfielder_rating
from positions.forward import calculate_rating as forward_rating

# pulling the data from api end point
data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
d = data.json() 

players = d["elements"]
prev_highest = 0
name_highest = ""
for player in players:
    # splitting into specific position
    if player["element_type"] == 1:
        rating = goalkeeper_rating(player)
    elif player["element_type"] == 2:
        rating = defender_rating(player)
    elif player["element_type"] == 3:
        rating = midfielder_rating(player)
    elif player["element_type"] == 4:
        rating = forward_rating(player)
    
    if rating > prev_highest:
        if player["web_name"] != "Jaros":
            prev_highest = rating
            name_highest = player["web_name"]

print(f"{name_highest} is the highest scoring goalie with a rating off {prev_highest}")
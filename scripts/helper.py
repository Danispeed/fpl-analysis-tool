from teams import team_strength
from teams import fixture_comparison

# normalize a player's stat value to a range between 0-1 based on min and max value of that stat across all players of the same position
def normalize_stat(player_stat, min_stat, max_stat):
    if max_stat == min_stat:
        print("Error, should not get minimum and maximum stat to be equal")
        return 0 # cannot divide by zero
    else:
        return (player_stat - min_stat) / (max_stat - min_stat)
    
# inverted normalization for stats where a lower value is better
def normalize_stat_inverted(player_stat, min_stat, max_stat):
    if max_stat == min_stat:
        print("Error, should not get minimum and maximum stat to be equal")
        return 0 # cannot divide by zero
    else:
        return (max_stat - player_stat) / (max_stat - min_stat)

# calculate team specific data 
def calculate_team_data(data, fixtures):
    team_data = {}
    for team in data["teams"]:
        team_id = team["id"] 
        attack_strength, defense_strenght = team_strength(team)

        # gather data on the next 5 upcoming fixtures for a team
        upcoming_fixtures = [] 
        five_upcoming_fixtures = 5
        for fixture in fixtures:
            if fixture["finished"] == False:
                # checking through all premier league fixtures which has not started, starting from the fixture nearest current date
                if fixture["team_h"] == team_id or fixture["team_a"] == team_id:
                    # finding opponents team id, which is the opposite in the same fixture
                    opponent_id = 0
                    if fixture["team_h"] == team_id:
                        opponent_id = fixture["team_a"]
                    if fixture["team_a"] == team_id:
                        opponent_id = fixture["team_h"]
                    for opponent in data["teams"]:
                        if opponent["id"] == opponent_id: 
                            # comparing the two teams, checking difficulty in 
                            # attack and defense for "team" against "opponent"
                            attack_diff, defense_diff = fixture_comparison(team, opponent)
                            upcoming_fixtures.append({"opponent_id": opponent_id, "attack_diff": attack_diff, "defense_diff": defense_diff})

                            five_upcoming_fixtures -= 1
                            if five_upcoming_fixtures == 0:
                                break
        
        # calculate the total fixture difficulty for upcoming 5 matches both in attack and defense
        total_attack_diff = sum(fix["attack_diff"] for fix in upcoming_fixtures[:5])
        total_defense_diff = sum(fix["defense_diff"] for fix in upcoming_fixtures[:5])
        team_data[team_id] = {"team_attacking_strength": attack_strength, "team_defensive_strength": defense_strenght, "fixture_difficulty_attacker": total_attack_diff, "fixture_difficulty_defender": total_defense_diff}

    return team_data

def compute_stats_min_max(players, team_data):
    stats_min_max = {
        "goals_scored": {"min": float('inf'), "max": float('-inf')},
        "assists": {"min": float('inf'), "max": float('-inf')},
        "influence": {"min": float('inf'), "max": float('-inf')},
        "threat": {"min": float('inf'), "max": float('-inf')},
        "creativity": {"min": float('inf'), "max": float('-inf')},
        "bps": {"min": float('inf'), "max": float('-inf')},
        "form": {"min": float('inf'), "max": float('-inf')},
        "expected_goals": {"min": float('inf'), "max": float('-inf')},           
        "expected_assists": {"min": float('inf'), "max": float('-inf')},         
        "expected_goals_per_90": {"min": float('inf'), "max": float('-inf')},    
        "expected_assists_per_90": {"min": float('inf'), "max": float('-inf')}, 
        "yellow_cards": {"min": float('inf'), "max": float('-inf')},
        "clean_sheets_per_90": {"min": float('inf'), "max": float('-inf')},
        "goals_conceded_per_90": {"min": float('inf'), "max": float('-inf')},
        "expected_goals_conceded_per_90": {"min": float('inf'), "max": float('-inf')},
        "saves_per_90": {"min": float('inf'), "max": float('-inf')},
        "goals_per_90": {"min": float('inf'), "max": float('-inf')},    
        "assists_per_90": {"min": float('inf'), "max": float('-inf')},
        "team_attacking_strength": {"min": float('inf'), "max": float('-inf')},
        "team_defensive_strength": {"min": float('inf'), "max": float('-inf')},
        "fixture_difficulty_attacker": {"min": float("inf"), "max": float("-inf")},
        "fixture_difficulty_defender": {"min": float("inf"), "max": float("-inf")},
    }

    # iterate over each player to calculate min and max for each stat
    for player in players:
        team_id = player["team"]
        for stat in stats_min_max.keys():
            try:
                # calculating goals and assists per 90, from goals, assists, and minutes data
                if stat == "goals_per_90":
                    if player["goals_scored"] == 0:
                        value = 0
                    else: 
                        value = (player.get("goals_scored", 0) / player.get("minutes", 1)) * 90
                elif stat == "assists_per_90":
                    if player["assists"] == 0:
                        value = 0
                    else: 
                        value = (player.get("assists", 0) / player.get("minutes", 1)) * 90

                # team attack or defense
                elif stat == "team_attacking_strength":
                    value = team_data[team_id]["team_attacking_strength"]
                elif stat == "team_defensive_strength":
                    value = team_data[team_id]["team_defensive_strength"]

                # upcoming 5 fixtures for the players team
                elif stat == "fixture_difficulty_attacker":
                    value = team_data[team_id]["fixture_difficulty_attacker"]
                elif stat == "fixture_difficulty_defender":
                    value = team_data[team_id]["fixture_difficulty_defender"]

                # default case, get the player stat directly from the API
                else:
                    value = float(player.get(stat, 0))

                # updating min and max values for the stats
                if value < stats_min_max[stat]["min"]:
                    stats_min_max[stat]["min"] = value
                if value > stats_min_max[stat]["max"]:
                    stats_min_max[stat]["max"] = value

            except ValueError:
                name = player['web_name']
                print("Stat {stat} is not available for polayer {name}")
    return stats_min_max
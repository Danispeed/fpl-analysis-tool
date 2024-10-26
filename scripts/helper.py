def normalize_stat(player_stat, min_stat, max_stat):
    if max_stat == min_stat:
        print("Error, should not get minimum and maximum stat to be equal")
        return 0 # cannot divide by zero
    else:
        return (player_stat - min_stat) / (max_stat - min_stat)
    
def normalize_stat_inverted(player_stat, min_stat, max_stat):
    if max_stat == min_stat:
        print("Error, should not get minimum and maximum stat to be equal")
        return 0 # cannot divide by zero
    else:
        return (max_stat - player_stat) / (max_stat - min_stat)
    
def compute_stats_min_max(players, position):
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
    }

    for player in players:
        if player["element_type"] == position:
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
                    pass
    return stats_min_max
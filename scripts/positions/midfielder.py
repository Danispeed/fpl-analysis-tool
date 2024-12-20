from helper import normalize_stat
from helper import normalize_stat_inverted

def calculate_rating(player, stats_min_max, own_team):
    rating = 0
    max_rating = 100
    
    # normalize positive stats
    goals_per_90 = normalize_stat(float(player["goals_scored"] / player["minutes"] * 90) if player["minutes"] > 0 else 0, stats_min_max["goals_per_90"]["min"], stats_min_max["goals_per_90"]["max"])
    assists_per_90 = normalize_stat(float(player["assists"] / player["minutes"] * 90) if player["minutes"] > 0 else 0, stats_min_max["assists_per_90"]["min"], stats_min_max["assists_per_90"]["max"])
    influence = normalize_stat(float(player["influence"]), stats_min_max["influence"]["min"], stats_min_max["influence"]["max"])
    threat = normalize_stat(float(player["threat"]), stats_min_max["threat"]["min"], stats_min_max["threat"]["max"])
    creativity = normalize_stat(float(player["creativity"]), stats_min_max["creativity"]["min"], stats_min_max["creativity"]["max"])
    bps = normalize_stat(player["bps"], stats_min_max["bps"]["min"], stats_min_max["bps"]["max"])
    form = normalize_stat(float(player["form"]), stats_min_max["form"]["min"], stats_min_max["form"]["max"])
    # xG = normalize_stat(float(player["expected_goals"]), stats_min_max["expected_goals"]["min"], stats_min_max["expected_goals"]["max"])
    # xA = normalize_stat(float(player["expected_assists"]), stats_min_max["expected_assists"]["min"], stats_min_max["expected_assists"]["max"])
    xG_p90 = normalize_stat(float(player["expected_goals_per_90"]), stats_min_max["expected_goals_per_90"]["min"], stats_min_max["expected_goals_per_90"]["max"])
    xA_p90 = normalize_stat(float(player["expected_assists_per_90"]), stats_min_max["expected_assists_per_90"]["min"], stats_min_max["expected_assists_per_90"]["max"])
    
    # normalize negative stats
    yellow_cards = normalize_stat_inverted(player["yellow_cards"], stats_min_max["yellow_cards"]["min"], stats_min_max["yellow_cards"]["max"])

    # team strength and fixture difficulty (upcoming 5)
    attack_strength = own_team["team_attacking_strength"]
    fixture_difficulty_attack = own_team["fixture_difficulty_attacker"]

    # normalize team strength and fixture difficulty
    attack_strength = normalize_stat(attack_strength, stats_min_max["team_attacking_strength"]["min"], stats_min_max["team_attacking_strength"]["max"])
    fixture_difficulty_attack = normalize_stat(fixture_difficulty_attack, stats_min_max["fixture_difficulty_attacker"]["min"], stats_min_max["fixture_difficulty_attacker"]["max"])

    # weights for both positive and negative stats
    weights = {
        "goals_per_90": 20,
        "assists_per_90": 15,
        "influence": 8,
        "threat": 12,
        "creativity": 10,
        "bps": 8,
        "form": 6,
        "xG_p90": 15,
        "xA_p90": 12,
        "yellow_cards": 2,
        "attack_strength": 10,
        "fixture_difficulty": 10
    }

    # compute contributions of both negative and positive stats
    rating += goals_per_90 * weights["goals_per_90"]
    rating += assists_per_90 * weights["assists_per_90"]
    rating += influence * weights["influence"]
    rating += threat * weights["threat"]
    rating += creativity * weights["creativity"]
    rating += bps * weights["bps"]
    rating += form * weights["form"]
    # rating += xG * weights["xG"]
    # rating += xA * weights["xA"]
    rating += xG_p90 * weights["xG_p90"]
    rating += xA_p90 * weights["xA_p90"]
    rating -= yellow_cards * weights["yellow_cards"]
    rating += attack_strength * weights["attack_strength"]
    rating += fixture_difficulty_attack * weights["fixture_difficulty"]

    # ensure rating is between 0 and 100
    rating = max(0, min(rating, max_rating))

    return rating
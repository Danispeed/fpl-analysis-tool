from helper import normalize_stat
from helper import normalize_stat_inverted

def calculate_rating(player, stats_min_max, own_team):
    rating = 0
    max_rating = 100

    # normalize positive stats
    clean_sheets_p90 = normalize_stat(player["clean_sheets_per_90"], stats_min_max["clean_sheets_per_90"]["min"], stats_min_max["clean_sheets_per_90"]["max"])
    goals_per_90 = normalize_stat((player["goals_scored"] / player["minutes"] * 90) if player["minutes"] > 0 else 0, stats_min_max["goals_per_90"]["min"], stats_min_max["goals_per_90"]["max"])
    assists_per_90 = normalize_stat((player["assists"] / player["minutes"] * 90) if player["minutes"] > 0 else 0, stats_min_max["assists_per_90"]["min"], stats_min_max["assists_per_90"]["max"])
    influence = normalize_stat(float(player["influence"]), stats_min_max["influence"]["min"], stats_min_max["influence"]["max"])
    creativity = normalize_stat(float(player["creativity"]), stats_min_max["creativity"]["min"], stats_min_max["creativity"]["max"])
    threat = normalize_stat(float(player["threat"]), stats_min_max["threat"]["min"], stats_min_max["threat"]["max"])
    bps = normalize_stat(player["bps"], stats_min_max["bps"]["min"], stats_min_max["bps"]["max"])
    form = normalize_stat(float(player["form"]), stats_min_max["form"]["min"], stats_min_max["form"]["max"])
    xG_p90 = normalize_stat(float(player["expected_goals_per_90"]), stats_min_max["expected_goals_per_90"]["min"], stats_min_max["expected_goals_per_90"]["max"])
    xA_p90 = normalize_stat(float(player["expected_assists_per_90"]), stats_min_max["expected_assists_per_90"]["min"], stats_min_max["expected_assists_per_90"]["max"])

    # normalize negative stats
    goals_conceded_p90 = normalize_stat_inverted(player["goals_conceded_per_90"], stats_min_max["goals_conceded_per_90"]["min"], stats_min_max["goals_conceded_per_90"]["max"])
    xGC_p90 = normalize_stat_inverted(float(player["expected_goals_conceded_per_90"]), stats_min_max["expected_goals_conceded_per_90"]["min"], stats_min_max["expected_goals_conceded_per_90"]["max"])
    yellow_cards = normalize_stat_inverted(player["yellow_cards"], stats_min_max["yellow_cards"]["min"], stats_min_max["yellow_cards"]["max"])

    # team strengths and fixture difficulties
    attack_strength = own_team["team_attacking_strength"]
    defense_strength = own_team["team_defensive_strength"]
    fixture_difficulty_attack = own_team["fixture_difficulty_attacker"]
    fixture_difficulty_defense = own_team["fixture_difficulty_defender"]

    # normalize team strengths and fixture difficulties
    attack_strength = normalize_stat(attack_strength, stats_min_max["team_attacking_strength"]["min"], stats_min_max["team_attacking_strength"]["max"])
    defense_strength = normalize_stat(defense_strength, stats_min_max["team_defensive_strength"]["min"], stats_min_max["team_defensive_strength"]["max"])
    fixture_difficulty_attack = normalize_stat_inverted(fixture_difficulty_attack, stats_min_max["fixture_difficulty_attacker"]["min"], stats_min_max["fixture_difficulty_attacker"]["max"])
    fixture_difficulty_defense = normalize_stat_inverted(fixture_difficulty_defense, stats_min_max["fixture_difficulty_defender"]["min"], stats_min_max["fixture_difficulty_defender"]["max"])

    # weights for both positive and negative stats
    weights = {
        "clean_sheets_p90": 25,
        "defense_strength": 15,
        "fixture_difficulty_defense": 10,
        "goals_per_90": 10,
        "assists_per_90": 8,
        "xG_p90": 8,
        "xA_p90": 6,
        "threat": 8,
        "creativity": 6,
        "bps": 8,
        "form": 6,
        "attack_strength": 5,
        "fixture_difficulty_attack": 5,
        "goals_conceded_p90": 5,
        "xGC_p90": 5,
        "yellow_cards": 2
    }

    # compute contributions of both negative and positive stats
    rating += clean_sheets_p90 * weights["clean_sheets_p90"]
    rating += defense_strength * weights["defense_strength"]
    rating += fixture_difficulty_defense * weights["fixture_difficulty_defense"]
    rating += goals_per_90 * weights["goals_per_90"]
    rating += assists_per_90 * weights["assists_per_90"]
    rating += xG_p90 * weights["xG_p90"]
    rating += xA_p90 * weights["xA_p90"]
    rating += threat * weights["threat"]
    rating += creativity * weights["creativity"]
    rating += bps * weights["bps"]
    rating += form * weights["form"]
    rating += attack_strength * weights["attack_strength"]
    rating += fixture_difficulty_attack * weights["fixture_difficulty_attack"]
    rating -= goals_conceded_p90 * weights["goals_conceded_p90"]
    rating -= xGC_p90 * weights["xGC_p90"]
    rating -= yellow_cards * weights["yellow_cards"]

    # ensure rating is between 0 and 100
    rating = max(0, min(rating, max_rating))

    return rating
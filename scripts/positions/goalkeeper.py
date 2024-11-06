from helper import normalize_stat
from helper import normalize_stat_inverted

def calculate_rating(player, stats_min_max, own_team):
    rating = 0
    max_rating = 100

    # normalize positive stats
    clean_sheets_p90 = normalize_stat(player["clean_sheets_per_90"], stats_min_max["clean_sheets_per_90"]["min"], stats_min_max["clean_sheets_per_90"]["max"])
    saves_per_90 = normalize_stat(player["saves_per_90"], stats_min_max["saves_per_90"]["min"], stats_min_max["saves_per_90"]["max"])
    bps = normalize_stat(player["bps"], stats_min_max["bps"]["min"], stats_min_max["bps"]["max"])
    form = normalize_stat(float(player["form"]), stats_min_max["form"]["min"], stats_min_max["form"]["max"])

    # normalize negative stats
    goals_conceded_p90 = normalize_stat_inverted(player["goals_conceded_per_90"], stats_min_max["goals_conceded_per_90"]["min"], stats_min_max["goals_conceded_per_90"]["max"])
    xGC_p90 = normalize_stat_inverted(float(player["expected_goals_conceded_per_90"]), stats_min_max["expected_goals_conceded_per_90"]["min"], stats_min_max["expected_goals_conceded_per_90"]["max"])
    yellow_cards = normalize_stat_inverted(player["yellow_cards"], stats_min_max["yellow_cards"]["min"], stats_min_max["yellow_cards"]["max"])

    # team strength and fixture difficulty
    defense_strength = own_team["team_defensive_strength"]
    fixture_difficulty_defense = own_team["fixture_difficulty_defender"]

    # normalize team strength and fixture difficulty
    defense_strength = normalize_stat(defense_strength, stats_min_max["team_defensive_strength"]["min"], stats_min_max["team_defensive_strength"]["max"])
    fixture_difficulty_defense = normalize_stat_inverted(fixture_difficulty_defense, stats_min_max["fixture_difficulty_defender"]["min"], stats_min_max["fixture_difficulty_defender"]["max"])

    # weights for both positive and negative stats
    weights = {
        "clean_sheets_p90": 25,
        "defense_strength": 20,
        "fixture_difficulty_defense": 15,
        "saves_per_90": 20,
        "bps": 8,
        "form": 6,
        "goals_conceded_p90": 5,
        "xGC_p90": 5,
        "yellow_cards": 2
    }

    # compute contributions of both negative and positive stats
    rating += clean_sheets_p90 * weights["clean_sheets_p90"]
    rating += defense_strength * weights["defense_strength"]
    rating += fixture_difficulty_defense * weights["fixture_difficulty_defense"]
    rating += saves_per_90 * weights["saves_per_90"]
    rating += bps * weights["bps"]
    rating += form * weights["form"]
    rating -= goals_conceded_p90 * weights["goals_conceded_p90"]
    rating -= xGC_p90 * weights["xGC_p90"]
    rating -= yellow_cards * weights["yellow_cards"]

    # ensure rating is between 0 and 100
    rating = max(0, min(rating, max_rating))

    return rating
def calculate_rating(player):
    print(player["web_name"])
    rating = 0

    # Clean sheets per 90 minutes (important for goalkeepers)
    if player["clean_sheets_per_90"] > 0:
        rating += player["clean_sheets_per_90"] * 20  # Weight clean sheets heavily

    # Saves per 90 minutes (higher saves are good)
    rating += player["saves_per_90"] * 10  # Give points for each save

    # Penalize for goals conceded
    if player["goals_conceded_per_90"] > 1:
        rating -= player["goals_conceded_per_90"] * 10  # Subtract points for each goal conceded

    # BPS (Bonus Points System)
    rating += player["bps"] / 10  # Scale the BPS to fit a 10-point range

    # Form (recent performance)
    rating += float(player["form"]) * 5  # Scale form to a max of 5 points

    # Expected goals conceded (lower is better)
    rating -= float(player["expected_goals_conceded_per_90"]) * 5  # Penalize for expected goals conceded

    # Ensure rating is between 0 and 100
    rating = max(0, min(rating, 100))

    print(rating)

    return rating
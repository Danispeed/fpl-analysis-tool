# return two strength variables, both offense and defense
def team_strength(team):
    att_strength = 0
    def_strength = 0

    # important for defender, midfielder, attacker
    att_strength += attacking_threat(team)

    # important for goalkeeper, defender
    def_strength += defending_security(team)

    return att_strength, def_strength 

# compares the relative strengths of two teams, both offensively and defensively
# wtih team1 being the player's team
def fixture_comparison(team1, team2):
    attacking1, defensive1 = team_strength(team1)
    attacking2, defensive2 = team_strength(team2)

    attack = attacking1 - defensive2
    defense = defensive1 - attacking2

    return attack, defense

# taking the average of attacking home and away
def attacking_threat(team):
    return (team["strength_attack_home"] + team["strength_attack_away"]) / 2

# taking the average of defending home and away
def defending_security(team):
    return (team["strength_defence_home"] + team["strength_defence_away"]) / 2
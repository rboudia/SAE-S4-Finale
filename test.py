def tournament_tree_levels(total_matches):
    levels = []
    matches_remaining = total_matches
    matches_at_level = 1
    level = 1

    while matches_remaining > 0 and matches_remaining >= matches_at_level:
        levels.append((level, matches_at_level))
        matches_remaining -= matches_at_level
        level += 1
        matches_at_level *= 2
        reversed_list = levels[::-1]
    return reversed_list

# Exemple d'utilisation
total_matches = 1000
tree_levels = tournament_tree_levels(total_matches)
for level, matches in tree_levels:
    print(f"Au {level}ème niveau, il y a {matches} matchs.")

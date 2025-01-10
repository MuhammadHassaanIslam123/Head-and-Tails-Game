import random
import pandas as pd
from itertools import combinations


# Step 1: Setup Teams and Groups
def setup_teams_and_groups():
    """Ask the user for team names, divide into groups, and assign the user's team."""
    print("Welcome to the T20 World Cup")

    # Ask for team names
    teams = []
    print("\nEnter the names of 8 teams:")
    for i in range(8):
        while True:
            team_name = input(f"Enter the name of team {i + 1}: ").strip()
            if team_name and team_name not in teams:
                teams.append(team_name)
                break
            print("Invalid or duplicate team name. Please try again.")

    # Shuffle and divide teams into groups
    random.shuffle(teams)
    group_a = teams[:4]
    group_b = teams[4:]

    # Display groups
    print("\n--- Groups ---")
    print("Group A:")
    for team in group_a:
        print(f"- {team}")
    print("Group B:")
    for team in group_b:
        print(f"- {team}")

    # Assign user's team
    user_team = None
    while True:
        chosen_team = input(
            "\nChoose your team by typing its name (or type 'computer' to let the computer control all teams): ").strip()
        if chosen_team.lower() == "computer":
            print("\nYou chose to let the computer control all teams.")
            user_team = "computer"
            break
        elif chosen_team in teams:
            print(f"\nYou chose the team: {chosen_team}")
            user_team = chosen_team
            break
        print("Invalid choice. Please choose a valid team name from Group A or Group B.")

    return group_a, group_b, user_team


# Step 2: Generate Match Schedules
def generate_group_schedule(group):
    """Generate a schedule for matches within a group."""
    return list(combinations(group, 2))


def generate_full_schedule(group_a, group_b):
    """Combine match schedules for both groups into a single unified schedule."""
    group_a_matches = generate_group_schedule(group_a)
    group_b_matches = generate_group_schedule(group_b)
    return group_a_matches + group_b_matches


def display_schedule(schedule):
    """Display the complete match schedule."""
    print("\n--- Full Match Schedule ---")
    for i, match in enumerate(schedule, start=1):
        print(f"Match {i}: {match[0]} vs {match[1]}")





# Step 3: Group Tables
def initialize_group_table(group):
    """Create a table with Wins, Losses, Draws, Points, and Net Run Rate (NRR) for a group."""
    table = {team: {"Wins": 0, "Losses": 0, "Draws": 0, "Points": 0, "Net Run Rate": 0.0} for team in group}
    return pd.DataFrame.from_dict(table, orient="index")


def reorder_group_table(table):
    """Reorder the group table based on Points, Wins, and Net Run Rate (NRR)."""
    table = table.sort_values(by=["Points", "Wins", "Net Run Rate"], ascending=[False, False, False])
    return table


def update_group_table(table, team1, team2, team1_score, team2_score, team1_overs, team2_overs):
    """Update the group table after a match."""
    # Team 1 wins
    if team1_score > team2_score:
        table.loc[team1, "Wins"] += 1
        table.loc[team1, "Points"] += 2
        table.loc[team2, "Losses"] += 1
    # Team 2 wins
    elif team2_score > team1_score:
        table.loc[team2, "Wins"] += 1
        table.loc[team2, "Points"] += 2
        table.loc[team1, "Losses"] += 1
    # Match is a draw
    else:
        table.loc[team1, "Draws"] += 1
        table.loc[team2, "Draws"] += 1
        table.loc[team1, "Points"] += 1
        table.loc[team2, "Points"] += 1

    # Update Net Run Rate
    team1_nrr = (team1_score / team1_overs) - (team2_score / team2_overs)
    team2_nrr = (team2_score / team2_overs) - (team1_score / team1_overs)
    table.loc[team1, "Net Run Rate"] += team1_nrr
    table.loc[team2, "Net Run Rate"] += team2_nrr

    # Reorder the table after updating
    table = reorder_group_table(table)
    return table


def display_group_table(group_name, table):
    """Display the updated group table."""
    print(f"\n--- {group_name} Points Table ---")
    print(table)





# Step 4: User Batting Innings
def user_batting_innings(target_score=None):
    """Simulate the user's batting innings."""
    print("\n--- Your Team is Batting ---")
    total_score = 0
    wickets_lost = 0  # Track wickets lost
    balls = 120
    ball_count = 0

    while ball_count < balls and wickets_lost < 10:
        print("\nOptions for batting simulation:")
        print("1. Simulate entire innings (20 overs)")
        print("2. Simulate 5 overs")
        print("3. Simulate 1 over")
        print("4. Play ball by ball")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            simulate_balls = balls - ball_count
        elif choice == '2' and (balls - ball_count) >= 30:
            simulate_balls = 30
        elif choice == '3' and (balls - ball_count) >= 6:
            simulate_balls = 6
        elif choice == '4':
            simulate_balls = 0
        else:
            print("Invalid choice or not enough balls remaining for this option. Please try again.")
            continue

        # Simulate innings
        if simulate_balls > 0:
            for _ in range(simulate_balls):
                if ball_count >= balls or wickets_lost == 10 or (target_score and total_score >= target_score):
                    break
                ball_count += 1
                user_score = random.randint(0, 6)
                comp_score = random.randint(0, 6)
                if user_score == comp_score:
                    wickets_lost += 1  # Increment wickets lost
                else:
                    total_score += user_score
                if target_score and total_score >= target_score:
                    print(f"\nYou chased the target in {ball_count / 6:.1f} overs with {10 - wickets_lost} wickets remaining!")
                    return total_score, ball_count / 6
            print(f"Final score: {total_score}/{wickets_lost} in {ball_count / 6:.1f} overs.")
            return total_score, ball_count / 6
        else:
            # Play ball by ball
            while ball_count < balls and wickets_lost < 10:
                ball_count += 1
                try:
                    user_score = int(input(f"Ball {ball_count}: Choose a number between 0 and 6: "))
                    if user_score < 0 or user_score > 6:
                        print("Invalid choice. Please choose a number between 0 and 6.")
                        ball_count -= 1
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 6.")
                    ball_count -= 1
                    continue

                comp_score = random.randint(0, 6)
                print(f"Computer chose {comp_score}")

                if user_score == comp_score:
                    wickets_lost += 1  # Increment wickets lost
                    print(f"You're out! Wickets left: {10 - wickets_lost}")
                else:
                    total_score += user_score
                print(f"Current score: {total_score}/{wickets_lost}")

                if target_score and total_score >= target_score:
                    print(f"\nYou chased the target in {ball_count / 6:.1f} overs with {10 - wickets_lost} wickets remaining!")
                    return total_score, ball_count / 6

    print(f"Innings over. Final score: {total_score}/{wickets_lost} in {ball_count / 6:.1f} overs.")
    return total_score, ball_count / 6





# Step 5: Computer Batting Innings
def computer_batting_innings(team_name, target_score=None):
    """Simulate the computer's batting innings with user-controlled bowling options."""
    print(f"\n--- {team_name}'s innings begins ---")
    total_score = 0
    wickets_lost = 0  # Track wickets lost
    balls = 120
    ball_count = 0

    while ball_count < balls and wickets_lost < 10:
        print(f"\nOptions for bowling simulation:")
        print("1. Simulate entire innings (20 overs)")
        print("2. Simulate 5 overs")
        print("3. Simulate 1 over")
        print("4. Bowl ball by ball")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            simulate_balls = balls - ball_count
        elif choice == '2' and (balls - ball_count) >= 30:
            simulate_balls = 30
        elif choice == '3' and (balls - ball_count) >= 6:
            simulate_balls = 6
        elif choice == '4':
            simulate_balls = 0
        else:
            print("Invalid choice or not enough balls remaining for this option. Please try again.")
            continue

        # Simulate innings
        if simulate_balls > 0:
            for _ in range(simulate_balls):
                if ball_count >= balls or wickets_lost == 10 or (target_score and total_score >= target_score):
                    break
                ball_count += 1
                computer_score = random.randint(0, 6)
                user_guess = random.randint(0, 6)  # Simulated user guess
                if computer_score == user_guess:
                    wickets_lost += 1  # Increment wickets lost
                else:
                    total_score += computer_score
                if target_score and total_score >= target_score:
                    print(f"\n{team_name} chased the target in {ball_count / 6:.1f} overs with {10 - wickets_lost} wickets remaining!")
                    return total_score, ball_count / 6
            print(f"After {ball_count / 6:.1f} overs: {total_score}/{wickets_lost}")
        else:
            # Bowl ball by ball
            while ball_count < balls and wickets_lost < 10:
                ball_count += 1
                try:
                    user_guess = int(input(f"Ball {ball_count}: Guess a number between 0 and 6: "))
                    if user_guess < 0 or user_guess > 6:
                        print("Invalid choice. Please choose a number between 0 and 6.")
                        ball_count -= 1
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 6.")
                    ball_count -= 1
                    continue

                computer_score = random.randint(0, 6)
                print(f"Computer chose {computer_score}")

                if computer_score == user_guess:
                    wickets_lost += 1  # Increment wickets lost
                    print(f"Computer is OUT! Wickets left: {10 - wickets_lost}")
                else:
                    total_score += computer_score
                print(f"Current score: {total_score}/{wickets_lost}")

                if target_score and total_score >= target_score:
                    print(f"\n{team_name} chased the target in {ball_count / 6:.1f} overs with {10 - wickets_lost} wickets remaining!")
                    return total_score, ball_count / 6

                # Offer to simulate at specific intervals
                if ball_count % 6 == 0 and wickets_lost < 10:
                    print("\nOptions to continue:")
                    print("1. Simulate remaining innings")
                    print("2. Simulate 5 overs")
                    print("3. Simulate 1 over")
                    print("4. Continue bowling")
                    interval_choice = input("Enter your choice (1/2/3/4): ").strip()
                    if interval_choice == '1':
                        simulate_balls = balls - ball_count
                        break
                    elif interval_choice == '2' and (balls - ball_count) >= 30:
                        simulate_balls = 30
                        break
                    elif interval_choice == '3' and (balls - ball_count) >= 6:
                        simulate_balls = 6
                        break
                    elif interval_choice == '4':
                        continue
                    else:
                        print("Invalid choice. Continuing ball by ball.")
                        continue

    print(f"\n{team_name}'s innings is over. Final score: {total_score}/{wickets_lost} in {ball_count / 6:.1f} overs.")
    return total_score, ball_count / 6









# Step 6: Toss and Match Logic (User and Computer Integration)
def toss_and_match_logic_with_tables(match, user_team, group_a_table, group_b_table):
    """Simulate toss, play the match, and update group tables."""
    print(f"\n--- Match: {match[0]} vs {match[1]} ---")
    group_table = group_a_table if match[0] in group_a_table.index else group_b_table

    user_batting_first = None

    if user_team in match:
        print("\n--- Toss ---")
        while True:
            user_toss_call = input(f"Choose heads or tails for the toss: ").strip().lower()
            if user_toss_call in ["heads", "tails"]:
                break
            print("Invalid input. Please choose 'heads' or 'tails'.")
        toss_result = random.choice(["heads", "tails"])
        print(f"The toss result is: {toss_result.capitalize()}")

        if user_toss_call == toss_result:
            print("You won the toss!")
            while True:
                toss_decision = input("Do you want to bat or bowl? (Enter 'bat' or 'bowl'): ").strip().lower()
                if toss_decision in ["bat", "bowl"]:
                    user_batting_first = toss_decision == "bat"
                    break
                print("Invalid input. Please type 'bat' or 'bowl'.")
        else:
            print("You lost the toss.")
            computer_choice = random.choice(["bat", "bowl"])
            print(f"The opponent chose to {computer_choice} first.")
            user_batting_first = computer_choice == "bowl"

        # Simulate the match based on toss results
        if user_batting_first:
            print("\nYou are batting first.")
            user_score, user_overs = user_batting_innings()
            target = user_score + 1
            print(f"\nYour final score: {user_score}/{10} in {user_overs:.1f} overs. Target for opponent: {target}.")
            comp_score, comp_overs = computer_batting_innings(match[1], target)
        else:
            print("\nYou are bowling first.")
            comp_score, comp_overs = computer_batting_innings(match[0])
            target = comp_score + 1
            print(f"\nOpponent's final score: {comp_score}/{10} in {comp_overs:.1f} overs. Target for your team: {target}.")
            user_score, user_overs = user_batting_innings(target_score=target)

        # Update the group table
        group_table = update_group_table(group_table, match[0], match[1], user_score, comp_score, user_overs, comp_overs)
    else:
        # Simulate computer vs computer match
        print("\nSimulating the match...")
        team1_score = random.randint(100, 200)
        team2_score = random.randint(100, 200)
        team1_wickets = random.randint(0, 10)
        team2_wickets = random.randint(0, 10)

        print(f"\n{match[0]} scored: {team1_score}/{team1_wickets} in 20 overs.")
        print(f"{match[1]} scored: {team2_score}/{team2_wickets} in 20 overs.")

        # Update tables
        group_table = update_group_table(group_table, match[0], match[1], team1_score, team2_score, 20, 20)

    # Display updated group table
    group_name = "Group A" if group_table is group_a_table else "Group B"
    display_group_table(group_name, group_table)









# Step 7: Determine Semifinalists
def determine_semifinalists(group_a_table, group_b_table):
    """Determine the top 2 teams from each group for the semifinals."""
    print("\n--- Determining Semifinalists ---")

    # Sort Group Tables by Points and Net Run Rate
    group_a_table = reorder_group_table(group_a_table)
    group_b_table = reorder_group_table(group_b_table)

    # Top 2 Teams from Group A and Group B
    group_a_teams = group_a_table.index.tolist()
    group_b_teams = group_b_table.index.tolist()

    # Semifinalists
    team1, team2 = group_a_teams[:2]
    team3, team4 = group_b_teams[:2]

    print(f"Semifinalists: Team 1 ({team1}), Team 2 ({team2}), Team 3 ({team3}), Team 4 ({team4})")
    return team1, team2, team3, team4








# Step 8: Play Match (User or Simulated)
def play_match(team1, team2, user_team):
    """Simulate or play a match depending on whether the user is involved."""
    print(f"\n--- Match: {team1} vs {team2} ---")

    if user_team in [team1, team2]:
        print("\n--- Toss ---")
        while True:
            user_toss_call = input(f"Choose heads or tails for the toss: ").strip().lower()
            if user_toss_call in ["heads", "tails"]:
                break
            print("Invalid input. Please choose 'heads' or 'tails'.")
        toss_result = random.choice(["heads", "tails"])
        print(f"The toss result is: {toss_result.capitalize()}")

        if user_toss_call == toss_result:
            print("You won the toss!")
            while True:
                toss_decision = input("Do you want to bat or bowl? (Enter 'bat' or 'bowl'): ").strip().lower()
                if toss_decision in ["bat", "bowl"]:
                    user_batting_first = toss_decision == "bat"
                    break
                print("Invalid input. Please type 'bat' or 'bowl'.")
        else:
            print("You lost the toss.")
            user_batting_first = random.choice([True, False])
            print(f"The opponent chose to {'bat' if user_batting_first else 'bowl'} first.")

        # Simulate innings based on toss decision
        if user_team == team1:
            if user_batting_first:
                user_score, user_overs = user_batting_innings()
                comp_score, comp_overs = computer_batting_innings(team2, user_score + 1)
            else:
                comp_score, comp_overs = computer_batting_innings(team1)
                user_score, user_overs = user_batting_innings(target_score=comp_score + 1)
        else:
            if user_batting_first:
                user_score, user_overs = user_batting_innings()
                comp_score, comp_overs = computer_batting_innings(team1, user_score + 1)
            else:
                comp_score, comp_overs = computer_batting_innings(team2)
                user_score, user_overs = user_batting_innings(target_score=comp_score + 1)

        # Determine winner
        if user_score > comp_score:
            print(f"\nYour team ({user_team}) wins!")
            return user_team
        else:
            print(f"\n{team2 if user_team == team1 else team1} wins!")
            return team2 if user_team == team1 else team1
    else:
        # Simulate match
        team1_score = random.randint(0, 200)
        team2_score = random.randint(0, 200)

        print(f"{team1} scored: {team1_score}")
        print(f"{team2} scored: {team2_score}")

        if team1_score > team2_score:
            print(f"{team1} wins!")
            return team1
        else:
            print(f"{team2} wins!")
            return team2



# Step 9: Play Semifinals and Final
def play_semifinals_and_final(team1, team2, team3, team4, user_team):
    """Play the semifinals and final to determine the champion."""
    # Semifinal Matches
    semifinalists = [
        (team1, team4),  # Team 1 vs Team 4
        (team2, team3),  # Team 2 vs Team 3
    ]

    print("\n--- Playing Semifinals ---")
    winners = []
    for match in semifinalists:
        winner = play_match(match[0], match[1], user_team)
        winners.append(winner)

    # Final Match
    print("\n--- Final Match ---")
    champion = play_match(winners[0], winners[1], user_team)

    print(f"\n--- Champion: {champion} ---")
    return champion







# Main Game Logic
group_a, group_b, user_team = setup_teams_and_groups()  # Setup teams and groups
group_a_table = initialize_group_table(group_a)  # Initialize Group A table
group_b_table = initialize_group_table(group_b)  # Initialize Group B table
full_schedule = generate_full_schedule(group_a, group_b)  # Create full schedule
display_schedule(full_schedule)  # Display match schedule

# Play group stage matches
match_counter = 0
for match in full_schedule:
    print(f"\n--- Playing Match {match_counter + 1}: {match[0]} vs {match[1]} ---")
    toss_and_match_logic_with_tables(match, user_team, group_a_table, group_b_table)
    match_counter += 1

    # Display updated tables every two matches
    if match_counter % 2 == 0:
        print("\n--- Group Tables After Every Two Matches ---")
        print("\n--- Group A Table ---")
        display_group_table("Group A", group_a_table)
        print("\n--- Group B Table ---")
        display_group_table("Group B", group_b_table)


# Final Group Tables
print("\n--- Final Group Tables ---")
display_group_table("Group A", group_a_table)
display_group_table("Group B", group_b_table)

# Determine Semifinalists
team1, team2, team3, team4 = determine_semifinalists(group_a_table, group_b_table)

# Play Semifinals and Final
champion = play_semifinals_and_final(team1, team2, team3, team4, user_team)

# End of Tournament
print(f"\n--- Tournament Champion: {champion} ---")








# ----------------------------------------------------------------------------------------
# Objectives to add
# Improving the display of match results and tables.
# Adding difficulty levels for the AI teams.
# Adding Total Scores and individual performance of batters
# Allowing the user to name his 15 for the tournament
# Allowing user to make his 11 before the match and the option to use the previous eleven
# GUI For the entire game
# Integrate an option for odi world cup, t20 world cup, A test match or for a career mode
# designing the career mode and test match



# Points
# ISSUES:
# Group rankings should be changed based on the no of wins due to serial numbers this needs to be addressed







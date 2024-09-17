# main.py

from game_logic import initialize_game, update_state
from scenarios import (
    morning_routine, strange_occurrence, normal_day, encounter, reflect, dilemma, alternative_path, end
)
from utils import print_message, get_choice

def main():
    game_state = initialize_game()
    
    while game_state["current_scenario"] != "end":
        if game_state["current_scenario"] == "morning_routine":
            print_message(morning_routine())
        elif game_state["current_scenario"] == "strange_occurrence":
            print_message(strange_occurrence())
        elif game_state["current_scenario"] == "normal_day":
            print_message(normal_day())
        elif game_state["current_scenario"] == "encounter":
            print_message(encounter())
        elif game_state["current_scenario"] == "reflect":
            print_message(reflect())
        elif game_state["current_scenario"] == "dilemma":
            print_message(dilemma())
        elif game_state["current_scenario"] == "alternative_path":
            print_message(alternative_path())
        
        choices = ["investigate", "ignore", "follow", "stay", "talk", "keep to yourself", "engage", "walk_away", "ponder", "address", "accept", "reject", "explore"]
        choice = get_choice(choices)
        
        error = update_state(game_state, choice)
        if error:
            print_message(error)
        else:
            print_message("Proceeding to the next scenario...")
    
    print_message(end())

if __name__ == "__main__":
    main()


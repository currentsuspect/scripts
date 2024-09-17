# game_logic.py

def initialize_game():
    """Initialize the game state."""
    return {
        "current_scenario": "morning_routine",
        "choices_made": [],
        "memory": {}  # To remember player choices
    }

def update_state(game_state, choice):
    """Update game state based on the player's choice."""
    game_state["choices_made"].append(choice)
    
    if game_state["current_scenario"] == "morning_routine":
        if choice == "investigate":
            game_state["current_scenario"] = "strange_occurrence"
        elif choice == "ignore":
            game_state["current_scenario"] = "normal_day"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "strange_occurrence":
        if choice == "follow":
            game_state["current_scenario"] = "encounter"
        elif choice == "stay":
            game_state["current_scenario"] = "reflect"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "normal_day":
        if choice == "talk":
            game_state["current_scenario"] = "encounter"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "encounter":
        if choice == "engage":
            game_state["current_scenario"] = "dilemma"
        elif choice == "walk_away":
            game_state["current_scenario"] = "end"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "reflect":
        if choice == "ponder":
            game_state["current_scenario"] = "dilemma"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "dilemma":
        if choice == "accept":
            game_state["current_scenario"] = "end"
        elif choice == "reject":
            game_state["current_scenario"] = "alternative_path"
        else:
            return "Invalid choice. Try again."
    elif game_state["current_scenario"] == "alternative_path":
        if choice == "explore":
            game_state["current_scenario"] = "end"
        else:
            return "Invalid choice. Try again."

    return None


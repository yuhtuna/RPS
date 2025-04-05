import random
from abbey_counter import abbey_counter
from kris_counter import counter_kris


# Quincy pattern counter
def counter_quincy(prev_play):
    if player.prev_move == None:  
        return "P"  
    
    if prev_play == "R":
        return "P" 
    elif prev_play == "P":
        return "S" 
    else: 
        return "R"  
# Main player function
def player(prev_play, opponent_history=[], result=None):
    # Initialize persistent variables on first call
    if not hasattr(player, "losses"):
        player.losses = 0
        player.mode = "Abbey"
        player.prev_move = None

    # Determine if previous round was a loss
    if prev_play and player.prev_move:
        # Rock beats Scissors, Paper beats Rock, Scissors beats Paper
        win_conditions = {"R": "S", "P": "R", "S": "P"}
        if win_conditions.get(prev_play) == player.prev_move:
            player.losses += 1

    # Decide mode based on fixed loss thresholds
    # Reset losses when a new game starts
    if not prev_play:
        player.losses = 0
        print("New game detected - losses reset to 0")

    # Decide mode based on fixed loss thresholds
    if player.losses >= 200:
        player.mode = "Quincy"
    elif player.losses >= 150:
        player.mode = "Kris"
    else:
        player.mode = "Abbey"

    if player.mode == "Abbey":
        move = abbey_counter(opponent_history)
    elif player.mode == "Kris":
        move = counter_kris(prev_play)
    else:  # Quincy mode
        move = counter_quincy(prev_play)

    player.prev_move = move
    ### Debugger ###
    # print(f"Mode: {player.mode}, Losses: {player.losses}")
    return move

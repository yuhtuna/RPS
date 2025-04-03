import random
import numpy as np
from kris_counter import counter_kris
# Move mapping
move_map = {'R': 0, 'P': 1, 'S': 2}
reverse_map = {v: k for k, v in move_map.items()}

# Parameters
EXPLORATION_RATE = 0.02
TIE_THRESHOLD = 0.2  # Activate tie-breaker if ties exceed 20%
PATTERN_LENGTH = 2  # Length of history sequence to track
DETECTION_PHASE = 0.2  # First 20% of rounds for detection
KRIS_DETECTION_THRESHOLD = 0.6  # 60% of rounds countered for detection

# Tracking
tracker = {}
opponent_moves = {"R": 0, "P": 0, "S": 0}
our_moves = []  # Track our own moves
tie_count = 0
rounds_played = 0
kris_countered_count = 0  # Count of rounds where our move is countered
kris_detection_rounds = 0  # Total rounds considered for Kris detection

# Track detection status
our_last_move = None
kris_detected = False
abbey_detected = False

# Update tracker for opponent moves
def update_tracker(prev_play, opponent_history, result):
    global tie_count, rounds_played, kris_detected, kris_countered_count, kris_detection_rounds
    
    rounds_played += 1
    if result == 'tie':
        tie_count += 1
    
    if len(opponent_history) >= PATTERN_LENGTH:
        prev_sequence = "".join(opponent_history[-PATTERN_LENGTH:])
        tracker.setdefault(prev_sequence, {'R': 0, 'P': 0, 'S': 0})
        tracker[prev_sequence][prev_play] += 1
    
    opponent_moves[prev_play] += 1

    # Count how many times the last move was countered during detection phase
    if rounds_played <= int(DETECTION_PHASE * 1000):  # Assuming 1000 rounds
        kris_detection_rounds += 1
        if our_last_move and counter_move(our_last_move) == prev_play:
            kris_countered_count += 1

    # Determine if Kris is detected
    if kris_detection_rounds > 100 and kris_countered_count / kris_detection_rounds >= KRIS_DETECTION_THRESHOLD:
        kris_detected = True

    # Abbey Detection
    abbey_detected = is_low_variation()

# Detect repetitive players
def is_low_variation():
    total_moves = sum(opponent_moves.values())
    if total_moves == 0:
        return False
    
    max_freq = max(opponent_moves.values())
    return max_freq / total_moves > 0.9  # If 90% of moves are the same, it's likely Abbey

# Predict opponent move
def get_best_move(last_moves, opponent_history):
    if len(last_moves) < PATTERN_LENGTH:
        return random.choice(["R", "P", "S"])
    
    last_sequence = "".join(last_moves[-PATTERN_LENGTH:])
    if last_sequence not in tracker:
        return random.choice(["R", "P", "S"])
    
    move_counts = tracker[last_sequence]
    predicted_move = max(move_counts, key=move_counts.get)
    return predicted_move

# Choose counter move
def counter_move(move):
    return {"R": "P", "P": "S", "S": "R"}[move]

# Main player function
def player(prev_play, opponent_history=[], result=None):
    global our_last_move, kris_detected, abbey_detected
    
    # Handle the case where the first move is empty
    if prev_play:
        opponent_history.append(prev_play)
        update_tracker(prev_play, opponent_history, result)
    else:
        # If it's the first round, just play a random move
        our_last_move = random.choice(["R", "P", "S"])
        return our_last_move

    # If we have no history, play random
    if len(opponent_history) < PATTERN_LENGTH or random.random() < EXPLORATION_RATE:
        our_last_move = random.choice(["R", "P", "S"])
        return our_last_move

    predicted_move = get_best_move(opponent_history[-PATTERN_LENGTH:], opponent_history)

    # **Kris Exploit**: If Kris is detected, we can adapt our counter strategy
    if 1:
        if our_last_move is None:
            # If there's no last move, play randomly
            our_last_move = random.choice(["R", "P", "S"])
        else:
            # Counter Kris's expected move based on the last known move
            our_last_move = counter_move(prev_play)  # Counter the opponent's last move
        return our_last_move
    
    # **Abbey Exploit**: If Abbey is detected, disrupt the pattern
    if abbey_detected:
        if random.random() < 0.4:  # 40% chance to play randomly to disrupt
            our_last_move = random.choice(["R", "P", "S"])
        else:
            our_last_move = counter_move(predicted_move)  # Reverse Abbey's expected move
        return our_last_move
    
    # **Tie Breaker Mode**: If ties exceed 20%, shift strategy
    if rounds_played > 5 and tie_count / rounds_played > TIE_THRESHOLD:
        our_last_move = counter_move(random.choice(["R", "P", "S"]))  # Force a win over random ties
        return our_last_move
    
    # Normal counter move
    our_last_move = counter_move(predicted_move)
    return our_last_move

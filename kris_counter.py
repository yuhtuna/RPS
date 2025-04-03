def counter_kris(prev_play):
    # Initialize our strategy
    if not hasattr(counter_kris, "my_last_play"):
        counter_kris.my_last_play = "R"  # Start with Rock
    
    # Based on our last play, predict what kris will play next
    kris_ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    predicted_kris_play = kris_ideal_response.get(counter_kris.my_last_play, "R")
    
    # Choose the move that beats kris's predicted play
    our_ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    our_play = our_ideal_response[predicted_kris_play]
    
    # Update our last play for the next round
    counter_kris.my_last_play = our_play
    
    return our_play
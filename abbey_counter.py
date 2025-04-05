def abbey_counter(my_history=[]):


    # Manipulate Abbey's tracking by using a repeating pattern
    deception_cycle = ["S", "R", "P", "P", "R", "R", "S", "P"]  
    next_move = deception_cycle[len(my_history) % len(deception_cycle)]

    my_history.append(next_move)  # Track our plays

    return next_move
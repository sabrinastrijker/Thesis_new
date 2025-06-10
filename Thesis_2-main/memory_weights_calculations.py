def memory_weighted_score(memory_list, decay=0.8):
    """Calculates exponentially weighted sum of a memory list."""
    return sum((decay**i) * v for i, v in enumerate(memory_list))

def calculate_weights(memory_neighbors, memory_influencer, memory_self, decay=0.9):
    """Calculates normalized weights from memory lists."""
    # Avoid divide by zero by setting small value for empty lists
    C_n = memory_weighted_score(memory_neighbors, decay) if memory_neighbors else 1e-6
    C_inf = memory_weighted_score(memory_influencer, decay) if memory_influencer else 1e-6
    C_self = memory_weighted_score(memory_self, decay) if memory_self else 1e-6

    # print(C_n)
    
    total = C_n + C_inf + C_self
    # print(f"C_n: {C_n}, C_inf: {C_inf}, C_self: {C_self}, total: {total}")
    if total == 0:
        # print("hii")
        w_n = 1/3
        w_inf = 1/3
        w_self = 1/3
    else:
        # print("bye")
        w_n = C_n / total
        # print(f"neigbour{w_n}")

        w_inf = C_inf / total
        # print(f"influencer{w_inf}")
        w_self = C_self / total
        # print(f"self{w_self}")
    
    # print(f"Returned weights: neighbour {w_n}, influencer {w_inf}, self {w_self}")
    return w_n, w_inf, w_self

    # # If all memories are empty or all memory scores are zero, return equal weights
    # if (not memory_neighbors and not memory_influencer and not memory_self) or total == 0:
    #     w_n = w_inf = w_self = 1/3
    # else:
    #     w_n = C_n / total
    #     w_inf = C_inf / total
    #     w_self = C_self / total
    # # print(w_n)
    # return w_n, w_inf, w_self
        

    # # FULL safety: if total is zero, default to equal weights
    # if total == 0:
    #     w_n = w_inf = w_self = 1/3
    # else:
    #     w_n = C_n / total
    #     w_inf = C_inf / total
    #     w_self = C_self / total

    # print(w_n)
    # return w_n, w_inf, w_self
 

def update_participant_weights(participants_dict, decay=0.9):
    """Loops through participant dict, computes weights, and updates them."""
    for pid, info in participants_dict.items():
        memory_neighbors = info.get('memory_neighbors', [])
        # print(f'neighbours {memory_neighbors}')
        memory_influencer = info.get('memory_supervisor', [])
        # print(f'influencer {memory_influencer}')
        memory_self = info.get('memory_personal', [])
        # print(f'self {memory_self}')

        # print(memory_neighbors)
        
        w_n, w_inf, w_self = calculate_weights(memory_neighbors, memory_influencer, memory_self, decay)
        
        info['weight_neighbors'] = w_n
        info['weight_influencer'] = w_inf
        info['weight_self'] = w_self
    return participants_dict

# Usage:
# participants_dict = update_participant_weights(participants_dict, decay=0.8)

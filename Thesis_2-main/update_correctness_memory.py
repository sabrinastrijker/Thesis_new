def update_personal_correctness(agents_dict, old_price, new_price, correctness_key='memory_personal'):
    """
    For each agent, checks if their fundamental value prediction (with noise) correctly
    predicted the direction of price movement. Updates their correctness memory.
    """
    price_direction = 1 if new_price > old_price else 0  # 1=up, 0=down

    for agent in agents_dict.values():
        # Agent's predicted value
        predicted_value = agent['est_fundamental_value'] + agent['personal_noice_for_fundamental_value']
        advice = 1 if predicted_value > old_price else 0

        # Compare with actual movement
        correct = 1 if advice == price_direction else 0

        agent.setdefault(correctness_key, []).append(correct)
        agent[correctness_key] = agent[correctness_key][-20:]
    return agents_dict

def update_supervisor_correctness(agents_dict, old_price, new_price, correctness_key='memory_supervisor'):
    """
    For each agent, determine if the supervisor's prediction was correct.
    The supervisor predicts 'up' if supervisor_price > old_price, else 'down'.
    Actual market went up if new_price > old_price, else down.
    Appends 1 (correct) or 0 (wrong) to the agent's supervisor correctness memory.
    """
    actual_movement = 1 if new_price > old_price else 0  # 1 = up, 0 = down

    for agent in agents_dict.values():
        supervisor_pred = 1 if agent['supervisor_price'] > old_price else 0  # 1 = up, 0 = down
        correct = 1 if supervisor_pred == actual_movement else 0
        agent.setdefault(correctness_key, []).append(correct)
        agent[correctness_key] = agent[correctness_key][-20:]
    return agents_dict


def update_neighbors_correctness(agents_dict, old_price, new_price, memory_key='memory_neighbors'):
    """
    For each agent, determine if the MAJORITY of their neighbors' advice correctly predicted price movement.
    """
    
    price_direction = 1 if new_price > old_price else 0
    for agent in agents_dict.values():
        neighbors = agent.get('neighbors', [])
        if not neighbors:
            
            continue
        neighbor_advices = []
        for neighbor in neighbors:
            neighbor_agent = agents_dict[neighbor]
            neighbor_pred = neighbor_agent['est_fundamental_value'] #+ neighbor_agent['personal_noise_for_fundamental_value']
            neighbor_advice = 1 if neighbor_pred > old_price else 0
            neighbor_advices.append(neighbor_advice)
        if not neighbor_advices:
            continue
        # Majority vote
        majority_prediction = 1 if sum(neighbor_advices) > len(neighbor_advices) / 2 else 0
        correct = 1 if majority_prediction == price_direction else 0
        agent.setdefault(memory_key, []).append(correct)
        agent[memory_key] = agent[memory_key][-20:]
        agent[memory_key] = agent[memory_key][-20:]
        # print(f"Agent {agent} memory_neighbors length: {len(agent[memory_key])}")

    return agents_dict



# def update_neighbors_correctness(agents_dict, payoff_key='average_payoff_neighbours_total', memory_key='memory_neighbors'):
#     """
#     For each agent, check if average_payoff_neighbours_total is positive (1) or not (0).
#     Appends this to the agent's memory_neighbors list.
#     """
#     for agent in agents_dict.values():
#         payoff = agent.get(payoff_key, 0)
#         correct = 1 if payoff > 0 else 0
#         agent.setdefault(memory_key, []).append(correct)
#         agent[memory_key] = agent[memory_key][-7:]


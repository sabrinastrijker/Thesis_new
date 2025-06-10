# import math
# import random
# import numpy as np


import math
import re
import random

import mpmath
import numpy as np
from mpmath import mpf

def update_strategy_choices(data, alpha=1.0, phi=0.1):

    def transition_probability(pi_si, pi_sj):
        S = 1000000
        next = (S * (pi_si - pi_sj))
        exp_term = mpmath.exp(next)
        probability = (1 + exp_term) ** (-1)
        return probability

    def values_to_probabilities(values):
        arr = np.array(values, dtype=float)
        total = np.sum(arr)
        if total == 0:
            return np.ones_like(arr) / len(arr)
        return arr / total

    # def also_include_mutation_rate(probabilities, current_supervisor):
    #     mutation_rate = mpf('0.01')
    #     mutation_rate_2 = mpf('0.005')
    #     for idx in range(len(probabilities)):
    #         if (idx + 1) == current_supervisor:
    #             probabilities[idx] -= mutation_rate
    #         else:
    #             probabilities[idx] += mutation_rate_2
    #     return probabilities

    def get_range(random_number, probabilities):
        cumsum = np.cumsum(probabilities)
        for idx, val in enumerate(cumsum):
            if random_number < val:
                return idx + 1
        return len(probabilities)

    for key, value in data.items():
        current_strategy = value.get('strategy', 1)
        payoff_list = [
            value.get(f'average_payoff_neighbours_strat{h}', 0)
            for h in range(1, 3)
        ]

        # Calculate transition probabilities
        pi_1 = payoff_list[current_strategy - 1]
        transition_results = [
            transition_probability(pi_1, pi_2)
            for pi_2 in payoff_list
        ]

        # Apply mutation rate
        # mutated = also_include_mutation_rate(transition_results, current_strategy)

        # Convert to probability distribution
        probabilities = values_to_probabilities(transition_results)

        # Sample new supervisor
        random_number = np.random.rand()
        new_supervisor = get_range(random_number, probabilities)

        # Store result directly in the dict
        value['new_strategy'] = new_supervisor

        # for k2, v2 in data.items():
        #     if v2.get('supervisor_number') == new_supervisor:
        #         # Copy their variation_of_influencer and state
        #         value['price_error_of_new_supervisor'] = v2.get('supervisor_price_error')
        #         value['state_of_new_supervisor_to_follow'] = v2.get('supervisor_state')

    import pprint
    # pprint.pprint(data)
    return data


# def update_strategy_choices(agents_dict, alpha=1.0, phi=0.1):

#     def replicator_prob(current_payoff, other_payoff, S=1.0):
#         switch_cost = 10
#         # adjusted_other_payoff = max(other_payoff - switch_cost, 0)
#         adjusted_other_payoff = other_payoff - switch_cost
#         diff = current_payoff - adjusted_other_payoff
#         return 1 / (1 + np.exp(-S * diff))

#     for key, agent in agents_dict.items():
#         current_strategy = agent['strategy']
#         if current_strategy == 1:
#             current_payoff = agent['average_payoff_neighbours_strat1']
#             other_payoff = agent['average_payoff_neighbours_strat2']
#             alt_strategy = 2
#         else:
#             current_payoff = agent['average_payoff_neighbours_strat2']
#             other_payoff = agent['average_payoff_neighbours_strat1']
#             alt_strategy = 1

#         prob_stay = replicator_prob(current_payoff, other_payoff, S=1.0)

#         # Decide whether to switch or stay (stochastic update)
#         if np.random.random() < prob_stay:
#             agent['new_strategy'] = current_strategy
#         else:
#             agent['new_strategy'] = alt_strategy

#         # Optionally store the probability
#         agent['prob_stay_with_strategy'] = prob_stay

#     return agents_dict


# # def update_strategy_choices(agents_dict, alpha=1.0, phi=1.0):
# #     """
# #     Decide, probabilistically, if each agent should switch strategies using multinomial logit.

# #     Updates each agent's 'strategy' field in-place.
# #     Also can store probabilities for analysis if desired.
# #     """
# #     for key, agent in agents_dict.items():
# #         # For each possible strategy, calculate score
# #         strategy_scores = {}
# #         probabilities = {}

# #         for h in [1, 2]:  # Assuming only strategies 1 and 2
# #             # Own realized profit for strategy h (if not current, can be set to 0 or best-guess)
# #             # Here, we just use the agent's realized_profit for their current strategy
# #             # If you have historical profits per strategy, replace here accordingly
# #             if agent['strategy'] == h:
# #                 pi_i_h_t = agent.get('realized_profit', 0)
# #             else:
# #                 # If agent is not using this strategy, use 0 or a stored value if you have it
# #                 pi_i_h_t = 0

# #             # Average neighbor payoff for strategy h
# #             avg_pi_neigh_h = agent.get(f'average_payoff_neighbours_strat{h}', 0)
# #             # print(avg_pi_neigh_h)

# #             # Compute score for this strategy
# #             score = alpha * (pi_i_h_t + phi * avg_pi_neigh_h)
# #             # print(score)
# #             strategy_scores[h] = math.exp(score)

# #         # Denominator: sum over strategies
# #         denom = sum(strategy_scores.values())

# #         # Probabilities for each strategy
# #         for h in [1, 2]:
# #             probabilities[h] = strategy_scores[h] / denom if denom > 0 else 0.5  # avoid div by zero

# #         # Optionally store probabilities for analysis
# #         agent['strategy_probabilities'] = probabilities

# #         # Sample new strategy
# #         rand_val = random.random()
# #         if rand_val < probabilities[1]:
# #             new_strategy = 1
# #         else:
# #             new_strategy = 2

# #         agent['new_strategy'] = new_strategy  # Update with proposed strategy

# #     # Optional: To actually switch, you can update 'strategy' field here or in a separate step
# #     # for agent in agents_dict.values():
# #     #     agent['strategy'] = agent['new_strategy']


import math
import re
import random

import mpmath
import numpy as np
from mpmath import mpf

import math
import random
import numpy as np
import mpmath

def add_new_supervisor(data, supervisor_range):
    """
    For each agent, probabilistically select a new influencer to follow
    based ONLY on the set of influencers present in their neighbors
    (i.e., those for which 'average_payoff_neighbour_influencer_{h}' exists in the agent dict).
    """
    def transition_probability(pi_si, pi_sj, S=1.0):
        S = 1000000
        # A reasonable S; adjust as needed
        diff = S * (pi_si - pi_sj)
        try:
            exp_term = math.exp(diff)
        except OverflowError:
            exp_term = float('inf') if diff > 0 else 0.0
        probability = 1 / (1 + exp_term)
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
                return idx
        return len(probabilities) - 1

    for key, value in data.items():
        current_supervisor = value.get('supervisor_number', 1)

        # Gather only valid neighbor influencer payoffs
        payoff_list = []
        available_h = []
        for k in value:
            if k.startswith('average_payoff_neighbour_influencer_'):
                h = int(k.split('_')[-1])
                payoff_list.append(value[k])
                available_h.append(h)

        if not payoff_list:
            # No neighbor influencer payoffs: stay with current
            value['new_supervisor_to_follow'] = current_supervisor
            continue

        # Find current supervisor in available_h
        try:
            current_index = available_h.index(current_supervisor)
        except ValueError:
            current_index = 0  # If not among available, just pick first

        pi_1 = payoff_list[current_index]
        transition_results = [
            transition_probability(pi_1, pi_2)
            for pi_2 in payoff_list
        ]


        # Apply mutation rate
        # mutated = also_include_mutation_rate(transition_results, current_supervisor)

        probabilities = values_to_probabilities(transition_results)
        random_number = np.random.rand()
        chosen_idx = get_range(random_number, probabilities)
        new_supervisor = available_h[chosen_idx]
        value['new_supervisor_to_follow'] = new_supervisor

        # Copy variation_of_influencer and state from chosen influencer
        for v2 in data.values():
            if v2.get('supervisor_number') == new_supervisor:
                value['price_error_of_new_supervisor'] = v2.get('supervisor_price_error')
                value['state_of_new_supervisor_to_follow'] = v2.get('supervisor_state')
                break

    return data


# def add_new_supervisor(data, supervisor_range):

#     def transition_probability(pi_si, pi_sj):
#         S = 10**10
#         next = (S * (pi_si - pi_sj))
#         exp_term = mpmath.exp(next)
#         probability = (1 + exp_term) ** (-1)
#         return probability

#     def values_to_probabilities(values):
#         arr = np.array(values, dtype=float)
#         total = np.sum(arr)
#         if total == 0:
#             return np.ones_like(arr) / len(arr)
#         return arr / total

#     def also_include_mutation_rate(probabilities, current_supervisor):
#         # mutation_rate = mpf('0.01')
#         # mutation_rate_2 = mpf('0.005')
#         # for idx in range(len(probabilities)):
#         #     if (idx + 1) == current_supervisor:
#         #         probabilities[idx] -= mutation_rate
#         #     else:
#         #         probabilities[idx] += mutation_rate_2
#         return probabilities

#     def get_range(random_number, probabilities):
#         cumsum = np.cumsum(probabilities)
#         for idx, val in enumerate(cumsum):
#             if random_number < val:
#                 return idx + 1
#         return len(probabilities)

#     for key, value in data.items():
#         current_supervisor = value.get('supervisor_number', 1)
#         payoff_list = [
#             value.get(f'average_payoff_neighbour_influencer_{h}', 0)
#             for h in range(1, supervisor_range + 1)
#         ]

#         # Calculate transition probabilities
#         pi_1 = payoff_list[current_supervisor - 1]
#         transition_results = [
#             transition_probability(pi_1, pi_2)
#             for pi_2 in payoff_list
#         ]

#         # Apply mutation rate
#         mutated = also_include_mutation_rate(transition_results, current_supervisor)

#         # Convert to probability distribution
#         probabilities = values_to_probabilities(mutated)

#         # Sample new supervisor
#         random_number = np.random.rand()
#         new_supervisor = get_range(random_number, probabilities)

#         # Store result directly in the dict
#         value['new_supervisor_to_follow'] = new_supervisor

#         for k2, v2 in data.items():
#             if v2.get('supervisor_number') == new_supervisor:
#                 # Copy their variation_of_influencer and state
#                 value['price_error_of_new_supervisor'] = v2.get('supervisor_price_error')
#                 value['state_of_new_supervisor_to_follow'] = v2.get('supervisor_state')

#     import pprint
#     # pprint.pprint(data)
#     return data


# def update_influencer(agents_dict, alpha=1.0, phi=0.3):
#     """
#     For each agent, use both personal and average influencer payoff to update influencer.
#     """
#     for agent in agents_dict.values():
#         # 1. Find all influencer numbers
#         influencer_payoffs = {}
#         for key in agent:
#             match = re.match(r'average_payoff_neighbour_influencer_(\d+)', key)
#             if match:
#                 h = int(match.group(1))
#                 # Look for personal payoff as well
#                 personal_key = f'personal_payoff_influencer_{h}'
#                 personal_payoff = agent.get(personal_key, 0)
#                 avg_payoff = agent[key]
#                 influencer_payoffs[h] = (personal_payoff, avg_payoff)
        
#         # 2. Calculate scores
#         scores = {}
#         for h, (personal, avg) in influencer_payoffs.items():
#             score = alpha * (personal + phi * avg)
#             scores[h] = math.exp(score)
        
#         # 3. Normalize to probabilities
#         total = sum(scores.values())
#         probabilities = {h: (scores[h]/total if total > 0 else 1/len(scores)) for h in scores}
        
#         # 4. Store probabilities
#         agent['influencer_probabilities'] = probabilities

#         # 5. Sample new influencer
#         rnd = random.random()
#         cumulative = 0.0
#         selected = None
#         for h, prob in sorted(probabilities.items()):
#             cumulative += prob
#             if rnd <= cumulative:
#                 selected = h
#                 break
#         if selected is None:
#             selected = max(probabilities, key=probabilities.get)
#         agent['new_supervisor_to_follow'] = selected

#         state = None

#         for other_agent in agents_dict.values():
#             if other_agent.get('supervisor_number') == selected:
#                 state = other_agent.get('supervisor_state')
#                 variation_of_influencer = other_agent.get('supervisor_price_error')
#                 break
#         agent['price_error_of_new_supervisor'] = variation_of_influencer
#         agent['state_of_new_supervisor_to_follow'] = state



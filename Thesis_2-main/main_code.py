import pprint
import csv
import pandas as pd
import random
import numpy as np
import os
np.random.seed(1)

from matrix_generator import generate_matrix # type: ignore
from new_fundamental_value import calculate_fundamental_value, update_fundamental_value_with_noice, update_price_estimation_for_influencers, update_average_fundamental_value_neighbors, update_estimated_fundamental_value # type: ignore
from demand_of_funamentalisits_and_trend_chasers import calculate_share_demand, aggregate_excess_demand # type: ignore
from new_price_and_proffits import update_price, calculate_realized_profits # type: ignore
from restructure_and_get_neighbours import maak_matrix, get_neighbors_dict # type: ignore
from calculate_neighbour_payoffs import overview, average_payoff_neighbour_influencers # type: ignore
from update_new_strategy_based_on_neighbour import update_strategy_choices # type: ignore
from update_correctness_memory import update_personal_correctness, update_supervisor_correctness, update_neighbors_correctness # type: ignore
from memory_weights_calculations import update_participant_weights # type: ignore
from update_new_influencer_to_follow import add_new_supervisor # type: ignore 'update_influencer,'
from reset_dict_for_new_iteration import update_agent_strategy_and_supervisor # type: ignore
from visualisation_of_data import plot_new_strategy, plot_supervisor_matrix # type: ignore


# Initialise the matrix with all the information needed:

participant_id = 1  # Initialize participant ID for each matrix



""" 
this function will initialise the matrix of participants as
a dict with all information that is needed in this case
"""

def generate_matrices_part1(M, participant_id, R):
    matrices = []
    for index in range(M):
        gen_matrix = generate_matrix(participant_id, index + 1, R)
        matrices.append(gen_matrix)
        participant_id += R*R   # Increment participant ID for the next matrix
    
    return matrices
 
 

def process_match_data(match_dict, gen_matrix):
    original_dict = gen_matrix.copy()
    updated_dict = {}

    for key, value in original_dict.items():
        participant_id = value.pop('participant_id')
        value['participant_location'] = key
        updated_dict[participant_id] = value

    data = updated_dict

    match_strategy_map = {}
    for participant_id, participant_data in data.items():
        match_id = participant_data['match_id'][0]
        for match_participant_id, match_participant_data in data.items():
            if match_participant_data['participant_location'] == match_id:
                match_strategy_map[match_id] = match_participant_data['strategy']
                break

    for participant_id, participant_data in data.items():
        match_id = participant_data['match_id'][0]
        participant_data['match_strategy'] = match_strategy_map.get(match_id, None)

    return data



def filter_values(dictionary):
    filtered_dict = {}
    for key, values in dictionary.items():
        filtered_values = [value[1] if value[0] == key else value[0] for value in values]
        filtered_dict[key] = filtered_values
    return filtered_dict

def combineer():
    pass



def run_simulation(a2=1, theta=1.2, sigma=0.5, mu=0.004, *,
                   S=150, N=30, price_noise=1, output_csv=None):
    """Run the simulation with the provided parameters and save to ``output_csv``.

    Parameters
    ----------
    a2, theta, sigma, mu : float
        Key model parameters.
    S : int
        Number of periods.
    N : int
        Number of simulations.
    price_noise : float
        Noise factor added to the price estimation.
    output_csv : str
        Path of the CSV file to write results to. If ``None`` a file will be
        created under ``results/Impact_of_price_noice``.
    """
    print("hi")

    memory = 20  # normal = 20

    print(f"a2 = {a2}")
    print(f"theta = {theta}")
    print(f"sigma = {sigma}")
    print(f"mu is {mu}")
    print(f"memory is {memory}")
    print(f"price noice = {price_noise}")

    fieldnames = ['simulation','period', 'agent_id', 'supervisor_number', 'share_demand',
                  'realized_profit', 'strategy', 'weight_influencer', 'weight_neighbors',
                  'weight_self', 'supervisor_price', 'est_fundamental_value', 'price','strategy_history',
                        'supervisor_numer_history', 'personal_noice_for_fundamental_value']

    os.makedirs('results/Impact_of_price_noice', exist_ok=True)
<<<<<<< ours

    with open(f'results/Impact_of_price_noice/price_noice_is_{price_noice_for_person}.csv', 'w', newline='') as csvfile:
=======
    if output_csv is None:
        output_csv = (
            f"results/Impact_of_price_noice/"
            f"price_noice_is_{price_noise}_a2_{a2}_theta_{theta}_sigma_{sigma}_mu_{mu}.csv"
        )
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    with open(output_csv, 'w', newline='') as csvfile:
>>>>>>> theirs
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        

    fundamental_value_previous_period = 100
    fundamental_value_previous_period_for_influencer = 100
    # current market price:
    p_t = 100

    # Extra kosten die iemand betaald om het advies van een goede influencer te volgen
    extra_for_good_inflencer = 3

    M = 16

    # while True:
    #     M = int(input("Enter the number of influencers (M): "))
    #     if M in [4, 9, 16, 25, 36]:
    #         break
    #     else:
    #         print("Invalid input. Please enter one of the allowed numbers: 4, 9, 16, 25, 36.")

    # (participant rate is how many participants an influencer wil oversee initially)
    R = 4 #int(input("Enter the participant rate (2X2, 4X4, or 6X6): "))

    for simulation_number in range(N):    
        """ Step 1: initialise the matrix """

        # Initialise the matrix of the participants with all information needed
        first_matrix = generate_matrices_part1(M, participant_id, R)

        first_matrix = {k: v for d in first_matrix for k, v in d.items()}

        
        history = []

            
        fundamental_value_previous_period = 100
        fundamental_value_previous_period_for_influencer = 100
        # current market price:
        p_t = 100
            



    #####################################################
    ######################################################
    ######################################################3
    #####################################################

        # """Make sure all information will be saved correctly"""
        #     # Specify the filename for the CSV
        # csv_filename = f'test_result_M_is_{M}_R_is_{R}.csv'
        # # Open the CSV file in write mode
        #     # Open the CSV file in write mode
        # with open(csv_filename, mode='w', newline='') as file:
        #     writer = csv.writer(file)
        

        for index in range(S):

            """Step: Set a schock value only the influencers will observe"""


            shock_value_for_influencers = random.gauss(0, 5)
            # print(shock_value_for_influencers)

            """Step 2: Set a new fundamental value """
            

            # set the new fundamental value
            fundamental_value_new_period = calculate_fundamental_value(fundamental_value_previous_period)
            
            fundamental_value_new_period_for_influencer = calculate_fundamental_value(fundamental_value_previous_period_for_influencer)
            # print(f"fundamental value period {index} is {fundamental_value_new_period_for_influencer}")

            # reset the old fundamental value for the next period
            fundamental_value_previous_period_for_influencer = fundamental_value_new_period_for_influencer + shock_value_for_influencers
            
            fundamental_value_previous_period = fundamental_value_new_period

            

            """Step : Set the new price forecasted by the supervisor depending on the supervisor state"""

            # Get the fundamental value of the next period:
            # set the new fundamental value
            fundamental_value_for_forecast_of_influencers = calculate_fundamental_value(fundamental_value_previous_period_for_influencer)
            
            # add the error for every influencer
            first_matrix = update_price_estimation_for_influencers(first_matrix, fundamental_value_for_forecast_of_influencers)
            # print(f"later fundamental value {fundamental_value_for_forecast_of_influencers}")
            

            """ step: visualise the results"""
            if simulation_number == 1:

                plot_new_strategy(R, M, first_matrix, N, index)
                plot_supervisor_matrix(R, M, first_matrix, N, index)


            """ Step 3: Calculate a new personal fundamental value with noice"""

            # update the fundamental value with the noice for the participants
            first_matrix = update_fundamental_value_with_noice(first_matrix, fundamental_value_new_period)
            # pprint.pprint(first_matrix)

            """ stap: restructure the matrix om de average fundamental value van de neigbours te vinden"""
            # restructure the matrix to have the correct locations for the participant number in the grid
            location_of_participant_number_matrix = maak_matrix(R, M)
            # pprint.pprint(location_of_participant_number_matrix)

            # maak een apparte dict met alle apparte neighbours voor iedere agent
            dict_which_agents_are_neighbours = get_neighbors_dict(location_of_participant_number_matrix)
            # pprint.pprint(dict_which_agents_are_neighbours)

            """ stap: vind de average fundamental value van de neighbours"""
            data = update_average_fundamental_value_neighbors(first_matrix, dict_which_agents_are_neighbours)
            # pprint.pprint(data)

            # update the price estimation using the formula with the weights.
            first_matrix = update_estimated_fundamental_value(data, fundamental_value_new_period)
            # pprint.pprint(first_matrix)


            """ Step 4: Calculate the demand for the shares of the fundamentalisis 
            and the trend chasers based on the price and fundamental value"""

            first_matrix = calculate_share_demand(
            first_matrix, 
            p_t,             # Current market price
            a1=4,            # Risk aversion, fundamentalist [2,10]
            a2=1,            # Risk aversion, trend chaser [0.5,3]
            sigma2=sigma,        # Variance of excess returns
            R=1.01,          # Gross risk-free rate
            theta = theta,       # Trend chasing intensity
            b=0.8,             # Weight for moving average
            L=7,             # Window size for trend signal
            omega_k=None     # Weights for moving average
            ) 
            

            """ Step 5: Set the new price"""

            # calculate the excess demand of the share:
            total_excess_demand = aggregate_excess_demand(first_matrix)
            # print(total_excess_demand)

            # set the new price acording to the formula
            new_price = update_price(p_t, total_excess_demand, mu = mu)
            # print(new_price)

            """Step: calculate the realised proffits"""
            first_matrix = calculate_realized_profits(first_matrix, extra_for_good_inflencer,  R= 1.01, delta_t=1)
            # pprint.pprint(first_matrix)


            """ Step 6: Find the values of the neighbours and the strategies 
            to calculate how well they did per strategy"""

            # bereken alle neighbour payoffs per strategy
            dict_with_neigbour_payoffs = overview(first_matrix, dict_which_agents_are_neighbours)
            # pprint.pprint(dict_with_neigbour_payoffs)


            """ Step 7: Decide wether to swich strategies for price calculations based on 
            neighbours strategy"""

            # here a neighbour will decide to swich or not
            dict_with_neigbour_payoffs = update_strategy_choices(dict_with_neigbour_payoffs, alpha=1.0, phi=0.5)
            # pprint.pprint(dict_with_neigbour_payoffs)
            

            """ Step : Update your memory on wether or not you, your neighbour, or your influencer is correct"""

            # update personal memory of if your signal was correct or not
            dict_with_neigbour_payoffs = update_personal_correctness(dict_with_neigbour_payoffs, p_t, new_price, correctness_key='memory_personal')

            # update influencer memory of if their signal was correct or not
            dict_with_neigbour_payoffs = update_supervisor_correctness(dict_with_neigbour_payoffs, p_t, new_price, correctness_key='memory_supervisor')
            

            # update neighbour memory of if their signal was correct or not. 
            # this is just looking at wether the 'average_payoff_neighbours_total' is positive or negative 
            for agent_id, agent in dict_with_neigbour_payoffs.items():
                agent['neighbors'] = dict_which_agents_are_neighbours.get(agent_id, [])

            dict_with_neigbour_payoffs = update_neighbors_correctness(dict_with_neigbour_payoffs, p_t, new_price, memory_key='memory_neighbors')
            # update_neighbors_correctness(dict_with_neigbour_payoffs, payoff_key='average_payoff_neighbours_total', memory_key='memory_neighbors')
            
            """ Step 8: Update the credability weights for you, your neighbour, and your influencer,"""

            # update the weights
            participants_dict = update_participant_weights(dict_with_neigbour_payoffs, decay=0.8)
            # pprint.pprint(participants_dict)

            """ Step 9: Find the value of the neighbour influencers per influencer"""

            # calculate for now without memory
            participants_dict = average_payoff_neighbour_influencers(participants_dict, dict_which_agents_are_neighbours)
            

            """ step 10: Decide wether to swich influencers to one of your neighbours"""

            participants_dict = add_new_supervisor(participants_dict, supervisor_range=M)

            for agent in participants_dict.values():
                agent['strategy_history'].append(agent['strategy'])
                agent['supervisor_numer_history'].append(agent['supervisor_number'])

            # update_influencer(participants_dict, alpha=1.0, phi=0.1)
            # pprint.pprint(participants_dict)

            """ Step 11: save all information for later analisis"""

            dict_to_use_for_saving_data = participants_dict
            # pprint.pprint(dict_to_use_for_saving_data)

            for agent_id, agent in dict_to_use_for_saving_data.items():
                agent['price'] = p_t


            for agent_id, agent in dict_to_use_for_saving_data.items():
                history.append({
                    'simulation': simulation_number,
                    'period': index,
                    'agent_id': agent_id,
                    'supervisor_number': agent['supervisor_number'],
                    'share_demand': agent['share_demand'],
                    'realized_profit': agent['realized_profit'],
                    'strategy': agent['strategy'],
                    'weight_influencer': agent['weight_influencer'],
                    'weight_neighbors': agent['weight_neighbors'],
                    'weight_self': agent['weight_self'],
                    'supervisor_price': agent['supervisor_price'],
                    'est_fundamental_value': agent['est_fundamental_value'],
                    'price': agent['price'],
                    'strategy_history': agent['strategy_history'],
                    'supervisor_numer_history': agent['supervisor_numer_history'],
                    'personal_noice_for_fundamental_value': agent['personal_noice_for_fundamental_value']
                })
            
            """ Step 12: reset the game for a new itteration """

            # fundamental value is already reset. 
            # I need to reset p_t to the value of new_price
            p_t = new_price
            # I need to reset the strategy to new strategy in the dict
            # I need to set the supervisor_number to new_supervisor_to_follow 
            for agent_id, agent in dict_to_use_for_saving_data.items():
                agent['price'] = p_t

            participants_dict = update_agent_strategy_and_supervisor(participants_dict)

            
            # pprint.pprint(participants_dict)

            """step: delete more data to get for the new itteration"""
            for agent in participants_dict.values():
                agent['average_payoff_neighbours_strat1'] = -float('inf')
                agent['average_payoff_neighbours_strat2'] = -float('inf')
                agent['average_payoff_neighbours_total'] = -float('inf')
                agent['new_strategy'] = None
                agent['new_supervisor_to_follow'] = None
                agent['price_error_of_new_supervisor'] = None
                agent['state_of_new_supervisor_to_follow'] = None





                # Collect all keys to remove first to avoid modifying dict while iterating
                keys_to_remove = [k for k in agent if k.startswith('average_payoff_neighbour_influencer_')]
                for k in keys_to_remove:
                    del agent[k]
            


            # pprint.pprint(participants_dict)
            " Step: Set new dict to old dict"

            # first_matrix = participants_dict
            # pprint.pprint(participants_dict)

            # """ step: visualise the results"""
            # plot_new_strategy(R, M, first_matrix, N, index)
            # plot_supervisor_matrix(R, M, first_matrix, N, index)

            first_matrix = participants_dict
            # pprint.pprint(participants_dict)

        print(simulation_number)

                        
        # Save to CSV at the end
        # fieldnames = ['simulation','period', 'agent_id', 'supervisor_number', 'share_demand', 'realized_profit', 'strategy', 'weight_influencer', 'weight_neighbors', 'weight_self', 'supervisor_price ]
        with open(output_csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #   writer.writeheader()
            writer.writerows(history)



if __name__ == "__main__":
    run_simulation()

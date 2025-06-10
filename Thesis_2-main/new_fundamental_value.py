import numpy as np

def calculate_fundamental_value(fundamental_value_previous_period):
    """I will use a random walk with drift to get an estimate of the 
    fundamental value of an asset"""

    mu = 0.001  # Drift
    sigma_eta = 0.03

    eta_t = np.random.normal(0, sigma_eta)

    fundamental_value_new_period = fundamental_value_previous_period #+ mu + eta_t

    return fundamental_value_new_period

def update_fundamental_value_with_noice(matrices, fundamental_value_new_period):
    data = matrices

    for key, value in data.items():
        value['est_fundamental_value'] = fundamental_value_new_period + value['personal_noice_for_fundamental_value']

    return data

def update_price_estimation_for_influencers(matrices, fundamental_value_for_forecast_of_influencers):
    data = matrices

    for key, value in data.items():
        value['supervisor_price'] = fundamental_value_for_forecast_of_influencers + value['supervisor_price_error']
       
    return data


def update_average_fundamental_value_neighbors(data_values, numbers_dict):
    """
    For each agent, calculate the average fundamental value of their neighbors.
    Sets 'average_fundamental_value_neighbors' in the agent's dictionary.
    
    Args:
        data_values: main dict, keyed by agent number, with agent data dicts.
        numbers_dict: dict mapping each agent's id to a list of their neighbors' ids.
    """
    for agent_id, neighbor_ids in numbers_dict.items():
        neighbor_values = [
            data_values[nid]['est_fundamental_value'] + data_values[nid].get('personal_noice_for_fundamental_value', 0)
            for nid in neighbor_ids if nid in data_values
        ]
        if neighbor_values:
            avg_fundamental = sum(neighbor_values) / len(neighbor_values)
        else:
            avg_fundamental = 0  # or np.nan if you prefer
        
        data_values[agent_id]['average_fundamental_value_neighbors'] = avg_fundamental
    
    return data_values


def update_estimated_fundamental_value(agents_dict, fundamental_value_new_period):
    """
    Updates the estimated fundamental value for each agent according to the formula:
    p_new = w_n * neighbors_signal + w_inf * influencer_signal + w_self * personal_value
    """
    for agent in agents_dict.values():
        w_n = agent.get('weight_neighbors', 0)
        w_inf = agent.get('weight_influencer', 0)
        w_self = agent.get('weight_self', 0)

        # You need to have these in your agent dict!
        neighbors_signal = agent.get('average_fundamental_value_neighbors', 0)
        influencer_signal = agent.get('supervisor_price', 0)

        personal_value = fundamental_value_new_period + agent['personal_noice_for_fundamental_value']
        #agent['est_fundamental_value'] # + agent['personal_noice_for_fundamental_value']

        p_new = w_n * neighbors_signal + w_inf * influencer_signal + w_self * personal_value


        agent['est_fundamental_value'] = p_new  # store the new estimated fundamental value
    return agents_dict

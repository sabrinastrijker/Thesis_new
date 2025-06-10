import random
import numpy as np

def generate_matrix(participant_id, supervisor_number, R):
    matrix = {}
    current_participant = 1
    supervisor_state = round(random.random())
    
    # create the correctness of a supervisor depending on the error that you get
    if supervisor_state == 1:
        supervisor_error = round(random.uniform(- 0.2, 0.2), 2)
    else:
        supervisor_error = round(random.uniform(-1, 1), 2)

    for i in range(R):
        for j in range(R):            
            matrix[participant_id] = {
                "participant_id": participant_id,
                "participant_location": (i, j),
                "strategy": random.randint(1, 2),  # 1 = fundamentalist, 2 = trend chaser
                "realized_profit": 0,
                "supervisor_number": supervisor_number,
                "supervisor_state": supervisor_state, 
                "supervisor_price_error": supervisor_error,
                "supervisor_price": 0,

                "average_payoff_neighbours_strat1": 0,
                "average_payoff_neighbours_strat2": 0,
                "new_strategy": None,
                

                "new_strategy_participant": None,
                "new_supervisor_to_follow": None,
                
               # "wealth": 1000.0,  # or initial wealth
                "shares": 0.0,
                "personal_noice_for_fundamental_value": np.random.normal(-0.1, 0.1),
                "weight_self": (1/3),       # Can tune initialization
                "weight_neighbors": (1/3),  # Can tune initialization
                "weight_influencer": (1/3), # Can tune initialization
                "est_fundamental_value": 0.0,
                "memory_personal": [1] + [random.randint(0, 1) for _ in range(6)],
                "memory_neighbors": [1] + [random.randint(0, 1) for _ in range(6)],
                "memory_supervisor": [1] + [random.randint(0, 1) for _ in range(6)],

                # "memory_personal": [1,1,1],
                # "memory_neighbors": [1,1,1],
                # "memory_supervisor": [1,1,1],
                "supervisor_numer_history": [],
                "profit_history": [],
                "strategy_history": [],
                "price_deviation_history": [], # for the fundamentalists calculations
                "share_demand_history": []
                

            }

            # print(participant_id, supervisor_number)
            participant_id += 1  # Increment participant ID for each cell
        current_participant += R
    return matrix
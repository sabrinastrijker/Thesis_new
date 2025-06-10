def calculate_share_demand(
    agents_dict, 
            p_t,             # Current market price
            a1=4,            # Risk aversion, fundamentalist
            a2=1,            # Risk aversion, trend chaser
            sigma2=1,        # Variance of excess returns
            R=1.01,          # Gross risk-free rate
            theta=1.2,       # Trend chasing intensity
            b=1,             # Weight for moving average
            L=3,             # Window size for trend signal
            omega_k=None     # Weights for moving average
):
    # # Default weights if none are given
    # if omega_k is None:
    #     omega_k = [0.5, 0.3, 0.2]  # Should sum to 1, length L

    if omega_k is None:
    # Exponential weights as default, can change beta as needed
        beta = b
        omega_k = [beta ** k for k in range(L)]
        total = sum(omega_k)
        omega_k = [w / total for w in omega_k]  # Normalize

    for key, agent in agents_dict.items():
        # Calculate price deviation
        p_star = agent['est_fundamental_value']
        x_t = p_t - p_star

        # Append to price deviation history
        if 'price_deviation_history' not in agent:
            agent['price_deviation_history'] = []
        agent['price_deviation_history'].append(x_t)
        # Keep only the last L values
        if len(agent['price_deviation_history']) > L:
            agent['price_deviation_history'] = agent['price_deviation_history'][-L:]

        # Fundamentalist agent
        if agent['strategy'] == 1:
            z_f = (-R * x_t) / (a1 * sigma2)
            agent['share_demand'] = z_f  # Store demand in agent dict
        # Trend chaser agent
        elif agent['strategy'] == 2:
            # Calculate g_{i,t} (trend signal, weighted moving average)
            history = agent['price_deviation_history']
            # Ensure enough history, pad with current x_t if necessary
            if len(history) < L:
                padded_history = [history[0]] * (L - len(history)) + history
            else:
                padded_history = history[-L:]
            # Weighted sum
            g_it = b * sum(omega_k[k] * padded_history[-(k+1)] for k in range(L))
            z_trend = (theta * g_it - R * x_t) / (a2 * sigma2)
            agent['share_demand'] = z_trend  # Store demand in agent dict

        agent['share_demand_history'].append(agent.get('share_demand', 0))
        # Keep only the last 10 entries
        if len(agent['share_demand_history']) > 3:
            agent['share_demand_history'] = agent['share_demand_history'][-3:]


        # Optionally: else, handle other agent types

    # Return dict is mutated in place; could return it for chaining
    return agents_dict


def aggregate_excess_demand(agents_dict):
    return sum(agent.get('share_demand', 0) for agent in agents_dict.values())

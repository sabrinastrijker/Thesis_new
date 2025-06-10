import random

def update_price(p_t, excess_demand, mu):
    """
    Updates the price of the risky asset.

    Args:
        p_t (float): Current price at time t.
        excess_demand (float): Aggregate excess demand at time t.
        mu (float): Market friction (speed of price adjustment).
    Returns:
        float: New price at time t+1.
    """
    return p_t + mu * excess_demand


def calculate_realized_profits(agents_dict, extra_for_good_inflencer, R, delta_t=0):
    """
    Calculate and store realized profits for each agent.

    Args:
        agents_dict (dict): Dictionary of agents.
        R (float): Gross risk-free rate.
        delta_t (float, optional): Martingale difference shock (default 0).

    Modifies:
        Each agent dict gains 'realized_profit' and updates 'profit_history'.
    """

    for agent in agents_dict.values():
        # Make sure histories exist and have at least 2 elements
        price_devs = agent.get('price_deviation_history', [])
        share_history = agent.get('share_demand_history', [])

        # Default profit is 0
        realized_profit = 0

        if len(price_devs) >= 2 and len(share_history) >= 2:
            x_t = price_devs[-1]
            x_t_minus_1 = price_devs[-2]
            z_t_minus_1 = share_history[-2]

            # For both types, profit formula is the same!
            realized_profit = (x_t - R * x_t_minus_1 + delta_t) * z_t_minus_1

            # Apply extra cost if supervisor_state is 1
            if agent.get('supervisor_state', 0) == 1:
                realized_profit -= extra_for_good_inflencer
                
        # Store realized profit in dict and append to history
        agent['realized_profit'] = realized_profit
        if 'profit_history' not in agent:
            agent['profit_history'] = []
        agent['profit_history'].append(realized_profit)
        agent['profit_history'] = agent['profit_history'][-7:]
    
    return agents_dict




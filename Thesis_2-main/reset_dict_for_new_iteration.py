def update_agent_strategy_and_supervisor(agents_dict):
    """
    For each agent:
      - Set 'strategy' to 'new_strategy' if it exists.
      - Set 'supervisor_number' to 'new_supervisor_to_follow' if it exists.
    """
    for agent in agents_dict.values():
        # Update strategy if 'new_strategy' is present (and not None)
        if 'new_strategy' in agent and agent['new_strategy'] is not None:
            agent['strategy'] = agent['new_strategy']
        
        # Update supervisor_number if 'new_supervisor_to_follow' is present (and not None)
        if 'new_supervisor_to_follow' in agent and agent['new_supervisor_to_follow'] is not None:
            agent['supervisor_number'] = agent['new_supervisor_to_follow']

        if 'state_of_new_supervisor_to_follow' in agent and agent["state_of_new_supervisor_to_follow"] is not None:
            agent["supervisor_state"] = agent["state_of_new_supervisor_to_follow"]

        if 'price_error_of_new_supervisor' in agent and agent["price_error_of_new_supervisor"] is not None:
            agent["supervisor_price_error"] = agent["price_error_of_new_supervisor"]
    return(agents_dict)

        
        

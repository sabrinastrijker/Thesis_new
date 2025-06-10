

def overview(data_values, numbers_dict):


    def calculate_average_payoff_per_strategy(extracted_values):
        payoffs_per_strategy = {}
        strategy_count = {}

        for item in extracted_values:
            strategy = item['strategy']
          
            payoff = item['realized_profit']
            if strategy in payoffs_per_strategy:
                payoffs_per_strategy[strategy] += payoff
                strategy_count[strategy] += 1
            else:
                payoffs_per_strategy[strategy] = payoff
                strategy_count[strategy] = 1

        average_payoff_per_strategy = {}
        for strategy, total_payoff in payoffs_per_strategy.items():
            count = strategy_count[strategy]
            average_payoff_per_strategy[strategy] = total_payoff / count

        return average_payoff_per_strategy

    # def extract_values_by_numbers(data_values, numbers_dict):
    #     extracted_values = []
    #     for key, value in numbers_dict.items():
    #         extracted_values.extend([data_values[num] for num in value if num in data_values])
    #     return extracted_values

    def extract_values_by_numbers_updated(data_values, numbers_dict_updated):
        extracted_values = []
        
        # for value in numbers_dict_updated:

        return [data_values[num] for num in numbers_dict_updated if num in data_values]
          
            # extracted_values.extend([data_values[num] for num in numbers_dict_updated if num in data_values])
            # print(extracted_values)
        # print("einf")
        # return extracted_values
    
    for dict_key, dict_value in numbers_dict.items():
       # print(dict_value)
        extracted_values = extract_values_by_numbers_updated(data_values, dict_value)
        
        average_payoff_per_strategy = calculate_average_payoff_per_strategy(extracted_values)


        if extracted_values:
            total_payoff = sum(item['realized_profit'] for item in extracted_values)
            total_avg_payoff = total_payoff / len(extracted_values)
        else:
            total_avg_payoff = 0  # Or np.nan if no neighbours
        
        for key in dict_value:
            strategy = data_values[key]["strategy"]
            avg_payoff = average_payoff_per_strategy[strategy]
            data_values[dict_key][f'average_payoff_neighbours_strat{strategy}'] = avg_payoff

            # === Assign total average payoff for all neighbours ===
            data_values[key]['average_payoff_neighbours_total'] = total_avg_payoff

        # print(average_payoff_per_strategy)
        #print(dict_value)
        for key in dict_value:
            # print(key)
            # print("data_values type:", type(data_values))
            # print("data_values[key] type:", type(data_values[key]))
            # print("data_values[key]:", data_values[key])

            strategy = data_values[key]["strategy"]
            avg_payoff = average_payoff_per_strategy[strategy]
            data_values[dict_key][f'average_payoff_neighbours_strat{strategy}'] = avg_payoff

    #pprint.pprint(data_values)

    return(data_values)

def average_payoff_neighbour_influencers(data_values, numbers_dict):
    for participant_id, neighbour_ids in numbers_dict.items():
        # Remove any old influencer average keys
        keys_to_remove = [
            k for k in data_values[participant_id]
            if k.startswith('average_payoff_neighbour_influencer_')
        ]
        for k in keys_to_remove:
            del data_values[participant_id][k]
        
        influencer_profits = {}
        influencer_counts = {}
        my_influencer = data_values[participant_id].get('supervisor_number')
        my_profit = data_values[participant_id]['realized_profit']
        for neighbour_id in neighbour_ids:
            neighbour = data_values.get(neighbour_id, {})
            influencer_id = neighbour.get('supervisor_number')
            if influencer_id is not None and influencer_id in data_values:
                influencer_profit = data_values[influencer_id]['realized_profit']
                if influencer_id in influencer_profits:
                    influencer_profits[influencer_id] += influencer_profit
                    influencer_counts[influencer_id] += 1
                else:
                    influencer_profits[influencer_id] = influencer_profit
                    influencer_counts[influencer_id] = 1
        # Include own payoff if influencer matches
        # if my_influencer in influencer_profits:
        #     influencer_profits[my_influencer] += my_profit
        #     influencer_counts[my_influencer] += 1
        # elif my_influencer is not None:
        #     influencer_profits[my_influencer] = my_profit
        #     influencer_counts[my_influencer] = 1

        for influencer_id in influencer_profits:
            avg_payoff = influencer_profits[influencer_id] / influencer_counts[influencer_id]
            data_values[participant_id][f'average_payoff_neighbour_influencer_{influencer_id}'] = avg_payoff
    return data_values

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_new_strategy(R, M, new_dict, N, S):
    # The same matrix construction logic as before
    def maak_matrix(R, M):
        numbers = list(range(1, R**2 * M + 1))  # Changed to start from 1
        result_matrix = []
        sqrt = int(np.sqrt(M))
        begin_getal = 0
        for i in range(R * sqrt):
            if (i * R) % (R**2) == 0 and i != 0:
                begin_getal = i * R * sqrt + 1
            elif i == 0:
                begin_getal = 1
            else:
                begin_getal += R
            block = numbers[i:i + (R * M)]
            values_list = []
            for j in range(sqrt):
                for value in range(begin_getal + (j * R**2), begin_getal + (j * R**2) + R):
                    if value <= R**2 * M:
                        values_list.append(value)
            result_matrix.append(values_list)
        return result_matrix

    result_matrix = maak_matrix(R, M)
    # Build matrix with new_strategy
    strategy_matrix = []
    for row in result_matrix:
        new_row = []
        for value in row:
            if value in new_dict:
                new_row.append(new_dict[value]['strategy'])
            else:
                new_row.append(None)
        strategy_matrix.append(new_row)
    matrix = strategy_matrix

    colors = {1: 'lightblue', 2: 'darkblue', 3: 'red', None: 'white'}
    plt.figure(figsize=(len(matrix[0]), len(matrix)))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            color = colors.get(matrix[i][j], 'white')
            plt.fill([j, j + 1, j + 1, j], [-i, -i, -i - 1, -i - 1], color=color)
            # Add this line to print the value:
            #if matrix[i][j] is not None:
              #  plt.text(j + 0.5, -i - 0.5, str(matrix[i][j]), ha='center', va='center', fontsize=12)

    plt.xlim(0, len(matrix[0]))
    plt.ylim(-len(matrix), 0)
    plt.gca().set_aspect('equal')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
   
   # os.makedirs('visualisation_new_strategy', exist_ok=True)
    plt.savefig(f'visualisation_new_strategy/M_is_{M}_R_is_{R}_N_is{N}_S_is_{S}.png')
    plt.close()
    return matrix

# Usage
# plot_new_strategy(R, M, new_dict, N, S)


import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import numpy as np

def plot_supervisor_matrix(R, M, data_dict, N, S):
    # Matrix bouwen zoals eerder
    def maak_matrix(R, M):
        numbers = list(range(1, R**2 * M + 1))
        result_matrix = []
        sqrt = int(np.sqrt(M))
        begin_getal = 0
        for i in range(R * sqrt):
            if (i * R) % (R ** 2) == 0 and i != 0:
                begin_getal = i * R * sqrt + 1
            elif i == 0:
                begin_getal = 1
            else:
                begin_getal += R
            values_list = []
            for j in range(sqrt):
                for value in range(begin_getal + (j * R ** 2), begin_getal + (j * R ** 2) + R):
                    if value <= R ** 2 * M:
                        values_list.append(value)
            result_matrix.append(values_list)
        return result_matrix

    result_matrix = maak_matrix(R, M)
    # Bouw matrix met supervisor_number en state
    matrix = []
    for row in result_matrix:
        new_row = []
        for value in row:
            if value in data_dict:
                sup_num = data_dict[value]['supervisor_number']
                sup_state = data_dict[value]['supervisor_state']
                new_row.append((sup_num, sup_state))
            else:
                new_row.append((None, None))
        matrix.append(new_row)

    # Unieke supervisor_numbers vinden
    all_sup_nums = set()
    for row in matrix:
        for sup_num, sup_state in row:
            if sup_num is not None:
                all_sup_nums.add(sup_num)
    all_sup_nums = sorted(list(all_sup_nums))
    num_sup = len(all_sup_nums)

    # # Kleur mapping maken
    # # Voor blauw en rood, met genoeg duidelijk verschillende tinten
    # blue_cmap = plt.cm.get_cmap('Blues', num_sup + 2)  # +2 voor mooi bereik
    # red_cmap = plt.cm.get_cmap('Reds', num_sup + 2)

    # sup_num_to_blue = {sup_num: blue_cmap(i + 2) for i, sup_num in enumerate(all_sup_nums)}
    # sup_num_to_red = {sup_num: red_cmap(i + 2) for i, sup_num in enumerate(all_sup_nums)}

    # # Plotten
    # plt.figure(figsize=(len(matrix[0]), len(matrix)))
    # for i, row in enumerate(matrix):
    #     for j, (sup_num, sup_state) in enumerate(row):
    #         if sup_num is None:
    #             color = 'white'
    #         elif sup_state == 1:
    #             color = sup_num_to_blue[sup_num]
    #         elif sup_state == 0:
    #             color = sup_num_to_red[sup_num]
    #         else:
    #             color = 'grey'
    # purples_hex = [
    # "#f3e5f5", "#e1bee7", "#ce93d8", "#ba68c8", "#ab47bc", "#9c27b0", "#8e24aa", "#7b1fa2", "#6a1b9a"
    # ]
    # yellows_hex = [
    # "#fffde7", "#fff9c4", "#fff59d", "#fff176", "#ffee58", "#ffeb3b", "#fdd835", "#fbc02d", "#f9a825"
    # ]
    # purples_hex = [
    # "#f3e5f5", "#e8c8ec", "#ddb0e3", "#d298da", "#c782d1", "#bc6dc8", "#ab56bc", "#9a41b1",
    # "#8a36ab", "#7b2aa5", "#6b1d9e", "#5d1992", "#4e1587", "#441378", "#3a1069", "#300d5a"
    # ]

    purples_hex = [
    "#f3e5f5", "#ecd2ef", "#e4bfe9", "#ddace3", "#d599dd", "#ce86d7", "#c673d1", "#bf60cb",
    "#b64dc5", "#ad3abf", "#a22fb9", "#9625b3", "#8a1bad", "#7e10a7", "#7206a1", "#66009b",
    "#5c0092", "#520089", "#480080", "#3e0077", "#34006e", "#2a0065", "#23005a", "#1c004f",
    "#150044", "#13003d", "#110036", "#0f002f", "#0d0028", "#0b0021", "#09001a", "#070013",
    "#05000c", "#030005", "#010000", "#000000"
]
    yellows_hex = [
    "#fffde7", "#fffbdc", "#fffad1", "#fff8c6", "#fff7bb", "#fff5b0", "#fff3a5", "#fff19a",
    "#ffef8f", "#ffed84", "#ffeb79", "#ffe96e", "#ffe763", "#ffe458", "#ffe24d", "#ffe042",
    "#ffde37", "#ffdb2c", "#ffd921", "#ffd716", "#f7c913", "#efbc10", "#e7ae0d", "#dfa10a",
    "#d79307", "#cf8604", "#c77901", "#b96e00", "#ab6300", "#9d5800", "#8f4d00", "#814200",
    "#733700", "#652c00", "#572100", "#491600"
]


    # yellows_hex = [
    # "#fffde7", "#fffbd6", "#fffac4", "#fff8b2", "#fff7a0", "#fff58e", "#fff37c", "#ffe869",
    # "#ffdf56", "#ffd643", "#ffce31", "#ffc31e", "#ffb60c", "#f9a825", "#e09a20", "#c78c1c"
    # ]

    # for i, row in enumerate(matrix):
    #     for j, (sup_num, sup_state) in enumerate(row):
    #         if sup_num is None:
    #             color = 'white'
    #         elif sup_state == 1:
    #             color = purples_hex[sup_num - 1]  # e.g. sup_num==1 -> first color, etc.
    #         elif sup_state == 0:
    #             color = yellows_hex[sup_num - 1]
    #         else:
    #             color = 'grey'
    #         plt.fill([j, j + 1, j + 1, j], [-i, -i, -i - 1, -i - 1], color=color)
    for i, row in enumerate(matrix):
        for j, (sup_num, sup_state) in enumerate(row):
            if sup_num is None:
                color = 'white'
                label = ""
            elif sup_state == 1:
                color = purples_hex[sup_num - 1]
                label = f"{sup_num},{sup_state}"
            elif sup_state == 0:
                color = yellows_hex[sup_num - 1]
                label = f"{sup_num},{sup_state}"
            else:
                color = 'grey'
                label = f"{sup_num},{sup_state}"
            plt.fill([j, j + 1, j + 1, j], [-i, -i, -i - 1, -i - 1], color=color)
            # Add this to print the value:
            #if sup_num is not None:
                #plt.text(j + 0.5, -i - 0.5, label, ha='center', va='center', fontsize=8)

    plt.xlim(0, len(matrix[0]))
    plt.ylim(-len(matrix), 0)
    plt.gca().set_aspect('equal')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])

    # Zorg dat map bestaat
    os.makedirs('visualisation_supervisor_number', exist_ok=True)
    plt.savefig(f'visualisation_supervisor_number/M_is_{M}_R_is_{R}_N_is{N}_S_is_{S}.png')
    plt.close()

# Gebruik: 
# plot_supervisor_matrix(R, M, your_data_dict, N, S)



import math as mt

def maak_matrix(R, M):
    numbers = list(range(R**2*M))
    result_matrix = []
    sqrt = int(mt.sqrt(M))
    begin_getal = 0
    for i in range(R*sqrt):
        # Hij maakt hier het begingetal, dus het eerste getalletje in de lijst. Het probleem is alleen dat na R^2 moet ie weer resetten, dat doet ie niet goed
        #  dat moet nog gebouwd worden
        # if begin_getal % R = 0:

        if (i*R) % (R**2) == 0 and i != 0:
            begin_getal = i * R * sqrt +1 # Increment the starting number by R*M
        elif i == 0:
            begin_getal = 1
        else:
            begin_getal += R  # Increment the starting number by R
        # print(begin_getal)
        block = numbers[i:i+(R*M)]  # Extract a block of elements from the input list
        matrix_block = []
        # print(begin_getal)
        matrix_row = []
        values_list = []
        for j in range(sqrt):
            # ik heb nog geen manier gevonden om dynamisch de matrix rows aan elkaar te plakken. Het beginnetje is er want de eerste rij maakt ie 
            #  al bijna goed, hij gaat alleen maar tot " het goede aantal " - 1... 
            # hij zet nu soort van de getallen goed in de rijen, maar hij maakt lists in lists in plaats van een enkele lijst met alle getallen
            matrix_row_part =block[begin_getal+(j*R**2):begin_getal+(j*R**2)+R]
            matrix_row.append(matrix_row_part)
            for value in range(begin_getal + (j * R ** 2), begin_getal + (j * R ** 2) + R):
                values_list.append(value)  # Append each value to the list
        # print(values_list)
        matrix_block.append(values_list)
        # print(matrix_block)
        result_matrix.extend(matrix_block)
    return result_matrix



def get_neighbors_dict(data):

    # Function to get neighbors of a value in the list
    def get_neighbors(data, row, col):
        neighbors = []
        for r in range(max(0, row - 1), min(row + 2, len(data))):
            for c in range(max(0, col - 1), min(col + 2, len(data[0]))):
                if (r, c) != (row, col):
                    neighbors.append(data[r][c])
        return neighbors

    # Dictionary to store neighbors
    neighbor_dict = {}

    # Loop through the list and store neighbors in the dictionary
    for i, sublist in enumerate(data):
        for j, value in enumerate(sublist):
            neighbor_dict[value] = get_neighbors(data, i, j)

    return neighbor_dict
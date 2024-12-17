import numpy as np
import random as rd
#from math import exp
import copy as cp

import matplotlib.pyplot as plt

# On commence par créer une population de base qui va simplement nous permettre 
# de réaliser des tests sur les animations ect...
# Donc pour le moment on considère un modèle logistique discrétisé.
# See Murray, Mathematical biology (II) for additional information the calculation of growth rates
# as a function of resource availability. 


# We'll use classes later on
class bacteria:
    """This class corresponds to a single bacteria. Each bacteria has its own
    characteristcs: growth rate, nutrional balance, position in the grid."""
    pass

class colony:
    """This class corresponds to a colony of bacteria"""

    def __init__(self, nutrional_balance, LV_caracteristics):
        """Population class constructor"""
        self.grid = np.random.random((n, n))
        self.grid = self.grid < 0.5
    
    def population_growth(self, r):
        pass

# Let's first imagine a very simple lattice model considering only one type of
# bacteria.

n = 60
        
#grid = np.zeros((n, n))
# grid = grid < 0.5
#grid[int(n/2), int(n/2)] = 1 #initial bacteria

# Bacterial properties
#r = 0.2 #per seconds
#K = n ** 2

directions = {0: [0, -1], 
              1: [-1, 0], 
              2: [0, 1], 
              3: [1, 0]}

direction_choice = [0, 1, 2, 3]

bacteria_type = [i for i in range(1, 6)]
r_dict = {i:1 for i in range(1, 7)}
gap_dict = {
    1: 0.5,
    2: 0.5,
    3: 0.5,
    4: 0.5,
    5: 0.5,
    6: 0.4
}
# r_dict = {1:1,
#         2:0.8,
#         3:0.7,
#         4:0.6,
#         5:0.5
# }

n_dict = {
    0: None,
    1: 1.6,
    2: 1.8,
    3: 2.0,
    4: 2.2,
    5: 10,
    6: 200
}

coef_dict = [
    [1/3, 1/3, 1/3]
]

def initialize_pop(n):
    grid = np.random.random((n, n))

    for i, line in enumerate(grid):
        for j, element in enumerate(line):
            if element < 0.01:
                grid[i, j] = rd.choice(bacteria_type)
                # grid[i, j] = 1
            else:
                grid[i, j] = 0
    return grid

def calc_growth(s, n, r_val, gap_val):
    # s1 proteine
    # s2 glucide 
    # s3 lipide
    # n just_n
    s1, s2, s3 = s
    r_coeff = 1/3 * ((1/((1/(s1 + gap_val))**n + 1)) + (1/((1/(s2 + 0.5))**n + 1)) + (1/((1/(s3 + 0.5))**n + 1))) * r_val

    return r_coeff

def calc_growth_simple(s, n, r_val):

    pass

def population_growth(grid, r_dict, n_dict, s):

    new_grid = grid != 0
    # print(s)

    true_r_vect = [0,
    calc_growth(s, n_dict[1], r_dict[1], gap_dict[1]),
    calc_growth(s, n_dict[2], r_dict[2], gap_dict[2]),
    calc_growth(s, n_dict[3], r_dict[3], gap_dict[3]),
    calc_growth(s, n_dict[4], r_dict[4], gap_dict[4]),
    calc_growth(s, n_dict[5], r_dict[5], gap_dict[5]),
    calc_growth(s, n_dict[6], r_dict[6], gap_dict[6])]
    # print(true_r_vect)

    for i, row in enumerate(grid):
        for j, bact in enumerate(row):
            if bact:
                mult = rd.random()

                # print(bact)
                true_r = true_r_vect[int(bact)]

                if mult < true_r:
                    gap = rd.choice(directions)
                    index1 = i + gap[0]
                    index2 = j + gap[1]
                    # try :
                    #     if not new_grid[index1, index2] : grid[index1, index2] = 1
                    try :
                        grid[index1, index2] = bact
                    except IndexError:
                        pass 
    return grid

def population_growth2(grid):
    # Ne fonctionne que pour 1 type de bactérie
    r = 1
    new_grid = grid == 1

    mult_grid = np.random.random((n, n))
    mult_grid = mult_grid < r
    gap_grid = np.random.choice(direction_choice, size = (n, n))
    gap_coords_grid = [[directions[gap] for gap in row] for row in gap_grid]


    for i, (gridrow, multrow, gaprow) in enumerate(zip(new_grid, mult_grid, gap_coords_grid)):
        for j, (bact, mult, gap) in enumerate(zip(gridrow, multrow, gaprow)):
            if bact:
                if mult:
                    index1 = i + gap[0]
                    index2 = j + gap[1]
                    try :
                        if not new_grid[index1, index2] : grid[index1, index2] = 1
                    except IndexError:
                        pass 
    return grid

def Draw_pop_dynamics(grid, image_size, color_dict):

    colors = color_dict.values()
    x_size, y_size = image_size

    fig, axes = plt.subplots(1, 1)
    fig.set_edgecolor('white')
    fig.set_facecolor('black')
    
    N_slots = np.size(grid)

    proportions = np.zeros(7, dtype = 'float')

    for row in grid:
        for bact in row:
            proportions[int(bact)] += 1
        
    proportions / N_slots

    axes.pie(proportions, explode = [0 for i in range(7)],
    shadow = False, startangle=90, colors = colors)
    # autopct = '%1.1f%%',

    return fig, axes

def pathogene_spawn(grid):
    spawn = np.random.random((n, n))

    for i, line in enumerate(spawn):
        for j, element in enumerate(line):
            if element < 0.01:
                grid[i, j] = 6
    return grid



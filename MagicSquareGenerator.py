# -*- coding: utf-8 -*-

## References
#[1] Tao Xie and Lishan Kang, "An evolutionary algorithm for magic squares," The 2003 Congress on Evolutionary Computation, 2003. CEC '03., Canberra, ACT, Australia, 2003, pp. 906-913 Vol.2, doi: 10.1109/CEC.2003.1299763.
#[2] Cui, Xintian, Xiangqi Cheng, and Guoxuan Bu. "Research on Magic Square Construction Based on Genetic Algorithm." Academic Journal of Computing & Information Science 5.2 (2022): 77-80. Vol. 5, doi: 10.25236/AJCIS.2022.050212

# Magic Square Generator Notebook
# Author: Álvaro González Méndez

import argparse

import numpy as np
import numpy.random as rnd
import copy
import matplotlib.pyplot as plt
from tqdm import tqdm

# A class for our individuals and method than initializes it with random individuals
class individual:
  def __init__(self,size,starting_deviaton) -> None:
    self.size =size
    self.starting_deviaton = starting_deviaton
    ordered_numbers = np.arange(1, size**2+1)
    shuffled_numbers = np.random.permutation(ordered_numbers)
    self.M = shuffled_numbers.reshape((size,size))
    self.delta = np.full((size,size),starting_deviaton)
    self.c = (size*(size**2+1))/2
    self.max = size**2
    self.global_delta =0

    self.n_col = 0
    self.n_row = 0

    self.d1 = 1
    self.d2 = 1

def init_population(population,sqr_size,s_deviaton):
  individual_list = []
  for i in range(population):
    ind = individual(sqr_size,s_deviaton)
    individual_list.append(ind)
  return individual_list

# Fitness function for the first part of the algorithm, 
# (when we need to search for Low-Quality Magic Squares)
def first_fitness(individual):
  size = individual.size
  c = individual.c
  sum_rows = np.sum(individual.M,axis=1)
  sum_cols = np.sum(individual.M,axis=0)
  fitness = int(np.sum(np.abs(c-sum_rows))+np.sum(np.abs(c-sum_cols)))
  return fitness

# Method that calculates the fitness for each individual in a list in the
# first part of the algorithm
def first_population_fitness(individual_list):
  fitness_list = []
  for individual in individual_list:
    score = first_fitness(individual)
    if score == 0:
      return individual
    fitness_list.append(score)
  return fitness_list

# Method that updates `n_rows` and `n_cols` in a given individual and returns *S1* and *S2* lists
def ns_update(individual):
  col_sums = np.sum(individual.M,axis=0) - individual.c
  row_sums = np.sum(individual.M,axis=1) - individual.c
  individual.n_col = np.count_nonzero(col_sums)
  individual.n_row = np.count_nonzero(row_sums)
  S1 = set()
  S2 = set()
  col_list = []
  row_list = []
  for it in range(individual.size):
    if col_sums[it] != 0:
      S2.update(individual.M[:,it])
      col_list.append(it)
    if row_sums[it] != 0:
      S2.update(individual.M[it])
      row_list.append(it)
  for j in col_list:
    for i in row_list:
      S1.add(individual.M[i,j])
  return S1,S2

# Method that finds the nearest value to a given interger in an array,
# it also checks that is not a value called old
def find_nearest(elem_set, searched, old):
    nearest = None
    least_diff = int(100000000)
    for elem in elem_set:
        diff = abs(elem - searched)
        if diff < least_diff and elem != old:
            least_diff = diff
            nearest = elem
    return least_diff

# Updates the global variance of a given individual
def update_global_delta(individual):
  c = individual.c
  sum_rows = np.sum(individual.M,axis=1)
  sum_cols = np.sum(individual.M,axis=0)
  new_global_delta = np.ceil(np.sum(np.abs(c-sum_rows))+np.sum(np.abs(c-sum_cols))/(individual.n_col+individual.n_row))

  return new_global_delta

# Mutation Operator for the first part of the algorithm, 
# (when we need to search for Low-Quality Magic Squares)
def first_mutation(individual_list,probability):
  for individual in individual_list:
    if np.random.random() < probability:
      S1,S2 = ns_update(individual)
      permutations = [1,2]
      p1= 0
      p2= 0
      if individual.n_row != 0 or individual.n_col != 0:
        if individual.n_row == 0:
          p2 = 1/(individual.n_col*individual.size)
        elif individual.n_col == 0:
          p2 = 1/(individual.n_row*individual.size)
        else:
          p1 = 1/(individual.n_col*individual.n_row)
          p2 = 1/(individual.n_col*individual.size) +1/(individual.n_row*individual.size)
          permutations.append(0)
        permutation = np.random.choice(permutations)
        if permutation == 0:
          mut_set = list(S1)
          out_set = list(S2)
          p = p1
        elif permutation == 1:
          mut_set = list(S2)
          out_set = list(S2)
          p = p2
        else:
          mut_set = list(S2)
          out_set = list(range(1,individual.max+1))
          p = p2
        for elem in mut_set:
          if np.random.random() < p:
            i,j = np.where(individual.M == elem)
            old_value = individual.M[i,j]
            new_value = old_value
            new_value = old_value + np.random.randint(-individual.delta[i,j],individual.delta[i,j])
            if new_value < 1:
              new_value = np.random.randint(1,individual.size)
            elif new_value > individual.max:
              new_value = individual.max - np.random.randint(0,individual.size)

            if new_value not in out_set:
              new_value = find_nearest(out_set,new_value,old_value)
            k,l = np.where(individual.M == new_value)
            individual.M[i,j] = new_value
            individual.M[k,l] = old_value
            vary = np.random.randint(-1,2)
            new_delta = individual.delta[i,j] + vary
            global_delta = int(update_global_delta(individual))
            if new_delta < 1 or new_delta > global_delta :
              if global_delta < 2:
                new_delta = 1
              else:
                new_delta = np.random.randint(1,global_delta)
            individual.delta[i,j] = new_delta

# Selector Operator, it will always return the individual with lowes fitness.
# Its mean to be deterministic. Tested vs. stochastic general method and works better.
def get_best(population, fitness_scores, n):
    pairs = list(zip(fitness_scores, population))
    ordered_pairs = sorted(pairs, key=lambda pairs: pairs[0])
    best_pairs = ordered_pairs[:n]
    best_fitness, selected_individuals = zip(*best_pairs)
    return selected_individuals

# Set of deterministic rules that make the algorithm permutate values in order to be faster.
def local_rectification(individual):
    M = individual.M
    n = individual.size
    c = individual.c
    filas_con_error_indices = [i for i in range(n) if sum(M[i]) != c]

    for i in range(len(filas_con_error_indices)):
        for j in range(i + 1, len(filas_con_error_indices)):
            k = filas_con_error_indices[i]
            l = filas_con_error_indices[j]

            error_k = sum(M[k]) - c
            error_l = sum(M[l]) - c

            if error_k == -error_l:
                found_one_pair = False
                for s in range(n):
                    num_ks = M[k][s]
                    num_ls = M[l][s]
                    if (num_ks - num_ls) == error_k:
                        M[k][s], M[l][s] = M[l][s], M[k][s]
                        found_one_pair = True
                        break

                if found_one_pair:
                    continue

                found_two_pairs = False
                for s in range(n):
                    for t in range(s + 1, n):
                        num_ks = M[k][s]
                        num_ls = M[l][s]
                        num_kt = M[k][t]
                        num_lt = M[l][t]

                        if (num_ks + num_kt) - (num_ls + num_lt) == error_k:
                            M[k][s], M[l][s] = M[l][s], M[k][s]
                            M[k][t], M[l][t] = M[l][t], M[k][t]
                            found_two_pairs = True
                            break
                    if found_two_pairs:
                        break

# Fitness function for the first part of the algorithm, 
# (we need to transform our squares to High-Qualiti Magic Squares)
def second_fitness(individual):
  size = individual.size
  c = individual.c
  sum_diag = np.trace(individual.M)
  sum_antidiag = np.trace(np.fliplr(individual.M))
  fitness = int(np.abs(c-sum_diag)+np.abs(c-sum_antidiag))
  if sum_diag == 0: individual.d1 = 1
  else: individual.d1 = 0
  if sum_antidiag == 0: individual.d2 = 1
  else: individual.d2 = 0
  return fitness

# Method that calculates the fitness for each individual in a listç
# in the second part of the algorithm.
def second_population_fitness(individual_list):
  fitness_list = []
  for individual in individual_list:
    score = second_fitness(individual)
    if score == 0:
      return individual
    fitness_list.append(score)
  return fitness_list

# Mutation operator for the first part of the algorithm, 
# (we need to transform our squares to High-Qualiti Magic Squares)
def second_mutation(individual_list):
  for individual in individual_list:
    M = individual.M
    axis = np.random.randint(0, 2)
    if axis == 0:
        idx1, idx2 = np.random.choice(individual.size, size=2, replace=False)
        M[[idx1, idx2], :] = M[[idx2, idx1], :]
    else:
        idx1, idx2 = np.random.choice(individual.size, size=2, replace=False)
        M[:, [idx1, idx2]] = M[:, [idx2, idx1]]


# Command line options (python MagicSquareGenerator.py -h)
parser = argparse.ArgumentParser(
    description="Generate a magic square of order N with a two-phase evolutionary "
                "algorithm (T. Xie and L. Kang, 2003) plus local rectification.")
parser.add_argument("-n", "--size", type=int, default=10,
                    help="order N of the square (default: 10; 40 takes about 4 hours)")
parser.add_argument("--seed", type=int, default=25, help="random seed (default: 25)")
parser.add_argument("--max-iterations", type=int, default=200000,
                    help="maximum number of generations (default: 200000)")
parser.add_argument("-o", "--output", default="matriz.txt",
                    help="file where the square is saved (default: matriz.txt)")
parser.add_argument("--no-plot", action="store_true",
                    help="do not open the fitness evolution plots at the end")
args = parser.parse_args()

SEED = args.seed
np.random.seed(SEED)

OUTPUT_FILENAME = args.output

# Inicialize hyperparameters and required variables
sqr_size = args.size
s_deviaton = sqr_size**2
population = 1
offspring_num = sqr_size * 1
din_offspring_limit = sqr_size / 2
p_mutation = 1
max_iterations = args.max_iterations
first_min = 10000000
second_min = 10000000
phase_flag = False # If phase_flag == True we are on second phase
finish_flag = False

individuals = init_population(population,sqr_size,s_deviaton)
fitness_list_first = []
fitness_list_second = []

pbar = tqdm(range(max_iterations),desc="Generation")
try:
  for i in pbar:
    if not phase_flag:
      individuals_score = first_population_fitness(individuals)
      if type(individuals_score) == individual:
        print(f"No Quality Magic Square Found on Epoch {i}")
        phase_flag = True
        continue

      individual_fitness = individuals_score[0]
      fitness_list_first.append(individual_fitness)
      if individual_fitness < first_min:
        first_min = individual_fitness
        pointer = individuals_score.index(individual_fitness)
        pbar.set_postfix(min_epoch1=i,min_fitness1=individual_fitness)

      selected_individuals = get_best(individuals,individuals_score,population)
      if individual_fitness < 50 * sqr_size:
        for elem in selected_individuals:
          local_rectification(elem)
      individuals = []
      offspring = []

      for elem in selected_individuals:
        for i in range(offspring_num):
          offspring.append(copy.deepcopy(elem))

      first_mutation(offspring,p_mutation)

      individuals = offspring
    else:
      individuals_score = second_population_fitness(individuals)
      if type(individuals_score) == individual:
        finish_flag = True
        break

      individual_fitness = individuals_score[0]
      fitness_list_second.append(individual_fitness)
      if individual_fitness < second_min:
        second_min = individual_fitness
        pointer = individuals_score.index(individual_fitness)
        pbar.set_postfix(min_epoch2=i,min_fitness2=individual_fitness)

      selected_individuals = get_best(individuals,individuals_score,population)
      individuals = []
      offspring = []

      for elem in selected_individuals:
        for i in range(offspring_num):
          offspring.append(copy.deepcopy(elem))

      second_mutation(offspring)
      
      individuals = offspring
finally:
  if finish_flag:
    print("-"*25)
    print(f"Magic Square Found on Epoch {i}")
    print(individuals_score.M)
    with open(OUTPUT_FILENAME, "wt") as fp:
      fp.write(str(individuals_score.M))
    print(f"Matrix have been saved on {OUTPUT_FILENAME}")
    print("-"*25)
  else: print("-"*25+"\nSomething went wrong :(\n"+"-"*25)
  
  fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

  axes[0].plot(fitness_list_first, color='blue')
  axes[0].set_title("First Min Fitness evolution")
  axes[0].set_xlabel("Generation")
  axes[0].set_ylabel("Fitness")
  axes[0].grid(True)
  
  axes[1].plot(fitness_list_second, color='red')
  axes[1].set_title("Second Min Fitness evolution")
  axes[1].set_xlabel("Generation")
  axes[1].set_ylabel("Fitness")
  axes[1].grid(True)
  
  plt.tight_layout()
  
  if not args.no_plot:
    plt.show()
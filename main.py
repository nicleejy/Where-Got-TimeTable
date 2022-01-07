from random import choices
from collections import namedtuple
from functools import partial
import time

from moduleparser import get_all_module_info
from helperfunctions import dprint, sigmoid, table_compressor, generate_link, merge_scores
from genetics import single_point_crossover, mutate
from timetable_generator import generate_timetable
from fitness import *

#Parameters to vary

academic_year = "2021-2022"

semester = 1

module_codes = ["CS2100", "ES2660", "IS1103", "MA1521", "CS1231", "MA1521"]

container = None

# Takes in a 2D list containing lists of timetables 
# as well as the fitness and soft constraints function 
# and evaluates each timetable to find timetables with the highest score
def select_pairs(population_list, fitness_func, soft_constraints_func):
    return choices(
            population=population_list,
            weights=[merge_scores(timetable, fitness_func, soft_constraints_func) for timetable in population_list],
            k=2
    )


def populate(population_size):
    population = []
    for i in range(population_size):
        population.append(generate_timetable(container))
    return population


def run_evolution(population_size, generation_limit, fitness_limit, fitness_func, mutate_func, soft_constraints):

    population = populate(population_size)

    for j in range(generation_limit + 1):
        population = sorted(
            population,
            key=lambda timetable: (fitness_func(timetable), soft_constraints(timetable)),
            reverse=True
        )

        total = 0
        scores = []

        for member in population:
            total += soft_constraints(member)
            scores.append(soft_constraints(member))

        tolerance = abs(total/10 - soft_constraints(population[0]))

        if fitness_func(population[0]) == fitness_limit and 0 <= tolerance <= 1:
            break
        
        next_generation = population[0:2]

        for k in range(int(len(population) / 2) - 1):
            parents = select_pairs(population, fitness_func)
            child_a, child_b = single_point_crossover(parents[0], parents[1])
            child_a = mutate_func(child_a)
            child_b = mutate_func(child_b)
            next_generation += [child_a, child_b]

        population = next_generation

        print(f"\nGeneration: {j}\n")
        score = fitness_func(population[0])
        print(sorted(scores, reverse=True))
        
        soft_score = soft_constraints(population[0])
        print(f"Soft score: {soft_score}")
        print(f"Tolerance: {tolerance}")
        print(f"Fitness score: {score}\n")
        
    final_population = sorted(
            population,
            key=lambda timetable: (fitness_func(timetable), soft_constraints(timetable)),
            reverse=True
        )

    total1= 0
    scores3 = []
    for member1 in final_population:
        total1 += soft_constraints(member1)
        scores3.append(soft_constraints(member1))
    tolerance2 = abs(total1/10 - soft_constraints(final_population[0]))

    score_2 = fitness_func(final_population[0])
    soft_score_2 = scores3[0]

    print(sorted(scores3, reverse=True))
    print(f"Soft score at last generation: {soft_score_2}")
    print(f"Tolerance at last generation: {tolerance2}")
    print(f"Fitness score at last generation: {score_2}\n")
    
    return final_population, j

start = time.time()
population, generations = run_evolution(
    population_size=10,
    generation_limit=300,
    fitness_limit=1,
    fitness_func=partial(
        fitness_function, "1000", "1800", ["Monday"]
        ),
    mutate_func=partial(
        mutate, 1, container
        ),
    soft_constraints= partial(
        soft_constraints, 1, True
    )
)

end = time.time()
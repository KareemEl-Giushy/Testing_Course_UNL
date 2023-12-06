import random
import time
import sys



file_path = "text.txt"

with open(file_path, "r") as file:
    target_string = "".join(file.readlines())
    print(target_string)

# Define the genetic algorithm parameters
POPULATION_SIZE = 100 
MUTATION_RATE = 0.1
ELITE_PERCENTAGE = 0.1
MAX_GENERATIONS = 1000
PRINT_INTERVAL = 50

def generate_random_string(length):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !.,') for _ in range(length))

def calculate_fitness(chromosome, target):
    return sum(1 for c1, c2 in zip(chromosome, target) if c1 != c2)

def crossover(parent1, parent2):
    # Perform single-point crossover
    crossover_point = random.randint(0, min(len(parent1), len(parent2)))
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(chromosome):
    # Randomly mutate characters in the chromosome
    mutated_index = random.randint(0, len(chromosome) - 1)
    mutated_character = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !.,')
    return chromosome[:mutated_index] + mutated_character + chromosome[mutated_index + 1:]

def select_elites(population, target):
    # Select the top elites based on fitness
    elites = sorted(population, key=lambda x: calculate_fitness(x, target))[:int(ELITE_PERCENTAGE * POPULATION_SIZE)]
    return elites

def genetic_algorithm(target):
    # Generate an initial population
    population = [generate_random_string(random.randint(1, len(target))) for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        # Evaluate fitness of each individual in the population
        fitness_scores = [calculate_fitness(chromosome, target) for chromosome in population]

        # Check for a perfect match
        if 0 in fitness_scores:
            print(f"Found solution in generation {generation}!")
            break

        # Select elites to carry over to the next generation
        elites = select_elites(population, target)

        # Create the next generation using crossover and mutation
        new_population = elites.copy()

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)

            # Apply mutation to the children
            if random.random() < MUTATION_RATE:
                child1 = mutate(child1)
            if random.random() < MUTATION_RATE:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        # Update the population for the next generation
        population = new_population

        # Print progress every PRINT_INTERVAL generations
        if generation % PRINT_INTERVAL == 0 or generation == MAX_GENERATIONS - 1:
            average_fitness = sum(fitness_scores) / len(fitness_scores)
            best_fit_index = fitness_scores.index(min(fitness_scores))
            best_fit_chromosome = population[best_fit_index]
            best_fit_fitness = fitness_scores[best_fit_index]
            print(f"generation {generation}, average fit {average_fitness:.2f}, best fit {best_fit_fitness}\n{best_fit_chromosome}")

    print("\ndone:")
    unique_chromosomes = len(set(population))
    print(f"{unique_chromosomes} evaluated chromosomes")
    print(f"{generation + 1} generations")
    best_fit_index = fitness_scores.index(min(fitness_scores))
    print(f"best fit chromosome: {fitness_scores[best_fit_index]}\n{population[best_fit_index]}")

if __name__ == "__main__":
    start_time = time.time()
    genetic_algorithm(target_string)
    end_time = time.time()
    print(f"\nExecution time: {end_time - start_time:.2f} seconds")

import random
import time

TARGET_STRING = """Everything Apple announced today: Apple Watch 6 and SE, Apple One, new iPad Air.
The Apple Store went down this morning, heralding another Apple launch day. At the company's virtual event, Tim Cook started out by telling us that the Apple Watch and new additions to the iPad family of tablets would be the highlights -- and we got an Apple Watch Series 6, Apple Watch SE, a redesigned iPad Air debuting the A14 Bionic chip and a new eighth-gen iPad."""

POPULATION_SIZE = 100
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8
MAX_GENERATIONS = 1000
PRINT_INTERVAL = 50

# Helper function to generate a random chromosome
def generate_random_chromosome():
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-[]{}|;’:\",./<>? ") for _ in range(len(TARGET_STRING)))

# Updated fitness function based on length and characters
def calculate_fitness(chromosome):
    length_difference = abs(len(TARGET_STRING) - len(chromosome))
    character_difference = sum(1 for a, b in zip(TARGET_STRING, chromosome) if a != b)
    return length_difference + character_difference

# Genetic Algorithm
def genetic_algorithm():
    start_time = time.time()
    generation = 0
    population = [generate_random_chromosome() for _ in range(POPULATION_SIZE)]

    while generation < MAX_GENERATIONS:
        population = sorted(population, key=lambda x: calculate_fitness(x))
        best_fit = population[-1]
        avg_fit = sum(calculate_fitness(ch) for ch in population) / POPULATION_SIZE

        if generation % PRINT_INTERVAL == 0:
            print(f"Generation {generation}: Average Fitness = {avg_fit}, Best Fitness = {calculate_fitness(best_fit)}")

        if calculate_fitness(best_fit) == 0:
            print("Perfect fitness achieved!")

        new_population = [best_fit]  # Elitism - keep the best chromosome

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population, k=2)
            crossover_point = random.randint(1, len(TARGET_STRING) - 1)

            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            if random.random() < MUTATION_RATE:
                mutation_point = random.randint(0, len(TARGET_STRING) - 1)
                mutation_char = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-[]{}|;’:\",./<>? ")
                child1 = child1[:mutation_point] + mutation_char + child1[mutation_point+1:]

            if random.random() < MUTATION_RATE:
                mutation_point = random.randint(0, len(TARGET_STRING) - 1)
                mutation_char = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-[]{}|;’:\",./<>? ")
                child2 = child2[:mutation_point] + mutation_char + child2[mutation_point+1:]

            new_population.extend([child1, child2])

        population = new_population
        generation += 1

    end_time = time.time()

    print("\ndone:")
    print(f"Chromosomes evaluated: {POPULATION_SIZE * generation}")
    print(f"Number of generations: {generation}")
    print(f"Best fit string: {best_fit}")
    print(f"Fitness score of the best string: {calculate_fitness(best_fit)}")

    if calculate_fitness(best_fit) == 0:
        print("Perfect fitness achieved!")

    print(f"Total runtime: {end_time - start_time} seconds")

if __name__ == "__main__":
    genetic_algorithm()

import random
import sys

POPULATION_SIZE = 1050
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890\n, .-;:_!"#%&/()=?@${[]}\''''


filePath = sys.argv[1]
with open(filePath, 'rt') as f:
    TARGETS = f.readlines()

i = 0
FINAL_RESULT = ""
TARGET = TARGETS[i]

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        return [cls.mutated_genes() for _ in range(len(TARGET))]

    def mate(self, par2):
        child_chromosome = [
            gp1 if random.random() < 0.45 else gp2 if random.random() < 0.90 else self.mutated_genes()
            for gp1, gp2 in zip(self.chromosome, par2.chromosome)
        ]
        return Individual(child_chromosome)

    def cal_fitness(self):
        return sum(gs != gt for gs, gt in zip(self.chromosome, TARGET))

def line_checking():
    generation = 1
    population = [Individual(Individual.create_gnome()) for _ in range(POPULATION_SIZE)]

    while True:
        population = sorted(population, key=lambda x: x.fitness)
        fitness_scores = [individual.fitness for individual in population]
        if population[0].fitness <= 0:
            break

        new_generation = population[:int(0.1 * POPULATION_SIZE)]  # Elitism

        for _ in range(int(0.9 * POPULATION_SIZE)):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            new_generation.append(parent1.mate(parent2))

        population = new_generation

        generation += 1

        if generation % 50 == 0:
            print("\ndone:")
            unique_chromosomes = len(set("".join(individual.chromosome) for individual in population))
            print(f"{unique_chromosomes} evaluated chromosomes")
            average_fitness = sum(fitness_scores) / len(fitness_scores)
            print(f"Average fitness: {average_fitness}")
            print(f"{generation} generations")
            best_fit_index = population.index(min(population, key=lambda x: x.fitness))
            print(f"best fit chromosome: {population[best_fit_index].fitness}\n{FINAL_RESULT}\n{''.join(population[best_fit_index].chromosome)}")

    print("\nDone:")
    unique_chromosomes = len(set("".join(individual.chromosome) for individual in population))
    print(f"{unique_chromosomes} evaluated chromosomes")
    print(f"{generation} generations")
    best_fit_index = population.index(min(population, key=lambda x: x.fitness))
    print(f"Best fit chromosome: {population[best_fit_index].fitness}\n{''.join(population[best_fit_index].chromosome)}")
    return ''.join(population[best_fit_index].chromosome)

def main():
    global FINAL_RESULT
    global TARGET
    for i in range(len(TARGETS)):
        TARGET = TARGETS[i]
        FINAL_RESULT += line_checking()

    print("=====Final Output=====")
    print(FINAL_RESULT)

if __name__ == '__main__':
    main()

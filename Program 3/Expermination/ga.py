# Python3 program to create target string, starting from 
# random string using Genetic Algorithm 

import random 

# Number of individuals in each generation 
POPULATION_SIZE = 100

# Valid genes 
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP 
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}\''''

# Target string to be generated
with open("text.txt", 'rt') as f:
    TARGET = f.readline()
    print(TARGET)

class Individual(object): 
	''' 
	Class representing individual in population 
	'''
	def __init__(self, chromosome): 
		self.chromosome = chromosome 
		self.fitness = self.cal_fitness() 

	@classmethod
	def mutated_genes(self): 
		''' 
		create random genes for mutation 
		'''
		global GENES 
		gene = random.choice(GENES) 
		return gene 

	@classmethod
	def create_gnome(self): 
		''' 
		create chromosome or string of genes 
		'''
		global TARGET 
		gnome_len = len(TARGET) 
		return [self.mutated_genes() for _ in range(gnome_len)] 

	def mate(self, par2): 
		''' 
		Perform mating and produce new offspring 
		'''

		# chromosome for offspring 
		child_chromosome = [] 
		for gp1, gp2 in zip(self.chromosome, par2.chromosome):	 

			# random probability 
			prob = random.random() 

			# if prob is less than 0.45, insert gene 
			# from parent 1 
			if prob < 0.45: 
				child_chromosome.append(gp1) 

			# if prob is between 0.45 and 0.90, insert 
			# gene from parent 2 
			elif prob < 0.90: 
				child_chromosome.append(gp2) 

			# otherwise insert random gene(mutate), 
			# for maintaining diversity 
			else: 
				child_chromosome.append(self.mutated_genes()) 

		# create new Individual(offspring) using 
		# generated chromosome for offspring 
		return Individual(child_chromosome) 

	def cal_fitness(self): 
		''' 
		Calculate fitness score, it is the number of 
		characters in string which differ from target 
		string. 
		'''
		global TARGET 
		fitness = 0
		for gs, gt in zip(self.chromosome, TARGET): 
			if gs != gt: fitness+= 1
		return fitness 


def main():
    global POPULATION_SIZE

    # current generation
    generation = 1

    population = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while True:

        # sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)

        # If the individual has the lowest fitness score i.e.,
        # 0, then we know that we have reached the target
        if population[0].fitness <= 0:
            break

        # Otherwise generate new offsprings for a new generation
        new_generation = []

        # Perform Elitism, meaning 10% of fittest population
        # goes to the next generation
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # From 50% of fittest population, Individuals
        # will mate to produce offspring
        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        # print("Generation: {}\tString: {}\tFitness: {}".format(
        #     generation,
        #     "".join(population[0].chromosome),
        #     population[0].fitness))

        generation += 1

        # After a certain number of generations, print additional information
        if generation % 50 == 0:
            print("\ndone:")
            unique_chromosomes = len(set("".join(individual.chromosome) for individual in population))
            print(f"{unique_chromosomes} evaluated chromosomes")
            print(f"{generation} generations")
            best_fit_index = population.index(min(population, key=lambda x: x.fitness))
            print(f"best fit chromosome: {population[best_fit_index].fitness}\n{''.join(population[best_fit_index].chromosome)}")

    print("\nDone:")
    unique_chromosomes = len(set("".join(individual.chromosome) for individual in population))
    print(f"{unique_chromosomes} evaluated chromosomes")
    print(f"{generation} generations")
    best_fit_index = population.index(min(population, key=lambda x: x.fitness))
    print(f"Best fit chromosome: {population[best_fit_index].fitness}\n{''.join(population[best_fit_index].chromosome)}")


if __name__ == '__main__':
    main()
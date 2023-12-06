# Genetic Algorithm (Prgoram 3)
A genetic algorithm (GA) to evolve a string that matches a given target string. It evolves randomly generated strings to match the exact target string.

## Installation:
There are no external packages needed to run this program.

## Executing / Running The Script:

**Make sure to include the ```input file``` Absolute Path**

1. Open your terminal and make sure you are in the same directory as the script and enter the following command:
    ```
    python ga.py <Text Input File Path>
    ```
2. You are Done ... Enjoy :)

## Questions:
1. **What is your initial population size?**
    - The initail population is ``POPULATION_SIZE = 1050``
2. **How do you evaluate an individual? I.e., explain the formula that produces the fitness score**
    - ```python
        sum(gs != gt for gs, gt in zip(self.chromosome, TARGET))
        ```
    - ``self.chromosome`` represents the current individual's chromosome.
    - ``TARGET`` is the target string against which the individual's chromosome is compared.
    
    - The formula computes the sum of differences between corresponding characters in the individual's chromosome and the target string.

3. **What are the stopping criteria? (the GA loop stops when ...)**

    - The genetic algorithm loop stops when the fitness of the best individual in the population reaches zero
        ```python
        if population[0].fitness <= 0:
            break
        ```

4. **How do you select the chromosomes? (using tournament selection or other methods? what are the tournament sizes? etc.)**

    - The selection of parents for crossover is done using a simple method without explicitly implementing tournament selection. Instead, it uses random selection to choose parents from the first 50 individuals in the sorted population.
        ```python
        parent1 = random.choice(population[:50])
        parent2 = random.choice(population[:50])
        ```
    - ``parent1`` and ``parent2`` are randomly selected from the first 50 individuals in the sorted population. The use of the first 50 individuals implies a form of elitism.
5. **How often do you perform crossover and mutation? Are the crossover and mutation rates fixed or adaptive?**

    -  The crossover and mutation operations are performed in each generation. The rates of crossover and mutation are fixed and defined as follows:
        - Crossover:
            - Crossover is performed for 90% of the population in each generation.
            - The crossover rate is implicitly set to 90%.
        - Mutation:
            - Mutation is applied during the creation of a child chromosome in the mate method.
            - The mutation rate is not explicitly defined in the script, but it occurs when the mutated_genes method is called.

6. **How many chromosomes do you need to evaluate to achieve a chromosome with perfect fitness for the given target string? Due to the randomness of the algorithm, this number will fluctuate. Try to give some rough upper/lower bounds.  Note that your solution might not reach the target within the allowed time/space limit, but you should try to at least run once until it finds the target and report that here.**

    - Upper Bound Estimation:
        - 992 evaluated chromosomes
    - Lower Bound Estimaiton:
        - 871 evaluated chromosome

## Design Choice:

The code follows the structure of a genetic algorithm, which includes the representation of individuals as chromosomes, a mechanism for generating the initial population, a fitness function to evaluate the quality of individuals, and a mating process for creating a new generation. The algorithm employs elitism, selecting a portion of the top-performing individuals to directly pass to the next generation. The rest of the new generation is created through crossover (mating) and mutation.

The chromosomes in this genetic algorithm represent strings of characters from the defined set of genes (GENES). The Individual class encapsulates an individual in the population, with methods for generating mutated genes, creating a genome (random initial chromosome), and performing crossover during mating. The mutation is introduced probabilistically during crossover and also independently.

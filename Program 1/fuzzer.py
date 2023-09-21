import random
import subprocess
from typing import Union
from gcovr.gcov import process_gcov_data
from gcovr.utils import AlwaysMatchFilter
from locale import getpreferredencoding
import subprocess
import time
import sys
import os

if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        pass
    else:
        exit()
else:
    exit()


def main():

    log = False

    if "-log" in sys.argv:
        log = True

    
    program = ProgramRunner([sys.argv[1]])
    program.run()

    programCoverage = myCoverage(program_src=program)

    seeds = ["2 + 2", "8 + 9", "100 / 10"]

    mfuzzer = MutationFuzzer(seed=seeds)


    coverageTrack = []
    expTrack = []

    start_time = time.time()

    while (time.time() - start_time) < 55:
        
        exp = mfuzzer.fuzz()
        
        expTrack.append(exp)
        
        program.setProgram([sys.argv[1], str(exp)])
        
        result = program.run()

        if log == True:
            print(result)

        programCoverage.run()

        coverageTrack.append(programCoverage.covered_lines)
        if programCoverage.covered_lines == programCoverage.total_lines:
            break

    print(expTrack)
    print(coverageTrack[-1])
    programCoverage.printLines()

Outcome = str

class Runner:
    """Base class for testing inputs."""

    # Test outcomes
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"

    def __init__(self) -> None:
        """Initialize"""
        pass

    def run(self, inp: str) -> any:
        """Run the runner with the given input"""
        return (inp, Runner.UNRESOLVED)

class PrintRunner(Runner):
    """Simple runner, printing the input."""

    def run(self, inp) -> any:
        """Print the given input"""
        print(inp)
        return (inp, Runner.UNRESOLVED)

class ProgramRunner(Runner):
    """Test a program with inputs."""
    def __init__(self, program: Union[str, list[str]]) -> None:
        """Initialize.
        `program` is a program spec as passed to `subprocess.run()`"""
        self.program = program


    def setProgram(self, program: Union[str, list[str]]) -> None:
        self.program = program

    def getProgram(self) -> Union[str, list[str]]:
        return self.program

    def run_process(self, inp: str = "") -> subprocess.CompletedProcess:
        """Run the program with `inp` as input.
        Return result of `subprocess.run()`."""
        return subprocess.run(self.program,
                            input=inp,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    def run(self, inp: str = "") -> tuple[subprocess.CompletedProcess, Outcome]:
        """Run the program with `inp` as input.  
        Return test outcome based on result of `subprocess.run()`."""
        result = self.run_process(inp)

        if result.returncode == 0:
            outcome = self.PASS
        elif result.returncode < 0:
            outcome = self.FAIL
        else:
            outcome = self.UNRESOLVED

        return (result, outcome)

class Fuzzer:
    """Base class for fuzzers."""

    def __init__(self) -> None:
        """Constructor"""
        pass

    def fuzz(self) -> str:
        """Return fuzz input"""
        return ""

    def run(self, runner: Runner = Runner()) -> tuple[subprocess.CompletedProcess, Outcome]:
        """Run `runner` with fuzz input"""
        return runner.run(self.fuzz())

    def runs(self, runner: Runner = PrintRunner(), trials: int = 10) -> list[tuple[subprocess.CompletedProcess, Outcome]]:
        """Run `runner` with fuzz input, `trials` times"""
        return [self.run(runner) for i in range(trials)]


# ========================= MUTATION ===========================



def delete_random_character(s: str) -> str:
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]


def insert_random_character(s: str) -> str:
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

def replace_random_character(s): # Or replace
    """Returns s with a random bit replace in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]


def swap_random_characters(s: str) -> str:
    """Returns s with a random two character Swaped"""
    char_list = list(s)

    # Find the indices of the characters to swap
    index_char1 = random.randint(0, len(s) - 1)
    index_char2 = random.randint(0, len(s) - 1)

    # Swap the characters in the list
    char_list[index_char1], char_list[index_char2] = char_list[index_char2], char_list[index_char1]

    # Convert the list back to a string
    result_string = ''.join(char_list)

    return result_string


def mutate(s: str) -> str:
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        replace_random_character,
        swap_random_characters
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)

class MutationFuzzer(Fuzzer):
    """Base class for mutational fuzzing"""

    def __init__(self, seed: list[str], min_mutations: int = 2, max_mutations: int = 10) -> None:
        """Constructor.
        `seed` - a list of (input) strings to mutate.
        `min_mutations` - the minimum number of mutations to apply.
        `max_mutations` - the maximum number of mutations to apply.
        """
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self) -> None:
        """Set population to initial seed.
        To be overloaded in subclasses."""
        self.population = self.seed
        self.seed_index = 0

    def mutate(self, inp: str) -> str:
        return mutate(inp)

    def create_candidate(self) -> str:
        """Create a new candidate by mutating a population member"""
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def fuzz(self) -> str:
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = chr(0)
            while (chr(0) in self.inp):
                self.inp = self.create_candidate()

        return self.inp



# ============================ Coverage ==========================



class Options:
    exclude = []
    exclude_function_lines = False
    exclude_internal_functions = False
    exclude_lines_by_pattern = '.*[GL]COVR?_EXCL_LINE.*'
    exclude_throw_branches = False
    exclude_unreachable_branches = False
    filter = [AlwaysMatchFilter()]
    gcov_ignore_parse_errors = False
    keep = True
    objdir = '.'
    root_dir = '.'
    source_encoding = getpreferredencoding()
    starting_dir = '.'
    verbose = False

class myCoverage():
    def __init__(self, program_src: ProgramRunner) -> None:

        self.program_src = program_src
        self.covdata = dict()

        self.total_lines = 0
        self.covered_lines = 0
        self.discovered_statements = set()

    def compile_gcov(self):
        # print(self.program_src.getProgram())
        return subprocess.run(["gcov", self.program_src.getProgram()[0]],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    def run(self):
        self.compile_gcov()
        process_gcov_data(self.program_src.getProgram()[0] + ".c.gcov", self.covdata, None, Options())
        
        self.total_lines = 0
        self.covered_lines = 0
        for srcfile, filecov in self.covdata.items():
            for lineno, linecov in filecov.lines.items():
                if not linecov.noncode:
                    self.total_lines += 1
                if linecov.count > 0:
                    self.covered_lines += 1
                    self.discovered_statements.add(linecov.lineno)
    
    def printLines(self):
        self.run()
        for i in self.discovered_statements:
            print(f"{self.program_src.getProgram()[0]}:{i}", end=", ")
        print()
        


# Entry Point
if __name__ == "__main__":
    main()

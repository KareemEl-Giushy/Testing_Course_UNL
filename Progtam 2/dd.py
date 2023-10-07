import subprocess
import os
import json
import sys
from fuzzingbook.Fuzzer import ProgramRunner, Runner
from fuzzingbook.Reducer import CachingReducer


def main():

    Logging = False

    if len(sys.argv) < 3:
        print("You don't have suffient input")
        exit()

    if '-log' in sys.argv:
        Logging = True

    tFile = sys.argv[1]
    oracle = sys.argv[2]

    oracle_runner = ExternalBinaryProgramRuner(program=oracle)
    
    r_input = ''
    with open(tFile, 'rt') as f:
        r_input = f.read()

    dd_reducer = myDeltaDebuger(oracle_runner, log_test=Logging)

    dd_reducer.reduce(r_input)

    print(dd_reducer)

class ExternalBinaryProgramRuner(ProgramRunner):
    def run_process(self, progtxt = ""):
            """Run the program with `inp` as input.  
            Return result of `subprocess.run()`."""
            
            tempF = './temp.c'
            with open(tempF, 'wt') as f:
                f.write(progtxt)
                f.close()

            sp = subprocess.run([self.program, tempF],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            
            os.remove(tempF)

            return sp

class myDeltaDebuger(CachingReducer):
    def __init__(self, runner, log_test=False):
        super().__init__(runner, log_test)
        self.reducedLines = []
        self.out = {
            'lines': {
                'remain': 0,
                'removed': 0,
                'variants': 0,
                'reduced': 0
            },
            'characters': {
                'remain': 0,
                'removed': 0,
                'variants': 0,
                'reduced': 0
            }
        }
    
    def __repr__(self) -> str:
        return json.dumps(self.out, indent=4)

    def line_reducer(self, inp: list) -> list: 
        n = 2
        while len(inp) >= 2:
            start = 0.0
            subset_length = len(inp) / n
            is_interesting = False

            while start < len(inp):
                complement = inp[:int(start)] + inp[int(start + subset_length):]

                if self.test("".join(complement)) == Runner.PASS:
                    inp = complement
                    n = max(n - 1, 2)
                    is_interesting = True
                    break

                start += subset_length

            if not is_interesting:
                if n == len(inp):
                    break
                n = min(n * 2, len(inp))

        return inp

    def line_tester(self, complement: str, i: int, lines: list) -> bool:
        ttxt = lines.copy()
        ttxt[i] = complement
        if self.test("".join(ttxt)) == Runner.PASS:
            return True

        return False

    def char_reducer(self, lines: list) -> list:
        final = []
        for i, l in enumerate(lines):
            
            n = 2
            while len(l) >= 2:
                start = 0.0
                subset_length = len(l) / n
                is_interesting = False

                while start < len(l):
                    complement = l[:int(start)] + l[int(start + subset_length):]

                    if self.line_tester(complement, i, lines):
                        l = complement
                        n = max(n - 1, 2)
                        is_interesting = True
                        break

                    start += subset_length

                if not is_interesting:
                    if n == len(l):
                        break
                    n = min(n * 2, len(l))
            final.append(l)

        return final

    def reduce(self, inp):

        # reduce lines
        self.reset()
        reducedLines: list = self.line_reducer(inp.split("\n"))

        self.out['lines']['remain'] = len(reducedLines)
        self.out['lines']['removed'] = len(inp.split("\n")) - len(reducedLines)
        self.out['lines']['variants'] = len(self.cache)
        self.out['lines']['reduced'] = "\n".join(reducedLines)

        #reduce Characters for each line
        self.reset()
        red: list = self.char_reducer(reducedLines)
        red = "\n".join(red)

        self.out['characters']['remain'] = len(red)
        self.out['characters']['removed'] = len("\n".join(reducedLines)) - len(red)
        self.out['characters']['variants'] = len(self.cache)
        self.out['characters']['reduced'] = red

        return "\n".join(red)

if __name__ == "__main__":
    main()
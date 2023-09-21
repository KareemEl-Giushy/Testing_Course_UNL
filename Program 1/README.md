# Fuzzer And Coverage For A Simple ```C``` Calculator

## Installation:

Make sure to have the following package in your system.

```
pip install gcovr==5.0
```

OR you can just install the ```requirements.txt``` file provided with the code.

Also, make sure to compile the ***calc.c*** using gcc compiler with the coverage flag:

```
gcc --coverage calc.c -o calc 
```

## Executing / Running The Script:

**! When executing, make sure you pass the porgram not the script**

1. Open your terminal and make sure you are in the same directory as the script and enter the following command:
    ```
    python fuzzer.py <Calculator Excutable File Path> <argument(-log)>
    ```
2. To display logs please make sure you add ***-log*** argument.
    ```
    # Example
    python fuzzer.py ./calc -log
    ```

3. You are Done ... Enjoy :)

### Notes:
Make sure to rename the executable calc file to ```calc``` with no extension.

## Design Choice:

The approach chosen to implement the ```Fuzzer``` is to mutate an input seed and feed that input into the program. At each step of execution, it starts checking if the number of covered statements is equal to the total number of statements presented in the script. When the condition is satisfied, it breaks from the loop. In addition, any lines that have curly braces and other syntactical properties are not counted as a statement.


This approach is guaranteed to find a solution. For further enhancement, a time limit is created via a while loop. this guarantees that the program doesn't run forever but instead, it runs for a maximum of 55 seconds. A good seed makes a lot of difference. In my case, I was lucky to select a good set of seeds.
# Delta Debugger (Prgoram 2)
A delta debugger script to reduce input text based on what an oracle finds interesting. (e.g. ```0``` if it is interesting and ```1``` if it's not)

## Installation:

Make sure to have the following package in your system.

```
pip install fuzzingbook==1
```

OR you can just install the ```requirements.txt``` file provided with the code.

## Executing / Running The Script:

**Make sure to include the ```input file``` first and then the ```Oracal File``` in that order.**

1. Open your terminal and make sure you are in the same directory as the script and enter the following command:
    ```
    python dd.py <Text Input File Path> <Oracle File Path> <argument(-log)>
    ```
2. To display logs please make sure you add ***-log*** argument.
    ```
    # Example
    python dd.py ./hello1.c ./cfile.test.sh -log
    ```

3. You are Done ... Enjoy :)

## Design Choice:

The chosen approach to implement the ```Delta Debugger``` involves a divide-and-conquer algorithm, employing a binary search technique. This approach is executed in two distinct steps using the same algorithm. First, it focuses on reducing the number of lines within the text input by processing an array containing all lines in the text. In the second step, the goal is to minimize the number of characters within each individual line.

In the context of code design, the code featured in the book served as the foundation for modified classes that incorporate distinct implementations of functions. A new program runner was introduced to enable the creation of temporary files and pass them to the Oracle. Additionally, a new form of Delta Debugger implementation was introduced, consisting of three main functions: ```line_reducer```, ```char_reducer```, and ```line_tester```. These all functions is used to make up the logic of the main ```reduce``` function.

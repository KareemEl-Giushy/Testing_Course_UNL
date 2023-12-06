# Symbolic Execution (Prgoram 4)
A symbolic execution (SE) algorithm for deep neural networks extracts constraints for all neurons in the neural network so that it can be evaluated by `Z3`. A deep neural network (DNN) is a specific class of program, and symbolic execution enables the execution of the DNN on symbolic inputs, returning symbolic results.

## Installation:
There are no external packages needed to run this program except for the **Z3-Solver**.

## Executing / Running The Script:

1. Open your terminal and make sure you are in the same directory as the script and enter the following command:
    ```
    python se.py
    ```
2. You are Done ... Enjoy :)

## Design Choice:

The code implements symbolic execution by first creating a symbolic version of the deep neural network (DNN) using the `symbolize()` function. It takes into consideration the input layer by extracting it from the incoming edge weights stored in the neurons (nodes) of the first hidden layer. Three different loops are implemented to generate the symbolized deep neural network for each type of layer (input, hidden, output).

Furthermore, the second part of the code involves extracting constraints for every neuron (node), considering the `ReLU` activation function. All the extracted constraints are summed together using `z3.Sum()`, and then the bias is added. Depending on whether the `ReLU` function is enabled or not, the `ReLU` condition is added to the constraints.
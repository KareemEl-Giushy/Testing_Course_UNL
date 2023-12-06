import z3

'''
dnn = [
    hiddenlayer1: [neuron, neuron, ...]
    hiddenlayer2: [neuron, neuron, ...]
    ...
    outputlayer: [neuron, neuron, ...]
]
'''
def symbolize(dnn):

    symbolized_dnn = []

    #Input Layer Symbolization
    symbolized_dnn.append([])
    for i in range(len(dnn[0][0])):
        symbolized_dnn[-1].append(z3.Real(f"i{i}"))

    # Hidden Layers Symbolization
    for i, layer in enumerate(dnn):
        if i == len(dnn) - 1:
            break
        symbolized_dnn.append([])
        for j, _ in enumerate(layer):
            symbolized_dnn[-1].append(z3.Real(f"n{i}_{j}"))
    
    # Output Layer Symbolization
    symbolized_dnn.append([])
    for i, _ in enumerate(dnn[-1]):
        symbolized_dnn[-1].append(z3.Real(f"o{i}"))

    return symbolized_dnn

def symbolic_execution(dnn):
    sym_dnn = symbolize(dnn)
    solver = z3.Solver()

    # Hidden Layers Constraint Extraction
    for i, layer in enumerate(dnn):
        for t, neuron in enumerate(layer):
            arr_of_w = []
            for j, weight in enumerate(neuron[0]):
                arr_of_w.append(weight * sym_dnn[i][j])

            if neuron[-1]: # if relu is enabled
                solver.add(sym_dnn[i+1][t] == z3.If( z3.Sum(arr_of_w) + neuron[1] <= 0, 0, z3.Sum(arr_of_w) + neuron[1]))
            else:
                solver.add(sym_dnn[i+1][t] == z3.Sum(arr_of_w) + neuron[1])

    return z3.And(solver.assertions())



def test():
    # each neuron takes the form:
    # ([list of weights], bias, should it use activation function relu)
    #
    n0_0 = ([1.0, -1.0], 0.0, True)
    n0_1 = ([1.0, 1.0], 0.0, True)
    #
    # each layer takes the form:
    # [list of neurons]
    #
    hidden_layer0 = [n0_0, n0_1]

    n1_0 = ([0.5, -0.2], 0.0, True)
    n1_1 = ([-0.5, 0.1], 0.0, True)
    hidden_layer1 = [n1_0, n1_1]

    o0 = ([1.0, -1.0], 0.0, False)  
    o1 = ([-1.0, 1.0], 0.0, False)
    output_layer = [o0, o1]

    #
    # the DNN takes the form:
    # [list of layers]
    #
    dnn = [hidden_layer0, hidden_layer1, output_layer]
    # symbolic_execution() is something you implement:
    #   it returns a single (quite large) Z3 formula representing the symbolic states of the DNN
    symbolic_states = symbolic_execution(dnn)

    print('done, obtained symbolic states for DNN with 2 inputs, 2 hidden layers with 2 neurons each, and 2 outputs in 0.1s')
    assert z3.is_expr(symbolic_states)  #symbolic_states is a Z3 formula

    print(symbolic_states)
    # And(n0_0 == If(0 + 1*i0 + -1*i1 <= 0, 0, 0 + 1*i0 + -1*i1),
    #     n0_1 == If(0 + 1*i0 + 1*i1 <= 0, 0, 0 + 1*i0 + 1*i1),
    #     n1_0 ==
    #     If(0 + 1/2*n0_0 + -1/5*n0_1 <= 0,
    #        0,
    #        0 + 1/2*n0_0 + -1/5*n0_1),
    #     n1_1 ==
    #     If(0 + -1/2*n0_0 + 1/10*n0_1 <= 0,
    #        0,
    #        0 + -1/2*n0_0 + 1/10*n0_1),
    #     o0 == 0 + 1*n1_0 + -1*n1_1,
    #     o1 == 0 + -1*n1_0 + 1*n1_1)
    print('generating random inputs/outputs')
    z3.solve(symbolic_states)  # we get o0, o1 = 0, 0
    # [i1 = 4,
    # n0_0 = 2,
    # n1_1 = 0,
    # i0 = 6,
    # n0_1 = 10,
    # o1 = 0,
    # n1_0 = 0,
    # o0 = 0]

    print('finding outputs when inputs are fixed [i0 == 1, i1 == -1]')
    i0, i1, n0_0, n0_1, o0, o1 = z3.Reals("i0 i1 n0_0 n0_1 o0 o1")
    g = z3.And([i0 == 1.0, i1 == -1.0])
    z3.solve(z3.And(symbolic_states, g))  # we get o0, o1 = 1, -1
    # [n1_1 = 0,
    # i0 = 1,
    # n0_1 = 0,
    # o1 = -1,
    # o0 = 1,
    # n0_0 = 2,
    # n1_0 = 1,
    # i1 = -1]

    print("Prove that if (n0_0 > 0.0 and n0_1 <= 0.0) then o0 > o1")
    g = z3.Implies(z3.And([n0_0 > 0.0, n0_1 <= 0.0]), o0 > o1)
    print(g)  # Implies(And(n0_0 > 0, n0_1 <= 0), o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))
    # proved

    print("Prove that when (i0 - i1 > 0 and i0 + i1 <= 0), then o0 > o1")
    g = z3.Implies(z3.And([i0 - i1 > 0.0, i0 + i1 <= 0.0]), o0 > o1)
    print(g)  # Implies(And(i0 - i1 > 0, i0 + i1 <= 0), o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))
    # proved

    print("Disprove that when i0 - i1 > 0, then o0 > o1")
    g = z3.Implies(i0 - i1 > 0.0, o0 > o1)
    print(g)  # Implies(i0 - i1 > 0, o0 > o1)
    z3.prove(z3.Implies(symbolic_states, g))
    # counterexample
    # [n1_1 = 0,
    #  i0 = 6,
    #  n0_1 = 10,
    #  o1 = 0,
    #  o0 = 0,
    #  i1 = 4,
    #  n1_0 = 0,
    #  n0_0 = 2]

def test2():

    n0_0 = ([1.0, -1.0, -0.6], 0.012, False)
    n0_1 = ([1.0, 1.0, 0.6], 0.0, False)
    n0_2 = ([1.0, 1.0, -1.0], 0.2, False)
    n0_3 = ([1.0, 1.0, 1.0], 0.5, False)

    hidden_layer0 = [n0_0, n0_1, n0_2, n0_3]

    n1_0 = ([0.5, -0.2, -0.3, -0.9], 0.0, False)
    n1_1 = ([-0.5, 0.1, -0.7, 0.7], 1.0, False)
    n1_2 = ([-0.5, 0.1, 0.4, 0.06], 0.123, False)
    n1_3 = ([-0.5, 0.1, 0.7, 0.0], 0.265, False)

    hidden_layer1 = [n1_0, n1_1, n1_2, n1_3]

    n2_0 = ([0.5, -0.2, 0.4, -0.32], 0.782, False)
    n2_1 = ([-0.5, 0.1, 0.8, -0.78], 0.0, False)
    n2_2 = ([-0.5, 0.1, 0.9, -0.1], 0.0, False)
    n2_3 = ([-0.5, 0.1, -0.4, 0.99], 0.265, False)

    hidden_layer2 = [n2_0, n2_1, n2_2, n2_3]

    o0 = ([1.0, -1.0, 1.0, -1.0], 0.0, True)  
    o1 = ([-1.0, 1.0, -1.0, 1.0], 0.0, True)
    output_layer = [o0, o1]



    dnn = [hidden_layer0, hidden_layer1, hidden_layer2, output_layer]
    
    symbolic_states = symbolic_execution(dnn)
    
    print('done, obtained symbolic states for DNN with 3 inputs, 3 hidden layers with 4 neurons each, and 2 outputs in 0.1s')
    assert z3.is_expr(symbolic_states)  #symbolic_states is a Z3 formula

    print(symbolic_states)
    
    print('='*30)
    print('generating random inputs/outputs')
    z3.solve(symbolic_states)

    print('='*30)
    print('finding outputs when inputs are fixed [i0 == 1, i1 == -1, i3 == 0.6]')
    i0, i1, i3, n0_0, n0_1, n0_2, o0, o1 = z3.Reals("i0 i1 i3 n0_0 n0_1 n0_2 o0 o1")
    
    g = z3.And([i0 == 1.0, i1 == -1.0, i3 == 0.6])
    z3.solve(z3.And(symbolic_states, g)) 
    
    print('='*30)
    print("Prove that if (n0_0 > 6.0 and n0_1 == 100.0 and n0_2 == 12.0) then o0 < o1")
    g = z3.Implies(z3.And([n0_0 < 6.0, n0_1 == 100.0, n0_2 == 12.0]), o0 < o1)
    print(g)
    z3.prove(z3.Implies(symbolic_states, g))
    # proved

    print('-'*30)
    print("Disprove that when (i0 - i1 > 3.0 and i0 + i1 <= 1.0 and n0_2 * n0_0 < 100), then o0 > o1")
    g = z3.Implies(z3.And([i0 - i1 > 3.0, i0 + i1 <= 1.0, n0_2 * n0_0 < 100]), o0 > o1)
    print(g)
    z3.prove(z3.Implies(symbolic_states, g))
    # disprove

    print('-'*30)
    print("Disprove that when i0 / i1 > 0, then o0 > o1")
    g = z3.Implies(i0 / i1 > 0.0, o0 > o1)
    print(g)
    z3.prove(z3.Implies(symbolic_states, g))
    #disprove

def test3():
    pass

if __name__ == "__main__":
    test()
    test2()
    test3()
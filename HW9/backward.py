import sys
import os
import numpy as np
import math
from logsum import log_sum


def initial_state(prior_data):
    prob = []
    for state in prior_data:
        prob.append(math.log(float(state.split(' ')[1])))
    return prob


def create_trans_matrix(trans_data):
    size = len(trans_data)
    trans_matrix = []
    for i in range(len(trans_data)):
        trans = []
        line = trans_data[i].split(' ')[1:]
        for j in range(len(line)-1):
            trans.append(math.log(float(line[j].split(':')[1])))
        trans_matrix.append(trans)
    return trans_matrix


def create_emit_matrix(emit_data):
    row = len(emit_data)
    col = len(emit_data[0].split(' ')[1:-1])
    vocab = []
    emit_matrix = []
    info = emit_data[0].split(' ')[1:-1]
    for word in info:
        vocab.append(word.split(':')[0])
    for i in range(len(emit_data)):
        list = []
        line = emit_data[i].split(' ')[1:-1]
        for j in range(col):
            list.append(math.log(float(line[j].split(':')[1])))
        emit_matrix.append(list)
    return vocab, emit_matrix


def backward(trans_matrix, observe_matrix):
    N_state = len(trans_matrix)
    T_observ = observe_matrix.shape[1]
    backward_matrix = np.zeros((N_state, T_observ-1))
    # initial step
    for i in range(N_state):
        backward_matrix[i,0] = math.log(1.0)
    # recursion step
    for t in range(T_observ-1):
        beta = backward_matrix[:, t - 1]
        for i in range(N_state):
            for j in range(N_state):
                if j == 0:
                    beta_sum = beta[j] + trans_matrix[i][j] + observe_matrix[j][t]
                else:
                    beta_sum = log_sum(beta_sum, beta[j] + trans_matrix[i][j] + observe_matrix[j][t])
            backward_matrix[i, t] = beta_sum
    return backward_matrix


def find_observe(sentence, vocab_list, emit_matrix, prob_matrix, trans_matrix):
    emit = np.array(emit_matrix)
    col_list = []
    for word in sentence:
        col = vocab_list.index(word)
        col_list = [col] + col_list
    observe_matrix = emit[:, col_list]
    backward_matrix = backward(trans_matrix, observe_matrix)
    for i in range(len(trans_matrix)):
        if i == 0:
            res = prob_matrix[i] + backward_matrix[i][-1] + observe_matrix[i][-1]
        else:
            res = log_sum(res, prob_matrix[i] + backward_matrix[i][-1] + observe_matrix[i][-1])
    print res


def create_dev_matrix(dev_data, vocab_list, emit_matrix, prob_matrix, trans_matrix):
    for line in dev_data:
        sentence = []
        string = line.split(' ')
        for word in string:
            sentence.append(word)
        find_observe(sentence, vocab_list, emit_matrix, prob_matrix, trans_matrix)


# forward.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
if len(sys.argv) != 5 or not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]) or not os.path.isfile(sys.argv[3]) or not os.path.isfile(sys.argv[3]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as dev_f:
        dev_data = dev_f.read().splitlines()
    with open(sys.argv[2], 'r') as trans_f:
        trans_data = trans_f.read().splitlines()
    with open(sys.argv[3], 'r') as emit_f:
        emit_data = emit_f.read().splitlines()
    with open(sys.argv[4], 'r') as prior_f:
        prior_data = prior_f.read().splitlines()
    if not dev_data or not trans_data or not emit_data or not prior_data:
        print "empty file"
    else:
        prob_matrix = initial_state(prior_data)
        trans_matrix = create_trans_matrix(trans_data)
        vocab_list, emit_matrix = create_emit_matrix(emit_data)
        create_dev_matrix(dev_data, vocab_list, emit_matrix, prob_matrix, trans_matrix)

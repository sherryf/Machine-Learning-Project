import sys
import os
import numpy as np
import math


def initial_state(prior_data):
    prob = []
    for state in prior_data:
        prob.append(math.log(float(state.split(' ')[1])))
    return prob


def create_trans_matrix(trans_data):
    size = len(trans_data)
    trans_matrix = []
    states = []
    for i in range(len(trans_data)):
        trans = []
        states.append(trans_data[i].split(' ')[0])
        line = trans_data[i].split(' ')[1:]
        for j in range(len(line)-1):
            trans.append(math.log(float(line[j].split(':')[1])))
        trans_matrix.append(trans)
    return trans_matrix, states


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


def viterbi_func(prob_matrix, trans_matrix, observe_matrix):
    N_state = len(trans_matrix)
    T_observ = observe_matrix.shape[1]
    viterbi_matrix = np.zeros((N_state, T_observ))
    backpoint_matrix = np.zeros((N_state, T_observ))
    # initial step
    for i in range(N_state):
        viterbi_matrix[i,0] = observe_matrix[i][0] + prob_matrix[i]
        backpoint_matrix[i,0] = 0
    # recursion step
    for t in range(1, T_observ):
        viterbi = viterbi_matrix[:,t-1]
        for i in range(N_state):
            for j in range(N_state):
                if j == 0:
                    max_value = viterbi[j] + trans_matrix[j][i] + observe_matrix[i][t]
                    max_tag = 0
                else:
                    comp = viterbi[j] + trans_matrix[j][i] + observe_matrix[i][t]
                    if comp > max_value:
                        max_value = comp
                        max_tag = j
                    # print comp

            viterbi_matrix[i,t] = max_value
            backpoint_matrix[i,t-1] = max_tag
            backpoint_matrix[i,t] = i
    # print viterbi_matrix
    #
    # print backpoint_matrix
    return backpoint_matrix, viterbi_matrix


def find_observe(sentence, vocab_list, emit_matrix, prob_matrix, trans_matrix):
    emit = np.array(emit_matrix)
    col_list = []
    for word in sentence:
        col = vocab_list.index(word)
        col_list.append(col)
    observe_matrix = emit[:, col_list]
    backpoint_matrix, viterbi_matrix = viterbi_func(prob_matrix, trans_matrix, observe_matrix)
    res = []
    index = np.argmax(viterbi_matrix[:, -1])
    res.insert(0,index)
    for i in xrange(len(col_list)-2,-1,-1):
        index = int(backpoint_matrix[index, i])
        res.insert(0, index)
    return res


def create_dev_matrix(dev_data, vocab_list, emit_matrix, prob_matrix, trans_matrix, states_list):
    dev = []
    for line in dev_data:
        sentence = []
        string = line.split(' ')
        for word in string:
            sentence.append(word)
        tag = find_observe(sentence, vocab_list, emit_matrix, prob_matrix, trans_matrix)
        # break
        for i in range(len(sentence)):
            print sentence[i] + '_' + states_list[tag[i]],
        print
    return dev


# python viterbi.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
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
        trans_matrix, states_list = create_trans_matrix(trans_data)
        vocab_list, emit_matrix = create_emit_matrix(emit_data)
        dev_matrix = create_dev_matrix(dev_data, vocab_list, emit_matrix, prob_matrix, trans_matrix, states_list)


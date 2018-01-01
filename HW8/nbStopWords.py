import sys
import os
import math


def create_table(file, table):
    if not os.path.isfile(file):
        print "no file"
    else:
        with open(file, 'r') as f:
            words = f.read().splitlines()
            for w in words:
                word = w.lower()
                if word not in table:
                    table[word] = 1
                else:
                    table[word] = table[word] + 1
            return table


def initial_table(file, total_table):
    if not os.path.isfile(file):
        print "no file"
    else:
        with open(file, 'r') as f:
            words = f.read().splitlines()
            for w in words:
                word = w.lower()
                if word not in total_table:
                    total_table[word] = 1
                else:
                    total_table[word] = total_table[word] + 1
            return total_table


def count_class(contents):
    con = 0
    lib = 0
    con_table = {}
    lib_table = {}
    total_table = {}
    for i in contents:
        total_table = initial_table(i, total_table)
        if i[:3] == "con":
            con += 1
            con_table = create_table(i, con_table)
        else:
            lib += 1
            lib_table = create_table(i, lib_table)
    return total_table, con_table, lib_table, con, lib


def calculate_likelihood(total_table, table, vocab, sum, smooth_p):
    prob_table = {}
    for word in total_table:
        if word not in table:
            n_k = 0
        else:
            n_k = table[word]
        prob_table[word] = (n_k + smooth_p) * 1.0/ (sum + smooth_p * vocab)
        # print word + ": " + str(prob_table[word])
    return prob_table


def train_files(trains, prob_con_table, prob_lib_table, prob_con, prob_lib):
    correct = 0
    for tdata in trains:
        is_con = 0
        p_con = math.log(prob_con)
        p_lib = math.log(prob_lib)
        epsilon = math.log(1.0*math.e**-16)
        if tdata[:3] == "con":
            is_con = 1
        if not os.path.isfile(tdata):
            print "no file"
        else:
            with open(tdata, 'r') as file:
                fs = file.read().splitlines()
                for data in fs:
                    word = data.lower()
                    if word in prob_con_table:
                        p_con += math.log(prob_con_table[word])
                    else:
                        p_con += epsilon
                    if word in prob_lib_table:
                        p_lib += math.log(prob_lib_table[word])
                    else:
                        p_lib += epsilon
                # print str(p_con) + ": " + str(p_lib)
                if p_con > p_lib:
                    if is_con == 1:
                        correct += 1
                    print "C"
                else:
                    if is_con == 0:
                        correct += 1
                    print "L"
    accuracy = float(correct)/len(trains)
    print "Accuracy: %.04f" % accuracy


if len(sys.argv) != 4 or not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.read().splitlines()
    with open(sys.argv[2], 'r') as train_f:
        trains = train_f.read().splitlines()
    if not contents or not trains:
        print "empty file"
    else:
        iter = 1
        N = int(sys.argv[3])
        total_table, con_table, lib_table, num_con, num_lib = count_class(contents)
        for key, value in sorted(total_table.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if iter <= N:
                total_table.pop(key)
                con_table.pop(key)
                lib_table.pop(key)
                iter += 1
        sum_con = sum(con_table.values())
        sum_lib = sum(lib_table.values())
        prob_con = num_con*1.0/(num_lib+num_con)
        prob_lib = num_lib*1.0/(num_lib+num_con)
        smooth_p = 1
        prob_con_table = calculate_likelihood(total_table, con_table, len(total_table), sum_con, smooth_p)
        prob_lib_table = calculate_likelihood(total_table, lib_table, len(total_table), sum_lib, smooth_p)
        train_files(trains, prob_con_table, prob_lib_table, prob_con, prob_lib)
import sys
import os


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
                    total_table[word] = 0
            return total_table


def update_table(total_table, table):
    for word in table:
        total_table[word] = table[word]
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

if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.read().splitlines()
    if not contents:
        print "empty file"
    else:
        iter = 1
        total_table, con_table, lib_table, num_con, num_lib = count_class(contents)
        sum_con = sum(con_table.values())
        sum_lib = sum(lib_table.values())
        prob_con = num_con*1.0/(num_lib+num_con)
        prob_lib = num_lib*1.0/(num_lib+num_con)
        smooth_p = 1
        prob_con_table = calculate_likelihood(total_table, con_table, len(total_table), sum_con, smooth_p)
        prob_lib_table = calculate_likelihood(total_table, lib_table, len(total_table), sum_lib, smooth_p)
        for key, value in sorted(prob_lib_table.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if iter <= 20:
                iter += 1
                print "%s %.04f" % (key, value)
        print
        iter = 1
        for key, value in sorted(prob_con_table.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if iter <= 20:
                iter += 1
                print "%s %.04f" % (key, value)
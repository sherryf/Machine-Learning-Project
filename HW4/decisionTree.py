import sys
import os
import math
import numpy as np

def readdata(dataset):
    info = dataset[0].split(",")
    length = len(dataset[0].split(",")) -1
    num_data = len(dataset) - 1
    plus_value = ['democrat', 'A', 'y', 'before1950', 'yes', 'morethan3min', 'fast', 'expensive', 'high', 'Two', 'large']
    # initial array only 0 and 1
    array = np.zeros((num_data, length+1))
    row = 0
    col = 0
    for i in dataset[1:]:
        data = i.split(",")
        for d in data:
            if d in plus_value:
                attr_name = d
                array[row, col] = 1
            col += 1
        row += 1
        col = 0
    # print info
    return array, attr_name, info

def createRoot(data_array):
    row = data_array.shape[0]
    col = data_array.shape[1]
    postive = sum(data_array[:, col-1])
    negative = row - postive
    entropy = calculate_entropy(postive, negative)
    return postive, negative, entropy

def calculate_entropy(postive, negative):
    res = 0
    if postive == 0 or negative == 0:
        res = 0
    else:
        sum = postive + negative
        res = -1.0 * postive / sum * math.log(postive / sum, 2) - negative / sum * math.log(negative / sum, 2)
    return res

def choose_node(data_array, c_entropy):
    max_entropy = 0
    max_col = 0
    f_pos_pos = 0.0
    f_pos_neg = 0.0
    f_neg_pos = 0.0
    f_neg_neg = 0.0
    for c in range(data_array.shape[1]-1):
        total = data_array.shape[0]
        postive = sum(data_array[:, c])
        negative = total - postive
        pos_pos = 0.0
        pos_neg = 0.0
        neg_pos = 0.0
        neg_neg = 0.0
        for r in range(data_array.shape[0]):
            if data_array[r,c] == 1 and data_array[r, data_array.shape[1]-1] == 1:
                pos_pos += 1
            if data_array[r,c] == 1 and data_array[r, data_array.shape[1]-1] == 0:
                pos_neg += 1
            if data_array[r,c] == 0 and data_array[r, data_array.shape[1]-1] == 1:
                neg_pos += 1
            if data_array[r,c] == 0 and data_array[r, data_array.shape[1]-1] == 0:
                neg_neg += 1
        # print pos_neg, pos_pos, postive
        pos_entropy = calculate_entropy(pos_pos, pos_neg)
        neg_entropy = calculate_entropy(neg_pos, neg_neg)
        entropy = c_entropy - postive/total * pos_entropy - negative/total * neg_entropy
        if entropy > max_entropy:
            max_entropy = entropy
            max_col = c
            f_pos_pos, f_pos_neg, f_neg_pos, f_neg_neg = pos_pos, pos_neg, neg_pos, neg_neg
    return f_pos_pos, f_pos_neg, f_neg_pos, f_neg_neg, max_col, max_entropy

def shrink_array(data_array, max_col):
    left_array = data_array[data_array[:, max_col] == 0]
    right_array = data_array[data_array[:, max_col] == 1]
    return left_array, right_array

def get_attr_name(attr_name):
    neg_name = ""
    if attr_name == "y" or attr_name == "democrat":
        attr_name = "y"
        neg_name = "n"
    elif attr_name == "A":
        neg_name = "notA"
    elif attr_name == "before1950":
        neg_name = "after1950"
    elif attr_name == "yes":
        neg_name = "no"
    elif attr_name == "morethan3min":
        neg_name = "lessthan3min"
    elif attr_name == "fast":
        neg_name = "slow"
    elif attr_name == "expensive":
        neg_name = "cheap"
    elif attr_name == "Two":
        neg_name = "MoreThanTwo"
    elif attr_name == "large":
        neg_name = "small"
    else:
        attr_name = "y"
        neg_name = "n"
    return attr_name, neg_name

class Node:
    """
    Class TreeNode
    """
    def __init__(self, left=None, right=None, attr_name="", nextname ="", entropy=0, pos=0, neg=0, mutual_info=0, classify=0):
        self.left = left
        self.right = right
        self.attr_name = attr_name
        self.nextname = nextname
        self.entropy = entropy
        self.pos = pos
        self.neg = neg
        self.mutual_info = mutual_info
        self.classify = classify

def build_tree(data_array, pos, neg, c_entropy, attr_name, info_list, info_col, depth):
    if depth >= 3 or data_array.shape[1] <= 1:
        return
    root = Node()
    root.pos = int(pos)
    root.neg = int(neg)
    root.attr_name = info_list[info_col]
    root.entropy = c_entropy
    if pos > neg:
        root.classify = 1
    else:
        root.classify = 0
    pos_pos, pos_neg, neg_pos, neg_neg, max_col, n_entropy = choose_node(data_array, c_entropy)
    left_array, right_array = shrink_array(data_array, max_col)
    root.mutual_info = n_entropy
    root.nextname = info_list[max_col]
    # pos_pos, pos_neg, neg_pos, neg_neg, max_col, n_entropy = choose_node(data_array, c_entropy)
    if left_array.shape[0] == 0:
        return root
    if right_array.shape[0] == 0:
        return root
    if n_entropy >= 0.1:
        pos, neg, c_entropy = createRoot(left_array)
        root.right = build_tree(left_array, pos, neg, c_entropy, info_list[max_col], info_list, max_col, depth+1)
        pos, neg, c_entropy = createRoot(right_array)
        root.left = build_tree(right_array, pos, neg, c_entropy, info_list[max_col], info_list, max_col, depth+1)
        # print info_list[max_col]
        # print createRoot(left_array)
        # print pos_pos, pos_neg, neg_pos, neg_neg, max_col, n_entropy
    return root

def print_tree(node, depth, isleft, pos_name, neg_name):
    if node == None:
        return
    if depth == 0:
        res = "[" + str(node.pos) + "+/" + str(node.neg) + "-]"
        print res
    elif depth == 1:
        if isleft == 1:
            res = node.attr_name + " = " + pos_name + ": [" + str(node.pos) + "+/" + str(node.neg) + "-]"
        else:
            res = node.attr_name + " = " + neg_name + ": [" + str(node.pos) + "+/" + str(node.neg) + "-]"
        print res
    else:
        if isleft == 1:
            res = "| " + node.attr_name + " = " + pos_name + ": [" + str(node.pos) + "+/" + str(node.neg) + "-]"
        else:
            res = "| " + node.attr_name + " = " + neg_name + ": [" + str(node.pos) + "+/" + str(node.neg) + "-]"
        print res
    print_tree(node.left, depth + 1, 1, pos_name, neg_name)
    print_tree(node.right, depth + 1, 0, pos_name, neg_name)

def go_tree(node, data, info_list, path):
    if node == None:
        return
    # if data[info_list.index(node.nextname)]
    if int(data[info_list.index(node.nextname)]) == 1:
        path.append(node.classify)
        go_tree(node.left, data, info_list, path)
    else:
        path.append(node.classify)
        go_tree(node.right, data, info_list, path)

def run_data(node, data_array, info_list):
    error = 0.0
    for data in data_array:
        path = []
        go_tree(node, data, info_list, path)
        if path[-1] != data[-1]:
            error += 1
    return error/float(data_array.shape[0])


if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as train_f:
        trainData = train_f.read().splitlines()
    with open(sys.argv[2], 'r') as test_f:
        testData = test_f.read().splitlines()
    if not trainData or not testData:
        print "empty file"
    else:
        data_array, attr_name, info_list = readdata(trainData)
        pos, neg, c_entropy = createRoot(data_array)
        tree = build_tree(data_array, pos, neg, c_entropy, attr_name, info_list, data_array.shape[1]-1, 0)
        pos_name, neg_name = get_attr_name(attr_name)
        print_tree(tree, 0, 0, pos_name, neg_name)
        train_error = run_data(tree, data_array, info_list)
        test_array, test_attr_name, test_info_list = readdata(testData)
        test_error = run_data(tree, test_array, info_list)
        print "error(train): " + str(train_error)
        print "error(test): " + str(test_error)

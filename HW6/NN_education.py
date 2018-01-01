import sys
import os
import math
import numpy as np

def loadtraindata(trainData):
    train_len = len(trainData) - 1
    attr = trainData[0].split(",")
    train_array = np.zeros((train_len, len(attr)+1))
    row = 0
    # normalize the data and load them
    for i in trainData[1:]:
        data = i.split(",")
        data[0] = float(data[0]) / 100.0
        data[1] = float(data[1]) / 100.0
        data[2] = float(data[2]) / 100.0
        data[3] = float(data[3]) / 100.0
        data[4] = float(data[4]) / 100.0
        train_array[row,0:len(attr)] = data
        train_array[row, -1] = 1
        row += 1
    return train_array

def loadkeydata(keyData):
    key_len = len(keyData)
    key_array = np.zeros((key_len, 1))
    row = 0
    for data in keyData:
        key_array[row] = float(data)/100.0
        row += 1
    return key_array

def forward(line, W1, W2, hidden_size):
    a1 = np.zeros((1, hidden_size+1))
    a1[-1] = 1
    for i in range(hidden_size):
        a1[0, i] = sum(np.multiply(W1[i], line))
    a1 = a1.tolist()[0]

    o1 = np.zeros((1, hidden_size+1))
    for i in range(hidden_size+1):
        o1[0, i] = sigmoid(a1[i])
    o1 = o1.tolist()[0]
    a2 = sum(np.multiply(o1, W2[0]))
    o2 = sigmoid(a2)
    return a1, o1, a2, o2

def cal_loss(o2, key):
    return 1.0/2*(key[0]-o2)**2

def backpropagation(a1, o1, a2, o2, t, x, W1, W2, hidden_size, learning_rate):
    for i in range(hidden_size):
        b2 = -(t-o2)*o2*(1-o2)
        dldwc = b2*o1[i]
        W2[0,i] = W2[0,i] - learning_rate * dldwc
        o1[i] = b2 * W2[0,i]
        for j in range(len(x)):
            dldwdc = sum(o1[i] * deriv_sigmoid(a1[i])*(1-deriv_sigmoid(a1[i]))*x[j])
            W1[i,j] = W1[i,j] - dldwdc * learning_rate
    return W1, W2

def sigmoid(x_array):
    return 1.0/(1.0 + np.exp(-x_array))

def deriv_sigmoid(x_array):
    return np.exp(-x_array)/((1 + np.exp(-x_array))**2)

if len(sys.argv) != 4 or not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]) or not os.path.isfile(sys.argv[3]):
    print "no file"
else:
    # music_train.csv music_train_keys.txt music_dev.csv
    with open(sys.argv[1], 'r') as train:
        trainData = train.read().splitlines()
        train_np = loadtraindata(trainData)
    with open(sys.argv[2], 'r') as test_f:
        keyData = test_f.read().splitlines()
        key_np = loadkeydata(keyData)
    with open(sys.argv[3], 'r') as dev_f:
        devData = dev_f.read().splitlines()
        dev_np = loadtraindata(devData)
    if not trainData or not keyData:
        print "empty file"
    else:
        hidden_size = 8
        learning_rate = 0.6
        np.random.seed(500)
        W1 = np.random.uniform(-2.2, 2.2, [hidden_size, 6])
        W2 = np.random.uniform(-2.2, 2.2, [1, hidden_size+1])
        # need to iter again and again!!!!
        for iter in range(120):
            i = 0
            loss = 0
            for line in train_np:
                a1, o1, a2, o2 = forward(line, W1, W2, hidden_size)
                W1, W2 = backpropagation(a1, o1, a2, o2, key_np[i], line, W1, W2, hidden_size, learning_rate)
                loss += cal_loss(o2, key_np[i])
                i += 1
            print loss
        print "TRAINING COMPLETED! NOW PREDICTING."
        for dev_line in dev_np:
            dev_a1, dev_o1, dev_a2, dev_o2 = forward(dev_line, W1, W2, hidden_size)
            print dev_o2*100


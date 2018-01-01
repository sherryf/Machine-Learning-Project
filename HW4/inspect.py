import sys
import os
import math

def inspect(contents):
    length = len(contents[0].split(","))
    totalNum = float(len(contents) - 1)
    postive = contents[1].split(",")[length-1]
    numPos = 0
    for index in contents[1:]:
        data = index.split(",")
        if data[length-1] == postive:
            numPos+=1.0
    numNeg = totalNum - numPos
    if numNeg == 0 or numPos == 0:
        entropy = 0
    else:
        entropy = -1.0 * numPos/totalNum*math.log(numPos/totalNum, 2)-numNeg/totalNum*math.log(numNeg/totalNum, 2)
    max = 0
    if numPos > numNeg:
        max = numPos
    else:
        max = numNeg
    error = 1 - max/totalNum
    print_entropy = "entropy: " + str(entropy)
    print_error = "error: " + str(error)
    return print_entropy, print_error


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.readlines()
    if not contents:
        print "empty file"
    else:
        entropy, error = inspect(contents)
        print entropy
        print error

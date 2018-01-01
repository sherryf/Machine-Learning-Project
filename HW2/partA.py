import sys
import os
import math
from decimal import *
# 1
inputSpace = 2**9
print inputSpace
# 2
conceptSpace = int(math.ceil(math.log(Decimal(2**inputSpace), 10)))
print conceptSpace
# 3
firstHypo = 3**9 + 1
print firstHypo
# 4
secondHypo = 3**10 + 1
print secondHypo
# 5
thirdHypo = 3**8 * 4 + 1
print thirdHypo


def FindS(contents):
    with open('partA6.txt', 'w') as outfile:
        # initial hypo
        hypo = ["null"] * 9
        count = 1
        for line in contents:
            sample = line.split('\t')
            # get rid of '/r/n'
            if sample[9].split(' ')[1][:4] == "high":
                for i in range(9):
                    if hypo[i] == "null" :
                        hypo[i] = sample[i].split(' ')[1]
                    elif hypo[i] != sample[i].split(' ')[1]:
                        hypo[i] = "?"
                    else:
                        hypo[i] = hypo[i]
            if count % 30 == 0:
                outfile.write("\t".join(hypo))
                outfile.write("\n")
            count += 1
        return hypo


def classify(lines, hypo):
    for line in lines:
        flag = 0
        data = line.split('\t')
        for i in range(9):
            if hypo[i] != "?" and data[i].split(" ")[1] != hypo[i]:
                flag = 1
                break
        if flag == 1:
            print "low"
        else:
            print "high"


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) or not os.path.isfile("9Cat-Dev.labeled") \
        or not os.path.isfile("9Cat-Train.labeled"):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.readlines()
    if not contents:
        print "empty file"
    else:
        with open("9Cat-Train.labeled", "r") as input:
            data = input.readlines()
            hypo = FindS(data)
            with open("9Cat-Dev.labeled", "r") as dev:
                devData = dev.readlines()
                sum = 0
                diff = 0
                for index in devData:
                    sum += 1
                    training = index.split('\t')
                    for i in range(9):
                        if hypo[i] != "?" and hypo[i] == training[i].split(" ")[1] \
                                and training[9].split(' ')[1][:3] == "low":
                            diff += 1
                        if hypo[i] != "?" and hypo[i] != training[i].split(" ")[1] \
                                and training[9].split(' ')[1][:3] != "low":
                            diff += 1
                            break
                print diff*1.0/sum
        classify(contents, hypo)
import sys
import os
# 1
inputSpace = 2**4
print inputSpace
# 2
conceptSpace = 2**inputSpace
print conceptSpace


# 3
def listThenElimit(train):
    matrix = []
    for num in range(0, conceptSpace):
        matrix.append(num)

    for data in train:
        count = 0
        sample = data.split('\t')
        # find the value of all the sample
        if sample[0].split(" ")[1] == "Male":
            count += 2**3
        if sample[1].split(" ")[1] == "Young":
            count += 2**2
        if sample[2].split(" ")[1] == "Yes":
            count += 2**1
        if sample[3].split(" ")[1] == "Yes":
            count += 1
        if sample[4].split(" ")[1][:4] == "high":
            check = 1
        else:
            check = 0
        # filter all the right choice
        tmp =[]
        for i in matrix:
            for tag in range(0, inputSpace):
                if tag == count and check == i >> (15-tag) & 1:
                    tmp.append(i)
        matrix = tmp
    return matrix


def testVote(hypo, contents):
    for testData in contents:
        count = 0
        sample = testData.split("\t")
        if sample[0].split(" ")[1] == "Male":
            count += 2**3
        if sample[1].split(" ")[1] == "Young":
            count += 2**2
        if sample[2].split(" ")[1] == "Yes":
            count += 2**1
        if sample[3].split(" ")[1] == "Yes":
            count += 1
        if sample[4].split(" ")[1][:4] == "high":
            check = 1
        else:
            check = 0
        vote = 0
        for h in hypo:
            if check == h >> (15-count) & 1:
                vote += 1
        # #high #low
        if check == 1:
            print str(vote) + " " + str(len(hypo) - vote)
        else:
            print str(len(hypo) - vote) + " " + str(vote)


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) or not os.path.isfile("4Cat-Train.labeled"):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.readlines()
    if not contents:
        print "empty file"
    else:
        with open("4Cat-Train.labeled", "r") as infile:
            train = infile.readlines()
            hypo = listThenElimit(train)
            print len(hypo)
            testVote(hypo, contents)

import sys
import os
if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print "no file"
else:
    with open(sys.argv[1], 'r') as f:
        contents = f.readlines()
    if not contents:
        print "empty file"
    else:
        contents.reverse()
        for index in contents:
            print index,
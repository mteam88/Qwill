from QHelper import *
import time
blanklists = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], \
    [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
lists = [[0,1,1,0,1,0,1,1,1,0,1,1], [1,1,1,1,1,0,0,0,0,0,0,0], \
         [1,0,1,0,1,0,1,0,0,0,0,0], [1,0,1,0,0,1,1,1,0,0,0,0]]
true_Dice = [False, True, True, True]
tags = ['Matthew']

print(aiturn(lists, true_Dice, 0, tags, 1))

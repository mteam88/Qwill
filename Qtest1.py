from QHelper import *
import time
blanklists = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], \
    [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
lists = [[0,1,1,0,1,0,1,1,1,0,1,1], [1,1,1,1,1,0,0,0,0,0,0,0], \
         [1,0,1,0,1,0,1,0,0,0,0,0], [1,0,1,0,0,1,1,1,0,0,0,0]]
mywrolls = wroll()
mycrolls = croll([True, True, True, True])
myrolls = mywrolls + mycrolls
print(myrolls)
print(possibleplays(blanklists, [True, True, True, True], myrolls))
#print(handlegameover(lists, -5, 2))
#print(rollindex([1, 3, 4, 3, 5, 1]))

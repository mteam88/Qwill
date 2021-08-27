from QHelper import *
from Qepicenter import *
InvalidAIUserInput = Exception
#         0,1,2,3,4,5,6,7,8,9,10,11
lists = [[0,0,0,0,0,0,0,0,0,0,0 ,0], [0,0,0,0,0,0,0,0,0,0,0,0], \
    [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
rnd = 1
tags = inithumans()
hmncnt = len(tags)
true_Dice = [True, True, True, True]
pnlty = 0

for gameloopiter in range(50):
    pnlty, lists, true_Dice = aiturn(lists, true_Dice, pnlty, tags, hmncnt)
#    input()

    print('\nHuman player wilds:  ')
    for tagnum, realtag in enumerate(tags):
        print('\n' + str(tagnum + 1) + ',  ', end=' ')

        try:
            wildinpt = int(input(realtag + ': '))
        except ValueError as _:
            print('Please input a valid integer.')
            try:
                wildinpt = int(input(realtag + ': '))
            except ValueError as _:
                raise InvalidAIUserInput('FATAL LOGIC ERROR! Program exiting')
# Previous lines are just user input cleaning... Kind of excessive...
        tookhmnw, lists = takehumanwild(lists, wildinpt, true_Dice)
        if tookhmnw:
            print('I took the wild. ')
            if tookhmnw[1] == 10:
                lists == addX(lists, tookhmnw[0], 11)
                true_Dice[tookhmnw[0]] = False
                print('I blocked a color.')
                print(displists(lists))
                if isgameover(true_Dice):
                    handlegameover(lists, pnlty, humans, tags)
        else:
            print('I did not take the wild. ')
# Is game over?
        if input('Is the game over?  (Type "Yes" to affirm):  ') == 'Yes':
            handlegameover(lists, pnlty, hmncnt, tags)



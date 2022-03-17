ProgramEnd = Exception
Penalty = Exception
LOGFILE = 'Qlog.txt'

def tutorial():
    """
    Runs the player through a quick tutorial on how to use the bot.
    """
    if input("Would you like a tutorial on how to use Qaike? ('yes' to accept): ") == "yes":
        print("\n\nQaike Tutorial")
        print("If you are reading this, you have already initialized the human players in the game.")
        print("Make sure you have entered each player seperately.")
        print("\nWhen you start the Qaike AI, have all human players get ready their Qwixx scoresheets")
        print("The bot/AI always goes first, it will tell you what wild is available")
        print("The bot will also show you its rolls in the format [firstwild, secondwild, red, yellow, green, blue]")
        print("\nAll human players should write down their wilds, and then type their wilds")
        print("\nTell Qaike when your game is done, and it will show you its score and its scorecard")
        print("\nIf you have any questions, open an issue on Github (https://github.com/Matthews-Makes/Qaike/issues/new/choose)")

def croll(true_Dice):
    """
    Returns color rolls in list to be unpacked.
    """
    crolls = []
    for i in range(4):
        if true_Dice[i]:
            crolls.append(int(rand.randint(1, 6)))
        else:
            crolls.append(False)
    return crolls


def wroll():
    """
    Returns the two wilds in a list to be unpacked.
    For example, wroll() might return "[1,3]"
    """
    rolls = []
    for i in range(2):
        rolls.append(int(rand.randint(1, 6)))
    return rolls


def Xify(rows):
    """
    Helper for displists, returns rows with 1s replaced with Xs
    Rows is also combined into one string seperated by spaces
    """
    Xedrows = []
    for row in rows:
        Xedrow = []
        for i, e in enumerate(row):
            if e == 1:
                Xedrow.append('X')
            else:
                Xedrow.append('-')
        Xedrows.append(' '.join(Xedrow))
    return Xedrows


def displists(lists):
    """
    recieves lists (a list containing 4 lists each of which have 12 elements)
    returns a formatted (newlined) string of the lists printed nicely.

    For example: displists([[1,0,1,0,0,1,1,1,0,0,1,1], ...])
    might return: "Red: [X - X - - X X X - - X X]\nYellow: ...
    """
    lists = Xify(lists)
    formatted = '\nRed:    {}\nYellow: {}\nGreen:  {}\nBlue:   {}'\
        .format(lists[0], lists[1], lists[2], lists[3])
    return formatted


def addX(lists, color, index, muffled=False):
    """
    Returns lists with an added "1" at colors index
    lists: a list with 4 lists, each of which have 12 elements (index 0-11)
    color: an integer (0, 1, 2, 3) representing which list to modify
    index: index of to add "1" (0,1,2...,10,11)
    """
    try:
        lists[color][index] = 1
    except IndexError as e:
        print('ERROR')
        if not muffled:
            raise e
    return lists


def scorelists(lists, penalty):
    """
    Returns an integer score based on QWIXX scoring rules that represents
        lists minus penalty.
    lists: a list with 4 lists, each of which have 12 elements (index 0-11)
    penalty: a positive integer that represents the amount of points to be
        subtracted from the score because of "penalties" from QWIXX
    """
    scrlst = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
    scr = 0-penalty
    for i in range(4):
        scr += scrlst[lists[i].count(1)]
    return scr


def wildsinptgen(tag):
    """
    Yields the input of a player. the player will be prompted with (tag(1-12))
    "tag" should be a string or integer representing an individual player in
        the QWIXX game
    """
    tag = str(tag)
    yield input(tag + '(1-12): ')


def inithumans():
    """
    inithumans returns a list of tags for each human play in the game.
    """
    tags = []
    for i in range(5):
        tags.append(input('\nPlayer name/tag (blank entry aborts): '))
        if not tags[i]:
            tags.pop()
            break
    print('Selected player names/tags:', tags, sep='\n')
    return tags


def findlastX(row):
    """
    findlastX returns the last (rightmost) occurence of the number '1'
    """

    for i, e in enumerate(row[::-1]):
        if e == 1:
            break
    if 1 not in row:
        return -1
    return len(row)-i-1

def findlastXs(lists):
    """
    findlastXs returns the last (rightmost) occurence of the number '1' in all rows in lists
    """
    final=[]
    for row in lists:
        final.append(findlastX(row))
    return final

def numindex(color, num):
    """
    Similar to rollindex, returns index of "num" in the list "color"
    color: 1-red, 2-yellow, 3-green, 4-blue
    """
    if color >= 2:
        return [color, 12 - num]
    else:
        return [color, num - 2]


def rollindex(rolls):
    """
    Returns the list of possible places to play an X based on rolls.
    the list is made up of the play indices with the same format output as
        possibleplays!
    """
    rindices = []
    for rollnum, roll in enumerate(rolls[2:]):
        if roll is not False:
            realrolls = [rolls[0] + roll, rolls[1] + roll]
            if rollnum >= 2:
                for i, _ in enumerate(realrolls):
                    toapp = (rollnum, 12 - realrolls[i])
                    rindices.append(toapp)
            else:
                for i, _ in enumerate(realrolls):
                    rindices.append((rollnum, realrolls[i]-2))
    return rindices


def mycrossref(la, lb):
    """
    Returns a list of the similarities between la and lb (lists)
    """
    myfinal = []
    for a in la:
        if a in lb:
            myfinal.append(a)
    for b in lb:
        if b in la:
            myfinal.append(b)
    return list(set(myfinal))


def emptyspots(lists, true_Dice):
    """
    Returns a list of all of the empty spots that are available.
    This includes all empty spots to the right of the rightmost X.
    These do not represent all possible plays because they include lock areas.
    (12, 2, and lock symbols may not be possible). 
    Also does not account for rolls!
    """
    pempty = []
    for i, color in enumerate(lists):
        if true_Dice[i] is True:
            last = findlastX(color)
            for ind, _ in enumerate(color[last+1:11]):
                pempty.append((i, ind+last+1))
    return pempty


def possibleplays(lists, true_Dice, rolls):
    """
    Returns a list of all of the possible plays that the QWIXX scoresheet can
        handle. The result is a list of tuples in the form:
        [(color, elementindex),(color, elementindex)]
    Args:
    lists: a list with 4 lists, each of which have 12 elements (index 0-11)
    true_Dice: a list containing 4 bool values
    rolls: a 6 elem list containing wilds then color rolls
    """
    pempty = emptyspots(lists, true_Dice)
    for i, color in enumerate(lists):
        if true_Dice[i] is True:
            last = findlastX(color)
            for ind, _ in enumerate(color[last+1:11]):
                pempty.append((i, ind+last+1))
    prolls = rollindex(rolls)
    allpos = mycrossref(pempty, prolls)
    finalpos = []
    for pos in allpos:
        if pos[1] == 10:
            if lists[pos[0]].count(1) >= 5:
                finalpos.append(pos)
        else:
            finalpos.append(pos)
    return finalpos


def isblocked(true_Dice):
    """
    Ask users if any new colors are blocked.
    If so, mark colors as blocked (False) in true_dice.
    Returns new true_dice.
    """
    # TODO: Add functionality so this does not happen if no humans are playing.
    blockinpt = input('Are any new colors blocked?   ')
    while blockinpt:
        if blockinpt:
            if blockinpt.lower().startswith('r'):
                true_Dice[0] = False
            elif blockinpt.lower().startswith('y'):
                true_Dice[1] = False
            elif blockinpt.lower().startswith('g'):
                true_Dice[2] = False
            elif blockinpt.lower().startswith('b'):
                true_Dice[3] = False
            else:
                break
            blockinpt = input('Are any new colors blocked?    ')
    return true_Dice


def isgameover(true_Dice):
    """
    If the game is over because 2 colors are locked, returns True
    Otherwise, returns False
    """

    if true_Dice.count(False) >= 2:
        return True
    else:
        return False


def handlegameover(lists, penalty, plyrs, tags):
    """
    gets various game data
    logs those values to LOGFILE (global variable)
    announces to player that game is over
    AND, displays score and final scoresheet
    """
    print('\tGAME OVER!!!\n\n')
    print('I scored a ' + str(scorelists(lists, penalty)), end='\n\n')
    print('My final scoresheet is ', displists(lists), sep='\n')
    with open(LOGFILE, 'a') as logf:
        print('\nGame score is ' + str(scorelists(lists, penalty)), file=logf)
        print('against ' + str(plyrs) + ' human players', file=logf)
        print(displists(lists) + '\n', file=logf)
        print('Penalty: ' + str(penalty), file=logf)
    print('You can safely close the program now')
    input('Enter to quit')
    quit()


def aiturn(lists, true_Dice, pnlty, tags, humans):
    """
    Rolls wilds with wroll
    Rolls colors with croll
    Displays the wilds rolled and the total
    Checks if should use wild with takewild from Qepicenter
    Says if blocked a color
    Asks if new colors are blocked
    Displays wilds and color rolls
    Calls "possibleplays" to get all possible plays
    Gets best play by calling bestplay from Qepicenter
    Marks that play on lists (with addX)
    Determines if that play blocks a color, if it does, mark extra X
    Displays a blurb if blocked a color
    Displays lists by printing the return value of "displists"---
    """
# TODO: Complete helper function and real docstr
    wilds = wroll()
    clrs = croll(true_Dice)
    print('\n\t\t\tMy Turn\t\t\t\n')
    print('I rolled a ' + str(wilds[0]) + ' and a ' + str(wilds[1]) +
          ', for a total of ' + str(sum(wilds)) + '.')
    took, lists = takewild(lists, wilds, clrs, true_Dice)
    if took:
        if took[1] == 10:
            print('I blocked a color!')
            lists == addX(lists, took[0], 11)
            true_Dice[took[0]] = False
        print('I took the wild', displists(lists), sep='\n')
    if sum(wilds) == 12 or sum(wilds) == 2:
        true_Dice = isblocked(true_Dice)
        if isgameover(true_Dice):
            handlegameover(lists, pnlty, humans, tags)
            return None
    rolls = wilds + clrs
    print('My rolls are: ', rolls)  # TODO: improve this
    pos = possibleplays(lists, true_Dice, rolls)
#    print(pos, '     DEBUG')  # DEBUGGER
    # Only "try"ing bestplay because bestplay will raise Penalty exception
    # if that is the best choice.
    try:
        bestply = bestplay(lists, pos, richter=2, lastxs=findlastXs)
        # Richter (difficulty) can be added here.
#        print(bestply, '   DEBUG')  # DEBUGGER
        lists = addX(lists, bestply[0], bestply[1])
        if bestply[1] == 10:
            lists == addX(lists, bestply[0], 11)
            true_Dice[bestply[0]] = False
            print('I blocked a color on my turn.')
            if isgameover(true_Dice):
                handlegameover(lists, pnlty, humans, tags)
                return None
    except:  # Means bestplay decided to take a Penalty
        pnlty += 5
        print('I took a penalty... Man... That makes ' + str(int(pnlty / 5)))
        if pnlty >= 20:
            handlegameover(lists, pnlty, humans, tags)
            return None

    print(displists(lists))
    return pnlty, lists, true_Dice

import random as rand
from Qepicenter import *
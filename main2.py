import random, sys

class Player:
    def __init__(self, tag):
        self.tag = tag
    def getWild(self):
        return input(tag+", please enter your wild")
    @classmethod
    def initPlayers(cls):
        '''
        Initialize humans. Returns list of Player objects.
        '''
        tags = []
        while True:
            tags.append(Player(input('\nPlayer name/tag (blank entry aborts): ')))
            if not tags[-1].tag:
                tags.pop()
                break
        print('Selected player names/tags:', [i.tag for i in tags], sep='\n')
        return tags

class Card(list):
    def __init__(self, initlist=[[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]], true_Dice=[True, True, True, True], penalty=0):
        super().__init__(initlist)
        SCORELIST = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
        self.true_Dice = true_Dice
        self.penalty = penalty

    def addX(self, position, muffled=False):
        """
        Adds "1" to position[0]'s position[1]
        self: a Card object
        position[0]: an integer (0, 1, 2, 3) representing which list to modify
        position[1]: index of to add "1" (0,1,2...,10,11)
        """
        try:
            self[position[0]][position[1]] = 1
        except IndexError as e:
            print('ERROR')
            if not muffled:
                raise e

    def scoreCard(self):
        """
        Returns an integer score based on QWIXX scoring rules that represents
        lists minus penalty.
        self & self.penalty are used
        """
        for i in range(4):
            scr += SCORELIST[lists[i].count(1)]
        scr = 0-self.penalty
        return scr

class XPlay:
    def __init__(self, position, isWild):
        self.position = position
        self.isWild = isWild
    def isPossible(self, card):
        '''
        Takes Card object, returns boolean. True if the play is possible.
        '''
        pass
    def getScoring(self, card):
        '''
        Returns various scoring data.
        Returns: (skipped, score incr) tuple
        '''
        skipped = self.position[1]- findlastXs()[self.position[0]]
        scoreincr = 0
        return (skipped,0)

    def disp(self):
        return __dict__
   
    @classmethod
    def findlastXs():
        """
        findlastXs returns the last (rightmost) occurence of the number '1' in all rows in lists
        """
        final=[]
        for row in lists:
            for i, e in enumerate(row[::-1]):
                if e == 1:
                    break
            if 1 not in row:
                result = -1
            else:
                result = len(row)-i-1
        final.append(result)
        return final


class Evaluater: #Super Class
    def __init__(self, xPlays):
        self.xPlays = xPlays
    def disp(self):
        for xPlay in self.xPlays:
            return xPlay.disp()
    def evalAll(card):
        '''
        To be overidden by child classes.
        '''
        pass

class LeastSkipped(Evaluater):
    def __init__(self, xPlays):
        super().__init__(xPlays)

    def evalAll(self, card):
        scoringlist = []
        for xPlay in self.xPlays: # Looping for ever play added.
            scoringlist.append([xPlay, xPlay.getScoring(card)]) # Initialize list
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.
        return scoringlist

leastSkippedEval = LeastSkipped([XPlay([0, 1], True), XPlay([0, 2], True), XPlay([1, 1], True), XPlay([2, 1], True), XPlay([0, 0], True), XPlay([3, 3], True)])
print(leastSkippedEval.evalAll(Card()))
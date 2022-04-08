from copy import deepcopy, copy
import logging

class Card(list):
    def __init__(self, initlist=None, true_Dice=None, penalty=0, roundnum=1):
        if initlist == None: # All of this is for mutable function parameters
            initlist = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
        if true_Dice == None:
            true_Dice = [False, False, False, False]
        super().__init__(initlist)
        self.SCORELIST = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78]
        self.true_Dice = true_Dice
        self.penalty = penalty
        self.roundnum = roundnum

    def addX(self, xplay, muffled=False):
        """
        Adds "1" to position[0]'s position[1]
        self: a Card object
        position[0]: an integer (0, 1, 2, 3) representing which list to modify
        position[1]: index of to add "1" (0,1,2...,10,11)
        """
        #print("xplay: ", xplay)
        try:
            self[xplay.position[0]][xplay.position[1]] = 1 #TODO: debug TypeError: 'XPlay' object is not subscriptable
        except IndexError as e:
            print('ERROR')
            if not muffled:
                raise e
        return self

    def scoreCard(self):
        """
        Returns an integer score based on QWIXX scoring rules that represents
        lists minus penalty.
        self & self.penalty are used
        """
        scr = 0-self.penalty
        for i in range(4):
            scr += self.SCORELIST[self[i].count(1)]
        return scr
    
    def getLists(self): #DELETE ME
        return list(self)

class XPlay:
    def __init__(self, position, isWild, plyrWild=False):
        self.position = position
        self.isWild = isWild
        self.plyrWild = plyrWild
    
    def disp(self):
        return (self.position, self.isWild, self.plyrWild).__repr__()

    def isPossible(self, card):
        '''
        Accepts Card object, returns boolean. True if the play is possible according to Qwixx rules
        '''
        pempty = [] # Returns all possible plays, but not last (lock) spot. This means this must be added later on.
        for i, color in enumerate(card):
            if card.true_Dice[i] is False:
                last = self.findlastXs(card)[i]
                for ind, _ in enumerate(color[last+1:11]):
                    pempty.append([i, ind+last+1])
        #print("pempty: ", pempty)
        pos = self.position
        #print("pos: ", pos)
        if pos in pempty:
            if pos[1] == 10:
                if card[pos[0]].count(1) >= 5:
                    return True
            else:
                return True
        else:
            return False

    def getScoring(self, card):
        '''
        Only works for possible plays.
        Returns various scoring data.
        Returns: (skipped, score incr) tuple
        '''
        #print(self.findlastXs(card))
        #skipped section
        #print("lastx of row: ", self.findlastXs(card)[self.position[0]])
        #print("position in question: ", self.position[1])
        skipped = self.position[1]- self.findlastXs(card)[self.position[0]] - 1
        #print("skipped: ", skipped)
        #scoreincr section
        scoreincr = Card(initlist=deepcopy(card), true_Dice=card.true_Dice, penalty=card.penalty).addX(self).scoreCard()-card.scoreCard()
        return (skipped,scoreincr)

   
    @classmethod
    def findlastXs(cls, card):
        """
        findlastXs returns the last (rightmost) occurence of the number '1' in all rows in lists
        """
        final=[]
        for row in card:
            for i, e in enumerate(row[::-1]):
                if e == 1:
                    break
            if 1 not in row:
                result = -1
                final.append(result)
            else:
                result = len(row)-i-1
                final.append(result)
        return final

print(XPlay([0,0], False).isPossible(Card()))
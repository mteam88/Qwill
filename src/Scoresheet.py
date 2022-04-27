from copy import deepcopy, copy
import logging

class Card(list):
    def __init__(self, initlist=None, true_Dice=None, penalty=0, roundnum=0):
        if initlist is None: # All of this is for mutable function parameters
            initlist = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
        if true_Dice is None:
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
        self[xplay.position[0]][xplay.position[1]] = 1
        if xplay.position[1] == 10:
            self._addlockingX(xplay)
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

    def _addlockingX(self, play):
        self.true_Dice[play.position[0]] = True
        self.addX(XPlay([play.position[0], 11], False))

    def __str__(self):
        """
        returns a formatted (newlined) string of the lists printed nicely.

        For example: [[1,0,1,0,0,1,1,1,0,0,1,1], ...]
        might return: "Red: [X - X - - X X X - - X X]\nYellow: ...
        """
        Xedrows = []
        for row in self:
            Xedrow = []
            for e in row:
                if e == 1:
                    Xedrow.append('X')
                else:
                    Xedrow.append('-')
            Xedrows.append(' '.join(Xedrow))
        return '\nRed:    {}\nYellow: {}\nGreen:  {}\nBlue:   {}'.format(Xedrows[0], Xedrows[1], Xedrows[2], Xedrows[3])


class XPlay:
    def __init__(self, position, isWild, plyrWild=False):
        self.position = position
        self.isWild = isWild
        self.plyrWild = plyrWild
    
    def __repr__(self):
        return (f"XPlay: {self.position, self.isWild, self.plyrWild}")

    def isPossible(self, card):
        '''
        Accepts Card object, returns boolean. True if the play is possible according to Qwixx rules
        '''
        pempty = [] # Returns all possible plays, but not last (lock) spot. This means this must be added later on.
        for i, color in enumerate(card):
            if card.true_Dice[i] is False:
                last = self.findlastXs(card)[i]
                pempty.extend([i, ind+last+1] for ind, _ in enumerate(color[last+1:11]))
        #print("pempty: ", pempty)
        pos = self.position
        if pos not in pempty:
            return False
        if pos[1] != 10:
            return True
        if card[pos[0]].count(1) >= 5:
            return True

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
            result = -1 if 1 not in row else len(row)-i-1
            final.append(result)
        return final

class PlaysList(list):
    def __init__(self, plist, iswild=False):
        self.iswild = iswild
        super().__init__(plist)
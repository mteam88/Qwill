import logging
from Scoresheet import XPlay, XMove
from typing import List

THRESHOLD = 2

class Penalty(Exception):
    pass

class Evaluater: #Super Class
    def __init__(self, xPlays, iswild=False):
        self.xPlays = xPlays
        self.iswild = iswild

    def disp(self):
        for xPlay in self.xPlays:
            return xPlay.disp()

    def evalAll(self, card):
        '''
        To be overidden by child classes.
        '''
        raise NotImplementedError

class LeastSkipped(Evaluater):
    def __init__(self, *args, threshold=THRESHOLD, **kwargs):
        self.threshold = threshold
        super().__init__(*args, **kwargs)

    def evalAll(self, card) -> List[XMove]:
        self.card = card
        # Check if any are blocking plays and always take one if there is.
        if (lockingmove := self._checkalllocking(self.xPlays)): # Hooray walrus operator!
            return lockingmove.xplays

        scoringlist = ScoringList(card, self.xPlays)

        scoringlist.score()

        print(f"scoringlist: {scoringlist}")
        
        scoringlist.sort_by(self._sort_added_skipped) # Sort by total number of spaces skipped.

        if scoringlist: 
            bestXPlayinfo = scoringlist[0] # Set bestxplayinfo

        elif self.iswild == False:
            raise Penalty
        else:
            return []

        if bestXPlayinfo.plyrWild == True: #This means that we might not have to take the XPlay
            result = bestXPlayinfo.xplays if bestXPlayinfo[1][0][1] <= self.threshold else [] # Not sure about this
            print(f"result: {result}")
            return result
        return bestXPlayinfo.xplays # TODO extend so takes wild then color play on turn if possible


    # Internal Helper Methods

    def _sort_added_skipped(self, xmove):
        result = sum(xmove.scoring[i][0] for i in range(len(xmove.xplays)))
        return (result, len(xmove.xplays))

    @staticmethod
    def _checklocking(move) -> bool:
        "Returns True if locking move."
        return True in [play.position[1] == 10 for play in move.xplays]
    
    @classmethod # So can call _checklocking here
    def _checkalllocking(cls, playslist):
        "Returns a locking move if there is one in playslist."
        for move in playslist:
            if cls._checklocking(move):
                return move

class ScoringList(list):
    def __init__(self, card, xplays):
        super().__init__(xplays)
        self.card = card
    
    def score(self):
        self = [ScoredXMove(xmove, self.card) for xmove in self]

    def sort_by(self, sortkey):
        self.sort(key=sortkey)

class ScoredXMove():
    def __init__(self, xmove, card):
        self = xmove
        self.scoring = xmove.getScoring(card)
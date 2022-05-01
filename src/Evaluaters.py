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

    @staticmethod
    def _len_xmove(xmove):
        return -len(xmove.xplays)

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

        scoringlist.multi_sort_by([self._sort_added_skipped_key, self._len_xmove]) # Sort by total number of spaces skipped.

        print(f"scoringlist: {scoringlist}")

        if scoringlist: 
            bestXMove = scoringlist[0] # Set bestxplayinfo

        elif self.iswild == False:
            raise Penalty
        else:
            return []

        if bestXMove.plyrWild == True: #This means that we might not have to take the XPlay
            return bestXMove.xplays if bestXMove.scoring[0][1] <= self.threshold else []
        return bestXMove.xplays # TODO extend so takes wild then color play on turn if possible


    # Internal Helper Methods

    def _sort_added_skipped_key(self, xmove):
        return sum(xmove.scoring[i][0] for i in range(len(xmove.xplays)))

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
    def __init__(self, card, xmoves):
        super().__init__([ScoredXMove(xmove, card) for xmove in xmoves])
        self.card = card

    def multi_sort_by(self, sortkeys):
        "Sorts by list of keys, sortkeys should have tiebreaker last."
        for sortkey in sortkeys[::-1]:
            self.sort(key=sortkey)

class ScoredXMove():
    def __init__(self, xmove, card):
        self.xmove = xmove
        self.scoring = xmove.getScoring(card)

    def __getattr__(self, name):
        return getattr(self.xmove, name)
    
    def __repr__(self):
        return (f"{self.__class__.__name__}: {self.__dict__}\n")
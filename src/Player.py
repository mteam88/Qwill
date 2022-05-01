import itertools
from Evaluaters import *
from random import randint
from Scoresheet import XPlay, Card, PlaysList, XMove
from warnings import warn
from loggingdecorator import logiof
import logging

class InputError(Exception):
    pass

class Player:
    def __init__(self, tag:str, card: Card, true_Dice:list=None):
        self.tag = tag
        self.card = card
        self.card.true_Dice = true_Dice
    def getWild(self):
        '''Get wild from player. Returns number that was rolled, not XPlay or index. Should be overwritten.'''
        pass
    def turn(self):
        '''Take turn. Returns [dict object with {bool True if took X (False on penalty), any/all XPlays used list(empty if none or human)}
            , wild (as a number)]'''
        pass
    def wild(self):
        '''Decide if should take wild based on card. Returns Returns [dict object with {bool True if took X (False on penalty)
            , any/all XPlays used list(empty if none or human)}
            , wild (as a number)]'''
    @classmethod
    def initPlayers(cls):
        '''
        Initialize all players. Returns PlayerList object of Human and AI objects (with Player superclassed).
        '''
        players = []
        while True:
            tag = input('\nPlayer name/tag (blank entry aborts) (prefix with "cpu_" to create a cpu): ')
            if tag == '':
                break
            if tag.split('_')[0] == 'cpu':
                players.append(AI(tag, Card()))
            else:
                players.append(Human(tag, Card()))
        print('Selected player names/tags:', [player.tag for player in players], sep='\n')
        return PlayerList(players)
    
    def __repr__(self):
        return f"{self.__class__.__name__} OBJECT: {self.tag}"

class Human(Player):
    def __init__(self, tag, card):
        super().__init__(tag, card)
        #self.tag = tag
    def turn(self, card=None):
        if card is None:
            card = self.card
        return self._getwild()

    def wild(self, wild, card=None):
        return Took({"didtake": False, "tookwhat": []})
    
    def _getwild(self):
        while True:
            response = input(f'{self.tag}, please enter your wild (2-12): ')
            try:
                response = int(response)
                if response in range(2,13):
                    return [Took({"didtake":False, "tookwhat": []}), response]
                else:
                    raise InputError
            except (InputError,ValueError):
                print("Please input a valid integer wild between 2 and 12")


class AI(Player):
    '''
    Class that interprets card state and decides what to do based on Evaluaters and Card
    '''
    def __init__(self, tag, card):
        super().__init__(tag, card)
        #self.tag = tag

    # Class Interface Methods

    @logiof
    def turn(self, card: Card =None):
        '''
        Returns [Took object, wild]
        '''
        if card is None: # Essentially an optional parameter
            card = self.card
        playslist, rolls = self._rolldiceandgetXPlays(card.true_Dice)
        print(f"rolls: {rolls}")
        playslist = self._getXmovesfromXplays(playslist)
        try:
            plays = self._eval(playslist, card, iswild=False)
            #logging.info(f"Took from XPlays input: {plays}")
            took = self._gettookfromXPlays(plays, card)
            return [took, sum(rolls[:2])] # latter is wild returned from _getXPlays() function 
        except Penalty: # Took penalty
            self.card.penalty += 1
            took = Took({'didtake': False, 'tookwhat': []})
            took.ispenalty = True
            return [took, sum(rolls[:2])]
    
    @logiof
    def wild(self, wild, card=None):
        if card is None:
            card = self.card
        playslist = self._getXmovesfromXplays(self._getXPlaysfromwild(wild))
        plays = self._eval(playslist, card, iswild=True)
        #print("plays: ", plays)
        if plays == []:
            took = Took({"didtake": False, "tookwhat": []})
            return took
        #print(plays[0], plays[0].position)
        card.addX(plays[0])  # Note the [0] bit, _eval can only return one best for human wild
        if plays[0].position[1] == 10:
            card.addX(XPlay([plays[0].position[0], 11], True))
        took = self._gettookfromXPlays(plays, card)
        return took

    # Internal Helper Methods

    @logiof
    def _eval(self, playslist, card, iswild=False):
        #logging.info(f"Old Playslist: {playslist}")
        playslist = self._getpossiblefromplays(playslist, card)
        #logging.info(f"New Playlist: {playslist}")
        lse = LeastSkipped(playslist, iswild=iswild)
        #logging.info(f"_evalall out: {lse.evalAll(card)}")
        return lse.evalAll(card)

    def _getXPlaysfromrolls(self, plays, j, realrolls, i):
        return plays.extend(XPlay([j, self._getindexfromroll(j, realrolls[i])], False) for i, _ in enumerate(realrolls))

    def _getindexfromroll(self, color: int, rollnum: int):
        return 12 - rollnum if color >= 2 else rollnum - 2

    def _rolldiceandgetXPlays(self, true_Dice):
        '''
        returns list that contains XPlay objects for 'False' dice, but 'False' for 'True' dice also returns rolls
        Rolls dice internally
        '''
        rolls = [randint(1,6) for _ in range(2)]
        for i in true_Dice:
            if not i:
                rolls.append(randint(1,6))
            else:
                rolls.append(False)
        #print("rolls: ", rolls)
        #Now turn rolls into XPlay 
        plays = []
        for i, j in itertools.product(range(2), range(4)):
            clroll = rolls[j+2] #color value currently being processed
            if clroll is not False: #Is color actually rolled (may be locked)
                realrolls = [rolls[0] + clroll, rolls[1] + clroll] #Get actual numbers on scorecard
                self._getXPlaysfromrolls(plays, j, realrolls, i)
        plays += AI._getXPlaysfromwild(sum(rolls[:2]))
        return plays, rolls #return data

    @staticmethod
    def _getXmovesfromXplays(xplays):
        moves = list(itertools.permutations(xplays,2))
        moves.extend([[ele] for ele in xplays])
        # convert list of tuples to list of XMoves
        moves = [XMove(list(ele)) for ele in moves]
        return moves


    @classmethod
    def _getpossiblefromplays(cls, plays, card):
        '''
        Only returns possible XMoves in plays PlaysList). 
        '''
        plays = [move for move in plays if move.isPossible(card)]
        plays = [move for move in plays if len(move.xplays) == 1 or (move.xplays[0].isWild == True and move.xplays[1].isWild == False)]
        return PlaysList(plays)

    @classmethod
    def _getXPlaysfromwild(cls, wildint, plyrWild=False):
        plays = [XPlay([i,wildint-2], True, plyrWild=plyrWild) for i in range(2)] # red and yellow
        plays.extend(XPlay([i, 12 - wildint], True, plyrWild=plyrWild) for i in range(2, 4)) # for blue and green that the two wilds added could go in

        return plays

    @classmethod
    def _gettookfromXPlays(cls, plays, card):
        '''Helper function to get Took object from list of XPlays selected by _eval() method'''
        took = Took({"didtake": False, "tookwhat": []}) # Defaults to did take nothing
        if plays != []:
            took["didtake"] = True
            for play in plays:
                took["tookwhat"].append(play)
                if plays[0].position[1] == 10:
                    card.addX(XPlay([play.position[0], 11], False))
                card.addX(play)

        else:
            took["didtake"] = False
            took["tookwhat"] = []

        return took
        

class PlayerList(list):
    def __init__(self, players: list):
        self.true_Dice = [False, False, False, False]
        for player in players: 
            player.card.true_Dice = self.true_Dice
        super().__init__(players)
    
    def funcall(self, func, *argsf, active=None, **kwargsf):
        'Calls a function string on all players. Yields output of that function in tuple after active_player Player object'
        logging.info(f'func: {func}, *argsf: {argsf}, **kwargsf: {kwargsf}')
        for player in [x for x in self if x != active]:
            funcout = getattr(player.__class__, func)(player, *argsf, **kwargsf) # Run selected function. A bit clunky.
            #funcout = functocall(f"player.{func}(*argsf, **kwargsf)") # Run selected function. A bit clunky.
            logging.info(f'funcout to yield: {funcout}')
            yield player, (funcout)
    
    def getAIs(self):
        return [x for x in self if isinstance(x, AI)]


class Took(dict): # Super simple class (pun intended) to make naming and extending easier.
    '''
    dict should be {"didtake": (False for did not take, True for took X(s)), "tookwhat": list of XPlays that was taken}
    '''
    def __init__(self, pdict):
        try:
            pdict['didtake']
            pdict['tookwhat']
        except KeyError as e:
            raise ValueError("Required dict fields are 'didtake' and 'tookwhat'") from e
        self.ispenalty = False # Set to true if penalty was taken
        super().__init__(pdict)
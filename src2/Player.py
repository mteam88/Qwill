from Evaluaters import *
from random import randint
from Scoresheet import XPlay, Card, PlaysList
from warnings import warn
from loggingdecorator import logiof
import logging

class InputError(Exception):
    pass

class Player:
    def __init__(self, tag):
        self.tag = tag
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
            if tag != '':
                if tag.split('_')[0] == 'cpu':
                    players.append(AI(tag, Card()))
                else:
                    players.append(Human(tag, Card()))
            else: break
        print('Selected player names/tags:', [player.tag for player in players], sep='\n')
        return PlayerList(players)
    
    def __repr__(self):
        return f"{self.__class__} OBJECT: {self.tag}"

class Human(Player):
    def __init__(self, tag, card):
        super().__init__(tag)
        #self.tag = tag
        self.card = card
    def turn(self, card=None):
        if card == None:
            card = self.card
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
    def wild(self, wild, card=None):
        return Took({"didtake": False, "tookwhat": []})


class AI(Player):
    '''
    Class that interprets card state and decides what to do based on Evaluaters and Card
    '''
    def __init__(self, tag, card):
        super().__init__(tag)
        #self.tag = tag
        self.card = card

    # Class Interface Methods

    @logiof
    def turn(self, card=None):
        '''
        Returns [Took object, wild]
        '''
        if card == None: # Essentially an optional parameter
            card = self.card
        playslist, rolls = self._getXPlays(card.true_Dice)
        try:
            plays = self._eval(playslist, card, iswild=False)
            #logging.info(f"Took from XPlays input: {plays}")
            took = self._gettookfromXPlays(plays, card)
            return [took, sum(rolls[0:2])] # latter is wild returned from _getXPlays() function 
        except Penalty: # Took penalty
            self.card.penalty += 1
            took = Took({'didtake': False, 'tookwhat': []})
            took.ispenalty = True
            return [took, sum(rolls[0:2])]
    
    @logiof
    def wild(self, wild, card=None):
        if card == None:
            card = self.card
        plays = self._eval(self._getXPlaysfromwild(wild), card, iswild=True)
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
        plays = lse.evalAll(card)
        #logging.info(f"_evalall out: {lse.evalAll(card)}")
        return plays

    def _getXPlays(self, true_Dice):
        '''
        returns list that contains XPlay objects for 'False' dice, but 'False' for 'True' dice also returns rolls
        Rolls dice by self
        '''
        rolls = []
        for i in range(2):
            rolls.append(randint(1,6))
        for i in true_Dice:
            if not i:
                rolls.append(randint(1,6))
            else:
                rolls.append(False)
        #print("rolls: ", rolls)
        #Now turn rolls into XPlay 
        plays = []
        for i in range(2): #for both wilds added to colors
            for j in range(4): #for all color dice
                clroll = rolls[j+2] #color value currently being processed
                if clroll is not False: #Is color actually rolled (may be locked)
                    realrolls = [rolls[0] + clroll, rolls[1] + clroll] #Get actual numbers on scorecard
                    if j >= 2: #Is number is blue or green
                        for i, _ in enumerate(realrolls): #for both numbers in realrolls (added each wild to color)
                            toapp = XPlay([j, 12 - realrolls[i]], False) #12 - val to get index from number
                            plays.append(toapp) #append to list
                    else: #Means number is yellow or red
                        for i, _ in enumerate(realrolls): #for both numbers in realrolls (added each wild to color)
                            plays.append(XPlay([j, realrolls[i] - 2], False)) # val - 2 to get index from number
        plays += AI._getXPlaysfromwild(sum(rolls[0:2])) # Get all of the wild plays
        return plays, rolls #return data

    @classmethod
    def _getpossiblefromplays(cls, plays, card):
        '''
        Only returns possible XPlays in plays PlaysList). 
        Oh, and it's a one-liner because I'm awesome. So there.
        '''
        return PlaysList([play for play in plays if play.isPossible(card)])

    @classmethod
    def _getXPlaysfromwild(cls, wildint, plyrWild=False):
        plays = []
        for i in range(2): #for red and yellow that the two wilds added could go in
            plays.append(XPlay([i,wildint-2], True, plyrWild=plyrWild)) # append wild play for every color
        for i in range(2,4): #for blue and green that the two wilds added could go in
            plays.append(XPlay([i,12-wildint], True, plyrWild=plyrWild)) # append wild play for every color
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

        elif plays == []:
            took["didtake"] = False
            took["tookwhat"] = []

        else:
            warn("Warning: plays is unusual.(at AI._gettookfromXPlays() classmethod)")
        return took
        

class PlayerList(list):
    def __init__(self, list_of_Players):
        super().__init__(list_of_Players)
    
    def funcall(self, func, *argsf, active=None, **kwargsf):
        'Calls a function string on all players. Yields output of that function in tuple after active_player Player object'
        logging.info(f'func: {func}, *argsf: {argsf}, **kwargsf: {kwargsf}')
        for player in [x for x in self if x != active]:
            funcout = getattr(player.__class__, func)(player, *argsf, **kwargsf) # Run selected function. A bit clunky.
            #funcout = functocall(f"player.{func}(*argsf, **kwargsf)") # Run selected function. A bit clunky.
            logging.info(f'funcout to yield: {funcout}')
            yield player, (funcout)
    
    def getAIs(self):
        return list([x for x in self if isinstance(x, AI)])

    @staticmethod
    def _countTD(player):
        "Sort key for updateTDice func below"
        return player.true_Dice.count()
    
    def updateTDice(self):
        players = self[:] # Shallow copy
        players.sort(key=self._countTD)


class Took(dict): # Super simple class (pun intended) to make naming and extending easier.
    '''
    dict should be {"didtake": (False for did not take, True for took X(s)), "tookwhat": list of XPlays that was taken}
    '''
    def __init__(self, pdict):
        try:
            pdict['didtake']
            pdict['tookwhat']
        except KeyError:
            raise ValueError("Required dict fields are 'didtake' and 'tookwhat'")
        self.ispenalty = False # Set to true if penalty was taken
        super().__init__(pdict)
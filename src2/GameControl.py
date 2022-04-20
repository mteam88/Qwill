from Player import AI

def handlegameover(player_list):
    '''Accepts PlayerList object'''
    print('\tGAME OVER!!!\n\n')
    for ai in player_list.getAIs(): #For each ai in the game
        print(f'{ai.tag} scored a {ai.card.scoreCard()}', end='\n')
        print(f'{ai.tag}\'s final scoresheet is {ai.card}', end='\n\n')
    print('You can safely close the program now')
    input('Enter to quit')
    sys.exit()

def isgameover(player_list):
    '''Returns True if game is over, Accepts PlayerList object'''
    for ai in player_list.getAIs():
        if ai.card.true_Dice.count(True) >= 2:
            return True
        elif ai.card.penalty >= 20:
            return True
        else: continue


def newround(player_list, isfirstround=False):
    '''Increments round number for all players.'''
    #print(f"isfirstround {isfirstround}")

    def dispAICards(stringtoformat):
        '''Helper, displays AI's cards'''
        for player in player_list:
            if isinstance(player, AI): #Display ai player cards.
                print(stringtoformat.format(ptag=player.tag, pcard=player.card))

    if isfirstround:
        dispAICards("{ptag}'s card before round: {pcard}")
    if not isfirstround:
        dispAICards("{ptag}'s card after round: {pcard}")
        for player in player_list: 
            player.card.roundnum += 1 #Update round counter for all players
        print(f"\nRound {str(player_list[0].card.roundnum)}") #Using first player's roundnum, perhaps change to a class called GameState or something
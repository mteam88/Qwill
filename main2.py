#Run tests:
import subprocess
subprocess.run(["pytest", "src2/testing/"])

#Import
import random, sys, logging
from src2 import Card, XPlay, Player, LeastSkipped, AI, Human
from copy import deepcopy, copy
gameover = False

logging.basicConfig(level=logging.DEBUG)

def main(player_list):
    while not gameover:
        print(f"\nRound {str(player_list[0].card.roundnum)}") #Using first player's roundnum, perhaps change to a class called GameState or something
        for i, player in enumerate(player_list): # Loop through all players
            took, wild = player.turn(player.card)
            if isinstance(player, AI):
                if took != []: # If player took value
                    logging.debug(took) # debug only
                else:
                    logging.debug(took)
                    print("Did not take that play")
                print(f"{player.tag}'s card after turn: ", player.card)
            for player in player_list: # call .wild on all players
                if player != player_list[i]: #If player is not going right now
                    took = player.wild(wild, card=player.card)
                    if took != []: # If player took value
                        logging.debug(f"took1: {took}") # debug only
                    else:
                        logging.debug(f"took2: {took}")
                        print("Did not take that wild")
        for player in player_list: 
            player.card.roundnum += 1 #Update round counter for all players
            if isinstance(player, AI):
                print(f"{player.tag}'s card after round: ", player.card)

main(Player.initPlayers())
#Run tests:
#import subprocess
#subprocess.run(["pytest", "src2/testing/"])

#Import
import random, sys, logging
from src2 import Card, XPlay, Player, LeastSkipped, AI, Human, newround
from copy import deepcopy, copy

logging.basicConfig(level=logging.CRITICAL)

def main(player_list):
    newround(player_list,isfirstround=True)
    gameover = False
    while not gameover:
        newround(player_list)
        for active_player, (took, wild) in player_list.funcall("turn"):
            logging.info(f'out of turn funcall: {took, wild}')
            player_list.funcall("wild", wild, active=active_player) # call wild on all players

main(Player.initPlayers())
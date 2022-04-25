import sys
sys.path.append("src/")
from Scoresheet import Card, XPlay
from Player import Player, AI, Human, PlayerList
from Evaluaters import LeastSkipped
from GameControl import handlegameover, isgameover, newround
from loggingdecorator import logiof
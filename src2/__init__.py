import sys
sys.path.append("src2/")
from Scoresheet import Card, XPlay
from Player import Player, AI, Human
from Evaluaters import LeastSkipped
from GameControl import handlegameover, isgameover, newround
from loggingdecorator import logiof
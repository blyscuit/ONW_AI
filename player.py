import random
from game import Roles
from PlayerAI import PlayerAI
class Player:
    myCard = None
    actionDid = []
    voteFor = None
    playerID = None
    gameObject = None
    playerAI = None
    def __init__(self, roles, player, game, ai):
        self.myCard = roles
        self.playerID = player
        self.gameObject = game
        self.playerAI = ai

    def addAction(self, action):
        actionDid.append(action)
    
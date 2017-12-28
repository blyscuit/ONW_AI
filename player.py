import random
from game import Roles
from PlayerAI import PlayerAI
class Player:
    myCard = None
    myFirstCard = None
    actionDid = []
    voteFor = None
    playerID = None
    gameObject = None
    playerAI = None
    usedSkillOn = None
    def __init__(self, roles, player, game, ai):
        self.myCard = roles
        self.myFirstCard = roles
        self.playerID = player
        self.gameObject = game
        self.playerAI = ai

    def addAction(self, action):
        self.actionDid.append(action)
    
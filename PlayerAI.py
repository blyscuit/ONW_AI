from game import Roles, Game, ColorTextExt
import random
from action import Action, ActionType
#just the thinking
class PlayerAgent:
    sureCard = []
class PlayerAI(PlayerAgent):
    def lookOwnCard(self, playerObject):
        self.sureCard = [-1] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
    def vote(self, playerObject):
        # Random
        # numbers = range(playerObject.gameObject.numberOfPlayers)
        # numbers.remove(playerObject.playerID)
        # random.shuffle(numbers)
        # playerObject.voteFor = numbers.pop()

        #Believe everyone
        for claim in playerObject.gameObject.claimArray:
            if claim.role == Roles.WEREWOLF:
                playerObject.voteFor = claim.claimed
                return
        playerObject.voteFor = (playerObject.playerID + 1) % playerObject.gameObject.numberOfPlayers
    def claim(self, playerObject):
        #honest
        playerObject.gameObject.claimRole(playerObject.myCard, playerObject.playerID, playerObject.playerID)

    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myCard == Roles.SEER:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    self.sureCard[i] = playerObject.gameObject.lookAtCard(i)
                    playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, i, self.sureCard[i]))
            else:
                self.sureCard[randomCard] = playerObject.gameObject.lookAtCard(randomCard)
                playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, randomCard, self.sureCard[randomCard]))
        elif playerObject.myCard == Roles.THIEF:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            newcard = playerObject.gameObject.switchCard(playerObject.playerID, randomCard)
            playerObject.addAction(Action(playerObject.playerID, ActionType.TRADE, randomCard, newcard, playerObject.myCard))
            self.sureCard[randomCard] = playerObject.myCard
            self.sureCard[playerObject.playerID] = newcard
            playerObject.myCard = newcard
        elif playerObject.myCard == Roles.WEREWOLF:
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    self.sureCard[i] = Roles.WEREWOLF
        
        
class PlayerHuman(PlayerAgent):
    def vote(self, playerObject):
        pass
        # nPlayer = None
        # var = raw_input("Vote for player number: ")
        # print "you voted", var
        # try:
        #     nPlayer = int(float(var))
        # except ValueError:
        #     nPlayer = 0
        # playerObject.voteFor = nPlayer % playerObject.gameObject.numberOfPlayers

    def claim(self, playerObject):
        pass
        #honest
        # playerObject.gameObject.claimRole(playerObject.myCard, playerObject.playerID, playerObject.playerID)

    def lookOwnCard(self, playerObject):
        self.sureCard = [-1] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
    
    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myCard == Roles.SEER:
            numbers = -1
            while(numbers < 0 or numbers > playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER - 1):
                var = raw_input("You are SEER, look at number:")
                print ColorTextExt(0), "looking at", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    print ColorTextExt(0), i, "is", playerObject.gameObject.lookAtCard(i).name, ColorTextExt.RESET
            else:
                print ColorTextExt(0),randomCard, "is", playerObject.gameObject.lookAtCard(randomCard).name, ColorTextExt.RESET
        elif playerObject.myCard == Roles.THIEF:
            numbers = -1
            while(numbers < 0 or numbers > playerObject.gameObject.numberOfPlayers - 1):
                var = raw_input("You are THIEF, switch with number:")
                print ColorTextExt(0), "switching with", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            print ColorTextExt(0), "New role:", playerObject.gameObject.switchCard(playerObject.playerID, randomCard).name,ColorTextExt.RESET
        elif playerObject.myCard == Roles.WEREWOLF:
            print ColorTextExt(0), "You are WEREWOLF", ColorTextExt.RESET
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    print ColorTextExt(0), i, "is WEREWOLF", ColorTextExt.RESET
        elif playerObject.myCard == Roles.VILLAGER:
            print ColorTextExt(0), "You are VILLAGER", ColorTextExt.RESET
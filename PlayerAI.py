from game import Roles, Game, ColorTextExt
import random
from action import Action, ActionType
#just the thinking
class PlayerAgent:
    sureCard = []
    personWeight = []
    def talkingLoop(self, playerObject) :
        pass
    
    def vote(self, playerObject):
        pass

    def claim(self, playerObject):
        pass
    def thinkAboutClaims(self, playerObject):
        pass
        
class PlayerAI(PlayerAgent):
    def lookOwnCard(self, playerObject):
        self.sureCard = [-1] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
        self.personWeight = [50] * playerObject.gameObject.numberOfPlayers
        self.personWeight[playerObject.playerID] = 100
    def vote(self, playerObject):
        # Random
        # numbers = range(playerObject.gameObject.numberOfPlayers)
        # numbers.remove(playerObject.playerID)
        # random.shuffle(numbers)
        # playerObject.voteFor = numbers.pop()

        #Believe everyone
        if self.sureCard[playerObject.playerID] != Roles.WEREWOLF:
            for claim in playerObject.gameObject.claimArray:
                if claim.role is Roles.WEREWOLF:
                    playerObject.voteFor = claim.claimed
                    return
        else:
            for idx, role in enumerate(self.sureCard):
                if role != Roles.WEREWOLF and role != Roles.UNKNOWN:
                    playerObject.voteFor = idx
                    return
        playerObject.voteFor = (playerObject.playerID + 1) % playerObject.gameObject.numberOfPlayers
    def claim(self, playerObject):
        #honest
        pass
        # playerObject.gameObject.claimRole(playerObject.myCard, playerObject.playerID, playerObject.playerID)
        # playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH, playerObject.playerID, playerObject.myCard))
    def claimBeingSeer(self, playerObject, target, cardSaw, truth = False):
        playerObject.gameObject.claimRole(cardSaw, target, playerObject.playerID)
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, target, cardSaw))
    def claimBeingThief(self, playerObject, target, cardGet, cardWas, truth = False):
        playerObject.gameObject.claimThief(cardGet, target, playerObject.playerID)
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, target, cardWas))
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, playerObject.playerID, cardGet))
        
    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myFirstCard == Roles.SEER:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    self.sureCard[i] = playerObject.gameObject.lookAtCard(i)
                    playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, i, self.sureCard[i]))
                    playerObject.usedSkillOn = i
            else:
                self.sureCard[randomCard] = playerObject.gameObject.lookAtCard(randomCard)
                playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, randomCard, self.sureCard[randomCard]))
                playerObject.usedSkillOn = randomCard
        elif playerObject.myFirstCard == Roles.THIEF:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            newcard = playerObject.gameObject.switchCard(playerObject.playerID, randomCard)
            playerObject.addAction(Action(playerObject.playerID, ActionType.TRADE, randomCard, newcard, playerObject.myCard))
            self.sureCard[randomCard] = playerObject.myCard
            self.sureCard[playerObject.playerID] = newcard
            playerObject.myCard = newcard
            playerObject.usedSkillOn = randomCard
        elif playerObject.myFirstCard == Roles.WEREWOLF:
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    self.sureCard[i] = Roles.WEREWOLF
    sayingTruthOnce = False
    def talkingLoop(self, playerObject) :
        if not self.sayingTruthOnce:
            self.sayingTruthOnce = True
            if playerObject.myFirstCard == Roles.SEER:
                self.claimBeingSeer(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.usedSkillOn], True)
            elif playerObject.myFirstCard == Roles.THIEF:
                self.claimBeingThief(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.playerID], self.sureCard[playerObject.usedSkillOn], True)
            elif playerObject.myFirstCard == Roles.VILLAGER:
                playerObject.gameObject.claimRole(playerObject.myFirstCard, playerObject.playerID, playerObject.playerID)
            elif playerObject.myFirstCard == Roles.WEREWOLF:
                playerObject.gameObject.claimRole(Roles.VILLAGER, playerObject.playerID, playerObject.playerID)
    
    def thinkAboutClaims(self, playerObject):
        noteSureCard = [None] * len(self.sureCard)
        for idx, role in enumerate(self.sureCard):
            if role != -1:
                noteSureCard[idx] = {'role': role, 'by': playerObject.playerID}

        for claim in playerObject.gameObject.claimArray:

            if noteSureCard[claim.claimed] != None and self.personWeight[claim.claimBy] >= self.personWeight[noteSureCard[claim.claimed]['by']]:
                noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
            elif noteSureCard[claim.claimed] == None:
                noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
        roleCount = [0] * Roles.roleCount
        for role in noteSureCard:
            if role != None:
                roleCount[role["role"].value] += 1
        if roleCount[Roles.WEREWOLF.value] > 2 or roleCount[Roles.THIEF.value] > 1 or roleCount[Roles.SEER.value] > 1 or roleCount[Roles.VILLAGER.value] > playerObject.gameObject.numberOfPlayers - playerObject.gameObject.CENTER_NUMBER:
            print ColorTextExt(playerObject.playerID), "something is WRONG!", ColorTextExt.RESET
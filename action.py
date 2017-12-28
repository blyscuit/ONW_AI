from game import enum
ActionType = enum(
    LOOK = 0,
    TRADE = 1,
    LIE = 2,
    TRUTH = 3,
    MAYBE = 4
)
class Action:
    performer = None
    targetPerson = None
    actionType = None
    result = None
    secondResult = None
    def __init__(self, performer, actionType, targetPerson = None, result = None, secondResult = None):
        self.performer = performer
        self.targetPerson = targetPerson
        self.actionType = actionType
        self.result = result
        self.result = secondResult
        pass
    

"""
cohost.py
from askaninjask

Goal: To produce a program that will "spit out" results, instead of having
       to work on them individually each night.

Stages: Set-up (write crucial things to file)
         In-game
         Notes (for postgame)

Entities:
  Players
    have: life, actions, votes, faction, items, role PM, 
        conditions on whether targetable or not, etc.
    do: send targets for night actions and items, die

Actions
    have: player, effect, results, targets, priority, text to be sent

Items
    have: action, holder, description, pass action

Results
    have: user, body
   
Factions
    have: members, win condition, inheritable roles
   
Public Notes
    have: body
   
Everything is remembered and stored into a file so that the data can be
 recollected at any time.
"""
playerList = []

class Player:
    def __init__(self, actionDescriptions, itemDescriptions, username):
        self.actions = []
        self.items = []
        self.votesFor = 0
        self.username = username
        for a in actionDescriptions:
            self.actions.append(Action(a))
        for i in itemDescriptions:
            self.items.append(item(i))

class Action:
    def __init__(self, description):
        self.name = description
        self.atNight = True
        self.atDay = False
        self.results = [] #list of dictionaries
        self.stopped = False

    def perform():
        pass


def cycle(time):
    actionList = []
    resultList = []
    
    # From the list of living players, construct a list of all actions stemming
    # from those players (night actions and item actions).    
    for user in playerList:
        
        for action in user.actions:
            if time == "Night":
                if atNight: actionList.append(action)
            elif time == "Day":
                if atDay: actionList.append(action)
            else: raise NameError("Time must be either 'Day' or 'Night'")
            
        for item in user.items:
            if time == "Night":
                if atNight: actionList.append(item.action)
            elif time == "Day":
                if atDay: actionList.append(item.action)
            else: raise NameError("Time must be either 'Day' or 'Night'")
            actionList.append(item.move)
            
    if time == "Day":
        # determine the votes and add the lynch to the list of actions
        for user in playerList:
            user.vote.votesFor += 1
        maximum = 0
        doghouse = ["No Lynch"]
        for user in playerList:
            if user.votesFor > maximum:
                if "No Lynch" in doghouse: doghouse.remove("No Lynch")
                doghouse = [user]
                maximum = user.votesFor
            if (user.votesFor == maximum) and "No Lynch" not in doghouse:
                doghouse.append[user]
        if (len(doghouse) != 1) or "No Lynch" in doghouse:
            resultList.append({"message": "No Lynch", "to": "everyone"})
        else:
            actionList.append(Action("lynch"))
            
    # sort this list of actions by priority from high to low
    actionList = sorted(actionList, key = lambda a: a.priority, reverse = True)
    
    # iterate through each action in actionList and carry out the action. Append
    # results to the resultList after completion.
    for action in actionList:
        action.perform()
        for result in action.results:
            resultList.append(result)

    resultList = sorted(resultList, key = lambda r: r.to)

    for result in resultList:
        print result

    print "Living players:"
    for c in playerList:
        print c.username

##def night():
##    actionList = []
##    resultList = []
##    
##    # From the list of living players, construct a list of all actions stemming
##    # from those players (night actions and item actions).    
##    for user in playerList:
##        for action in user.actions:
##            if atNight: actionList.append(action)
##        for item in user.items:
##            if atNight: actionList.append(item.action)
##            actionList.append(item.move)
##            
##    # sort this list of actions by priority from high to low
##    actionList = sorted(actionList, key = lambda a: a.priority, reverse = True)
##    
##    # iterate through each action in actionList and carry out the action. Append
##    # results to the resultList after completion.
##    for action in actionList:
##        action.perform()
##        for result in action.results:
##            resultList.append(result)
##
##    resultList = sorted(resultList, key = lambda r: r.to)
##
##    for result in resultList:
##        print result
##
##    print "Living players:"
##    for c in playerList:
##        print c.username
##
##
##
##
##def day():
##    # From the list of living players, construct a list of all actions stemming
##    # from those players that happen in the day.
##    actionList = []
##    resultList = []
##    
##    for user in playerList:
##        for action in user.actions:
##            if atDay: actionList.append(action)
##        for item in user.items:
##            if atDay: actionList.append(item.action)
##            actionList.append(item.move)
##
##    # determine the votes and add the lynch to the list of actions
##    for user in playerList:
##        user.vote.votesFor += 1
##    maximum = 0
##    doghouse = ["No Lynch"]
##    for user in playerList:
##        if user.votesFor > maximum:
##            if "No Lynch" in doghouse: doghouse.remove("No Lynch")
##            doghouse = [user]
##            maximum = user.votesFor
##        if (user.votesFor == maximum) and "No Lynch" not in doghouse:
##            doghouse.append[user]
##    if (len(doghouse) != 1) or "No Lynch" in doghouse:
##        resultList.append({"message": "No Lynch", "to": "everyone"})
##    else:
##        actionList.append(Action("lynch"))
##        
##
##    # sort this list of actions by priority from high to low
##    actionList = sorted(actionList, key = lambda a: a.priority, reverse = True)
##
##    # iterate thourgh actions etc
##    for action in actionList:
##        action.perform()
##        for result in action.results:
##            resultList.append(result)
##
##    resultList = sorted(resultList, key = lambda r: r.to)
##
##    for result in resultList:
##        print result
##
##        print "Living Players:"
##        for c in playerList: print c.username

def clear():
    for user in playerList:
        self.votesFor = 0
        for action in user.actions:
            self.results = []
            self.stopped = False

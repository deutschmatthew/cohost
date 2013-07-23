class Player:
    """This init function takes strings corresponding to various
       actions, dictionaries corresponding to the necessary item
       information including its name and action description."""
    def __init__(self, actionsInfo, itemsInfo, username, rolename):
        self.type = "Player"
        self.actions = []
        self.items = []
        self.votesFor = 0
        self.username = username
        self.rolename = rolename
        for a in actionsInfo:
            self.actions.append(Action(a, self))
        for i in itemsInfo:
            self.items.append(Item(i, self))

    def clear(self):
        self.votesFor = 0
        for a in self.actions:
            a.clear()
        for i in self.items:
            i.clear()


class Item:
    def __init__(self, itemInfo, holder):
        self.type = "Item"
        self.name = itemInfo["name"]
        self.actions = []
        self.holder = holder
        for a in itemInfo["actionsInfo"]:
            self.actions.append(Action(a, self))
        self.actions.append(
            Action({
                "name": "move",
                "priority": 0,
                "atNight": True,
                "atDay": True
            }, self))

    def clear(self):
        for a in self.actions:
            a.clear()
        self.move.clear()


class Action:
    def __init__(self, actionInfo, owner):
        self.name = actionInfo["name"]
        self.atNight = actionInfo["atNight"]
        self.atDay = actionInfo["atDay"]
        self.priority = actionInfo["priority"]
        self.results = []  # list of dictionaries
        self.stopped = False
        self.owner = owner
        self.ownerType = owner.type
        self.targets = []  # list of Players, not usernames.

    def perform(playerList, self):
        if self.stopped:
            return None

        if self.name == "move":
            if self.ownerType == "Item":
                self.owner.holder = self.targets[0]
                self.targets[0].items.append(self.owner)
                self.owner.holder.items.remove(self.owner)
                self.results.append({
                    "message": "You have been passed the " + self.owner.name,
                    "to": self.targets[0]
                })
            else:
                raise TypeError("Action 'move' must belong to an Item")

        elif self.name == "kill":
            playerList.remove(self.targets[0])
            self.results.append({
                "message": self.targets[0].username + " has been murderized by " + self.owner.username,
                "to": "everyone"
            })

        elif self.name == "hooker":
            for a in self.targets[0].actions:
                a.stopped = True
            for i in self.targets[0].items:
                for ia in i.actions:
                    ia.stopped = True

        elif self.name == "bodyguard":
            for user in playerList:
                for a in user.actions:
                    if a.name == "kill":
                        if a.targets[0] == self.targets[0]:
                            a.stopped = True
                            self.results.append({
                                "message": "Your kill was bodyguarded by " + self.owner.username,
                                "to": a.owner.username
                            })

        elif self.name == "martyr":
            for a in self.targets[0].actions:
                for t in a.targets:
                    t = self.owner
            self.results.append({
                "message": self.owner.username + " stood in your way last night so you targeted him instead.",
                "to": self.targets[0]
            })
            pass

        elif self.name == "rogue":
            pass

        elif self.name == "safeguard":
            for user in playerList:
                for a in user.actions:
                    if a.name != "kill":
                        for target in a.targets[0]:
                            if target == self.targets[0]:
                                a.stopped = True
                                self.results.append({
                                    "message": "Your action was blocked by " + self.owner.username,
                                    "to": a.owner.username
                                })

        elif self.name == "inspector":
            self.results.append({
                "message": self.targets[0] + "'s role PM",
                "to": self.owner.username
            })
            pass

        elif self.name == "persuader":
            pass
        elif self.name == "silencer":
            pass

        pass

    def clear(self):
        self.targets = []
        self.results = []
        self.stopped = False

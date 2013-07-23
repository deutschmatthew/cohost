"""
cohost.py
from askaninjask

Goal:   To produce a program that will "spit out" one night's worth of results,
        instead of having to work on them individually.

Stages: Set-up (write crucial things to file)
        Nighttime

TODO:
[ ] Set up input for night.
[ ] Incorporate Factions:
    members, inheritable roles, faction wide roles

Everything is stored in a google spreadsheet which is accessed using gspread.
"""
playerList = []


def init_from_sheet():
    # Authorize the user and login.
    password = raw_input("The password: ")
    dummy = True
    while dummy:
        try:
            gc = gspread.login('cohost.invite@gmail.com', password)
            dummy = False
        except AuthenticationError:
            print "Wrong password."
            password = raw_input("Retry?: ")
            dummy = True
    # Get the name of the sheet
    dummy2 = True
    print "What is the name of your master spreadsheet?:"
    mastersheet = None
    while dummy2:
        sheetname = raw_input()
        # Open the sheet
        try:
            mastersheet = gc.open(sheetname).get_worksheet(0)
            # This kind of sucks. There should be a better way...
        except SpreadsheetNotFound:
            print "No spreadsheet with such a name found. Perhaps you haven't"\
                " added cohost.invite@gmail.com to your spreadsheet?"
            print "Retry?:"
        else:
            dummy2 = True
    # Find the column marked "Smogon Usernames" in the sheet.
    usernameCell = mastersheet.find("Smogon Username")
    actionCell = mastersheet.find("Night Action")
    itemCell = mastersheet.find("Item")

    if any([
        usernameCell.row != 1,
        actionCell.row != 1,
        itemCell.row != 1
    ]):
        raise ValueError("I am an idiot computer, unable to understand your"
                         " formatting.")
    usernameCol = usernameCell.col
    actionCol = actionCell.col
    itemCol = itemCell.col


def cycle():
    resultList = []

    # From the list of living players, construct a list of all actions stemming
    # from those players (night actions and item actions).
    actionList = contruct_action_list()

    # sort this list of actions by priority from high to low
    actionList = sorted(actionList, key=lambda a: a.priority, reverse=True)

    # iterate through each action in actionList and carry out the action.
    # append results to the resultList after completion.
    for action in actionList:
        action.perform(playerList)
        for result in action.results:
            resultList.append(result)

    publicResults = []
    for anyresult in resultList:
        if anyresult["to"] == "everyone":
            publicResults.append(anyresult)
    resultList = sorted(resultList, key=lambda r: r["to"])

    displayresults(resultList)

    print "Living players:"
    for c in playerList:
        print c.username


def construct_action_list():
    actionList = []
    for user in playerList:
        for action in user.actions:
            if all(time == "Night", action.atNight):
                actionList.append(action)
            elif all(time == "Day", action.atDay):
                actionList.append(action)
            else:
                raise NameError("Time must be either 'Day' or 'Night'")
        for item in user.items:
            if all(time == "Night", action.atNight):
                actionList.append(item.action)
            elif all(time == "Day", action.atDay):
                actionList.append(item.action)
            else:
                raise NameError("Time must be either 'Day' or 'Night'")
    return actionList


def clear():
    for user in playerList:
        user.clear()


def displayresults(resultList):
    for result in resultList:
        print result

#    if time == "Day":
#        # determine the votes and add the lynch to the list of actions
#        for user in playerList:
#            user.vote.votesFor += 1
#        maximum = 0
#        doghouse = ["No Lynch"]
#        for user in playerList:
#            if user.votesFor > maximum:
#                if "No Lynch" in doghouse: doghouse.remove("No Lynch")
#                doghouse = [user]
#                maximum = user.votesFor
#            if (user.votesFor == maximum) and "No Lynch" not in doghouse:
#                doghouse.append[user]
#        if (len(doghouse) != 1) or "No Lynch" in doghouse:
#            resultList.append({"message": "No Lynch", "to": "everyone"})
#        else:
#            actionList.append(Action("lynch"))

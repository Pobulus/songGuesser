from yacht.anchor import *
import mpris as mp
from thefuzz import fuzz

threshold  = 75

class Game:
    def __init__(self, uid):
        self.id = uid
        self.players = {}
        self.inProgress = False
        self.service = mp._open_service(mp.get_services(), 0)
        self.title= "<not started yet>"
        print(self.service)

    def guess(self):
        self.title = "Guessing..."
        self.revealed = False
        self.service.next()
        for player in self.players.values():
            player.guess = ""

    def start(self):
        self.inProgress = True
        print(f"Game {self.id} starting!")
        self.guess()

    def reveal(self):
        self.title = self.service.player.Metadata.get("xesam:title")
        self.revealed = True
        self.inProgress = False
        for player in self.players.values():
            ratio = fuzz.partial_ratio(player.guess, self.title) 
            print(ratio)
            if ratio > threshold:
                player.result = True
                player.points += 1
            else:
                player.result = False
            player.ready = False


class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.guess = ""
        self.ready = False
        self.result = ""



games = {"123": Game("123")}

uid = "123"


def _checkPlayersReady(p):
    for player in p.values():
        if not player.ready:
            return False
    return True

def _checkPlayersNotReady(p):
    for player in p.values():
        if player.ready:
            return False
    return True
@anchor
def newPlayer(req):
    name = getRequestBody(req).get("value", "")

    if name:
        previousNameC = getCookie(req).get("playerName")
        previousName = ""
        if previousNameC is not None:
            previousName = previousNameC.value
        
        if previousName in games[uid].players.keys():
            del games[uid].players[previousName]
        
        
        games[uid].players[name] = Player(name)
        cookie = SimpleCookie()
        cookie["playerName"] = name
        setCookie(req, cookie)
        
        return name
    else:
        return "no name provided"

@anchor        
def getPlayers(req):
    output = ""
    for name in games[uid].players.keys():
        output += f"\n    <li>{name}</li>"
    return output

@anchor
def signalReady(req):
    nameC = getCookie(req).get("playerName")
    if nameC is not None:
        if nameC.value in games[uid].players.keys():
            games[uid].players[nameC.value].ready = True
            if(_checkPlayersReady(games[uid].players)):
                games[uid].start()
        return "waitingRoom.yaml"
    return ""

@anchor
def checkReady(req):
    return "guess.yaml" if games[uid].inProgress else ""
    
@anchor
def setGuess(req):
    guess = getRequestBody(req).get("value", "")
    if guess:
        nameC = getCookie(req).get("playerName")
        if nameC is not None:
            games[uid].players[nameC.value].guess = guess
    return ""

@anchor
def submitGuess(req):
    nameC = getCookie(req).get("playerName")
    if nameC is not None:
        games[uid].players[nameC.value].ready = False
        if _checkPlayersNotReady(games[uid].players):
            games[uid].reveal()
    return "awaitReveal.yaml"
@anchor
def checkRevealed(req):
    return "reveal.yaml" if games[uid].revealed else ""
    
@anchor
def getSongName(req):
    return games[uid].title


@anchor
def getResult(req):
    nameC = getCookie(req).get("playerName")
    if nameC is not None:
        return "You were: "+("Correct!" if games[uid].players[nameC.value].result else "Wrong :(")

@anchor
def getResultsTable(req):
    out = "<tr><th>Player</th><th>Guess</th><th>Score</th>"
    for player in games[uid].players.values():
        out += f"\n<tr><td>{player.name}</td>"
        out += f"<td>{player.guess} {'👍' if player.result else '💀' }</td>"
        out += f"<td>{str(player.points)}</td></tr>"
    return out
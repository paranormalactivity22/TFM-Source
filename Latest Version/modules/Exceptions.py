import time, traceback

class GameException():
    def __init__(self, client):
        self.client = client
        
    def Invoke(self, ExceptionType, playerName="", functionName=""):
        if ExceptionType == "unknownuser":
            self.client.sendClientMessage("The supplied argument isn't a valid nickname.", 1)
        elif ExceptionType == "moreargs":
            self.client.sendClientMessage("You need more arguments to use this command.", 1)
        elif ExceptionType == "requireFC":
            self.client.sendClientMessage("FunCorp commands only work when the room is in FunCorp mode.", 1)
        elif ExceptionType == "unknownuserorip":
            self.client.sendClientMessage("The supplied argument is neither a valid nickname nor an IP address.", 1)
        elif ExceptionType == "notloggedin":
            self.client.sendClientMessage("The player "+playerName+" hasn't logged in since the last reboot.", 1)
        elif ExceptionType == "notallowedlua":
            self.client.sendLuaMessage(f"[<V>{self.client.roomName}</V>] [{self.client.playerName}] You're not allowed to use the function {functionName}.")
        elif ExceptionType == "useralreadybanned":
            self.client.sendClientMessage("Player ["+playerName+"] is already banned, please wait.", 1)
        elif ExceptionType == "usernotbanned":
            self.client.sendClientMessage("The player "+playerName+" is not banned.", 1)
        elif ExceptionType == "useralreadymuted":
            self.client.sendClientMessage("Player ["+playerName+"] is already muted, please wait.", 1)
        elif ExceptionType == "usernotmuted":
            self.client.sendClientMessage("The player "+playerName+" is not muted.", 1)
        elif ExceptionType == "norecordfound":
            self.client.sendClientMessage("The map "+playerName+" don't have a record.", 1)
        elif ExceptionType == "noonlinestaff":
            self.client.sendClientMessage("Don't have any online "+playerName+" at moment.", 1)
        return
        
class ServerException():
    def __init__(self, Exception):
        self.exception = Exception
        
    def getTypeError(self, Type):
        if Type == "commanderreur":
            return "Command Erreur"
        elif Type == "tribulleerreur":
            return "Tribulle Erreur"
        elif Type == "packeterreur":
            return "Packet Erreur"
        return "Server Erreur"
        
    def SaveException(self, filename, client, Type):
        c = open(f"./include/logs/Errors/{filename}", "a")
        c.write("=" * 60)
        c.write(f"\n- Time: {time.strftime('%d/%m/%Y - %H:%M:%S')}\n- Name: {client.playerName}\n- {self.getTypeError(Type)} {self.exception}\n")
        traceback.print_exc(file=c)
        c.write("\n")
        c.close()
        client.sendServerMessageAdmin(f"<BL>[<R>ERROR<BL>] The user <R>{client.playerName}</R> found {self.getTypeError(Type)} [{time.strftime('%d/%m/%Y - %H:%M:%S')}].")
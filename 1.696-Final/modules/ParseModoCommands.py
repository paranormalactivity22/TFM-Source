#coding: utf-8
import re, sys, json, os, time, random, traceback, datetime

# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Exceptions import ServerException

class ModoCommands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0

    def sendBotMessage(self, message):
        self.client.sendPacket(Identifiers.send.Staff_Chat, ByteArray().writeByte(4).writeUTF("Delichoc").writeUTF(message).writeShort(0).writeShort(0).toByteArray())
    
    def requireArguments(self, arguments):
        if self.currentArgsCount < arguments:
            return False
        elif self.currentArgsCount == arguments:
            return True
        else:
            return False
    
    def parseCommand(self, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        self.currentArgsCount = argsCount
        try:
            if command in [".p", ".profile", ".perfil"] and self.requireArguments(1):
                self.client.sendProfile(Utils.parsePlayerName(args[0]))
                
            elif command in [".roompw", ".roompassword"] and self.requireArguments(1):
                roomName = argsNotSplited.split(" ", 0)[0]
                if roomName in self.server.rooms:
                    for client in self.server.rooms[roomName].clients.values():
                        if client != None:
                            password = client.room.roomPassword
                    self.sendBotMessage(password) if password != "" else self.sendBotMessage(f"The room {roomName} doesn't have password.")
                else:
                    self.sendBotMessage(f"The room {roomName} doesn't exists.")
                    
            elif command in [".relation"] and self.requireArguments(1):
                player = self.server.players.get(Utils.parsePlayerName(args[0]))
                if player != None:
                    r1 = []
                    displayed = []
                    List = "The player <BV>"+str(player.playerName)+"</BV> has the following relations:"
                    self.Cursor.execute("select distinct Username from LoginLogs where IP = %s", [Utils.EncodeIP(player.ipAddress)])
                    ip2 = f"<font color='{player.ipColor}'>{Utils.EncodeIP(player.ipAddress)}</font>"
                    for rs in self.Cursor.fetchall():
                        if rs[0] in displayed: continue
                        if self.server.players.get(str(rs[0])) == None:
                            d = self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [str(rs[0])])
                            d = self.Cursor.fetchall()
                            ips = []
                            ips2 = []
                            for i in d:
                                if i[0] in ips2: continue
                                ips.append(f"<font color='{Utils.DecodeIP(i[0])}'>{i[0]}</font>")
                                ips2.append(i[0])
                            toshow = ", ".join(ips)
                            List += f"<br>- <BV>{rs[0]}</BV> : {toshow}"
                        else:
                            ip31 = self.server.players.get(str(rs[0]))
                            List += f"<br>- <BV>{rs[0]}</BV> : <font color='{ip31.ipColor}'>{Utils.EncodeIP(ip31.ipAddress)}</font> (current IP)"
                        displayed.append(rs[0])
                    self.client.sendClientMessage(List, 1)

            elif command in [".log", ".casier"] and self.requireArguments(1):
                player = self.server.players.get(Utils.parsePlayerName(args[0]))
                if player != None:
                    try:
                        message = "<p align='center'><N>Sanction Logs for <V>"+player.playerName+"</V></N>\n</p><p align='left'>Currently running sanctions: </p><br>"
                        self.Cursor.execute("select * from casierlog where Name = %s order by Timestamp desc limit 0, 200", [player.playerName])
                        for rs in self.Cursor.fetchall():
                            name,ip,state,timestamp,modName,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5],rs[6]
                            fromtime = str(datetime.datetime.fromtimestamp(float(int(timestamp))))
                            ip = Utils.EncodeIP(player.ipAddress)
                            if time == '': time = 0
                            sanctime = (int(time)*60*60)
                            totime = datetime.datetime.fromtimestamp(float(int(timestamp) + sanctime))
                            totime1 = datetime.datetime.utcfromtimestamp(float(int(timestamp) + sanctime))
                            if state in ["UNMUTE", "UNBAN"]:
                                message = message + "<G><font size='12'><p align='left'> - </G><G><b>" + state + "</b> (" + str(ip) + ") by " + modName + "</font></G>\n"
                                message = message + "<G><p align='left'><font size='9'>    " + fromtime + "</font></G>\n\n"
                            elif state == "MUMUTE":
                                message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                                message = message + "<p align='left'><font size='9'>    " + fromtime + "</font>\n\n"
                            else:
                                message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                                if totime1 != None:
                                    message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " | "+ str(totime) + " → "+ str(totime1) + "</N2>\n\n"
                                elif totime != None:
                                    message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " → "+ str(totime) + "</N2>\n\n"
                                else:
                                    message = message + "<p align='left'><font size='9'><N2>    " + fromtime + "</N2>\n\n"
                        self.client.sendLogMessage(message)
                    except:
                        self.sendBotMessage("There has been an error when retrieving the list of sanctions of the player "+player.playerName+" : PARAMETRE_INVALIDE.")

            elif command in [".chatlog"] and self.requireArguments(1):
                self.client.modoPwet.openChatLog(Utils.parsePlayerName(args[0]))

        except Exception as e:
            sex = ServerException(e)
            sex.SaveException("Commands.log", self.client, "commanderreur")
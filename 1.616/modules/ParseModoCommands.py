#coding: utf-8
import re, sys, json, os, time, random, traceback

# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

class ModoCommands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0

    def sendBotMessage(self, message):
        self.client.sendStaffCM(4, "Delichoc", message)
    
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
            if command in [".avatar"] and self.requireArguments(1):
                playerName = args[0]
                avatar = ""
                player = self.server.players.get(playerName)
                if player != None:
                    self.Cursor.execute("select distinct avatar from users where Username = %s", [player.playerName])
                    for rs in self.Cursor.fetchall():
                        avatar += rs[0]
                    
                    self.sendBotMessage(player.playerName+"'s avatar: "+avatar)
            elif command in [".p", ".profile", ".perfil"] and self.requireArguments(1):
                self.client.sendProfile(Utils.parsePlayerName(args[0]))
            elif command in [".lswatch"]:
                message = ""
                for m in self.client.ModoWatchedPlayers:
                    message += m + '\n';
                self.client.sendLogMessage(message)

        except Exception as e:
            c = open("./logs/Errors/Commands.log", "a")
            c.write("\n" + "=" * 60 + "\n- Time: %s\n- Name: %s\n- Error Command: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), self.client.playerName))
            traceback.print_exc(file=c)
            c.close()
            self.client.sendServerMessageAdmin("<BL>[<R>ERROR<BL>] The user <R>%s</R> used error command [%s] in <font color='#C565FE'>#Modo</font>." %(self.client.playerName, time.strftime("%d/%m/%Y - %H:%M:%S")))
            
#coding: utf-8
import re, sys, json, os, base64, hashlib, time, random, asyncio, ast
"""
9 Admin, 8 Mod, 7 Arb, 6 MC, 5 FC, 4 LC, 3 - FS, 2 Sentinel, 1 PPL
Commands: /resign, /colormouse, /colornick, /lsbulle, /execpacket, /geoip, /tag

./tag [tag] [mapcode] [description] : Adds a tag to a map, or removes it if the map already had it
"""
# Modules
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Exceptions import ServerException
from modules import Lua

# Library
from datetime import datetime

class Commands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0
        self.lastsonar = 0
        self.owners = ["Chatta#0001", "Test#0213"] # i forgor
        self.commands = {}
        self.__init_2()
        
    def requireLevel(self, level=0, roomOwner=False, lua=False, mc=False, fc=False, arb=False):
        if roomOwner and self.client.privLevel < 5: return self.client.room.roomCreator == self.client.playerName or self.requireTribePerm(2046) or (self.client.isLuaCrew if lua else lua) or (self.client.isMapCrew if mc else mc) or (self.client.isFuncorpPlayer if fc else fc) or (self.client.isArbitre if arb else arb)
        return self.client.privLevel >= level or (self.client.isLuaCrew if lua else lua) or (self.client.isMapCrew if mc else mc) or (self.client.isFuncorpPlayer if fc else fc) or (self.client.isArbitre if arb else arb)

    def requireArgs(self, arguments, flags=False):
        if self.currentArgsCount < arguments:
            self.client.playerException.Invoke("moreargs")
            return False
        elif self.currentArgsCount >= arguments:
            return True
        else:
            return flag

    def requireTribePerm(self, permId):
        if self.client.room.isTribeHouse:
            rankInfo = self.client.tribeRanks.split(";")
            rankName = rankInfo[self.client.tribeRank].split("|")
            if rankName[2] in str(permId):
                return True
        elif self.client.privLevel >= 5: 
            return True
        else:
            return False
    
    def requireOwner(self):
        return self.client.playerName in self.owners
        
    
    def command(self,func=None,tribe=False,args=0,level=0,owner=False,roomOwner=False,lua=False,mc=False,fc=False,arb=False,alies=[],reqrs=[]):
        if not func:
            reqrs=[]
            if tribe: reqrs.append(['tribe',tribe])
            if args > 0: reqrs.append(['args',args])
            if level > 0: reqrs.append(['level',(level,roomOwner,lua,mc,fc,arb)])
            if owner: reqrs.append(['owner'])
            return lambda x: self.command(x,tribe,args,level,owner,roomOwner,lua,mc,fc,arb,alies,reqrs)
        else:
            for i in alies + [func.__name__]: self.commands[i] = [reqrs,func]
    
    async def parseCommand(self, command):
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        self.currentArgsCount = argsCount
        self.Cursor['commandlog'].insert_one({'Time':Utils.getTime(),'Username':self.client.playerName,'Command':command})
        self.client.sendServerMessageAdmin("<J>[%s]</J> <BV>%s</BV> used command ----> <CH2>%s</CH2>" %(Utils.getTime(), self.client.playerName, command))
        if command in self.commands:
            for i in self.commands[command][0]: 
                if i[0] == "level": 
                    if not self.requireLevel(*i[1]): return
                elif i[0] == "args":
                    if not self.requireArgs(i[1]): return
                elif i[0] == "tribe":
                    if not self.requireTribePerm(i[1]): return
                else:
                    if not self.requireOwner(): return
            await self.commands[command][1](self, *args)
    
    def __init_2(self):
    
# Player Commands
        @self.command(alies=['profil','perfil','profiel'])
        async def profile(self, name=''):
            self.client.sendProfile(Utils.parsePlayerName(name) if name else self.client.playerName)
        
        @self.command(alies=['editor'], level=1)
        async def editeur(self):
            self.client.sendPacket(Identifiers.send.Room_Type, 1)
            self.client.enterRoom("\x03[Editeur] %s" %(self.client.playerName))
            self.client.sendPacket(Identifiers.old.send.Map_Editor, [])
        
        @self.command(level=1)
        async def totem(self):
            if self.client.shamanSaves >= self.server.minimumNormalSaves:
                self.client.enterRoom("\x03[Totem] %s" %(self.client.playerName))
        
        @self.command(level=1)
        async def sauvertotem(self):
            if self.client.room.isTotemEditor:
                self.client.totem[0] = self.client.tempTotem[0]
                self.client.totem[1] = self.client.tempTotem[1]
                self.client.sendPlayerDied()
                self.client.enterRoom(self.server.recommendRoom(self.client.langue))
        
        @self.command(level=1)
        async def resettotem(self):
            if self.client.room.isTotemEditor:
                self.client.totem = [0 , ""]
                self.client.tempTotem = [0 , ""]
                self.client.resetTotem = True
                self.client.isDead = True
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()
        
        @self.command(alies=['mods'], level=1)
        async def mod(self):
            staffList, staff = "$ModoPasEnLigne", {}
            for player in self.server.players.copy().values():
                if player.privLevel == 8:
                    if player.langue.lower() in staff:
                        names = staff[player.langue.lower()]
                        names.append(player.playerName)
                        staff[player.langue.lower()] = names
                    else:
                        names = []
                        names.append(player.playerName)
                        staff[player.langue.lower()] = names
            if len(staff) >= 1:
                staffList = "$ModoEnLigne"
                for list in staff.items():
                    staffList += "<br>[%s] <BV>%s</BV>" %(list[0], ("<BV>, <BV>").join(list[1]))
            self.client.sendLangueMessage("", staffList)
        
        @self.command(level=1)
        async def mapcrew(self):
            staffList, staff = "$MapcrewPasEnLigne", {}
            for player in self.server.players.copy().values():
                if player.privLevel == 6:
                    if player.langue.lower() in staff:
                        names = staff[player.langue.lower()]
                        names.append(player.playerName)
                        staff[player.langue.lower()] = names
                    else:
                        names = []
                        names.append(player.playerName)
                        staff[player.langue.lower()] = names
            if len(staff) >= 1:
                staffList = "$MapcrewEnLigne"
                for list in staff.items():
                    staffList += "<br>[%s] <BV>%s</BV>" %(list[0], ("<BV>, </BV>").join(list[1]))
            self.client.sendLangueMessage("", staffList)
        
        @self.command(level=1, roomOwner=True)
        async def pw(self, password = ''):
            if self.currentArgsCount == 0:
                self.client.room.roomPassword = ""
                self.client.sendLangueMessage("", "$MDP_Desactive")
            else:
                self.client.room.roomPassword = password
                self.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))
        
        @self.command(alies=["titre", "titulo", "titel"], level=1)
        async def title(self, titleID=0):
            if self.currentArgsCount == 0:
                p = ByteArray()
                p2 = ByteArray()
                titlesCount = 0
                starTitlesCount = 0
                for title in self.client.titleList:
                    titleInfo = str(title).split(".")
                    titleNumber = int(titleInfo[0])
                    titleStars = int(titleInfo[1])
                    if titleStars > 1:
                        p.writeShort(titleNumber).writeByte(titleStars)
                        starTitlesCount += 1
                    else:
                        p2.writeShort(titleNumber)
                        titlesCount += 1
                self.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())
            else:
                found = False
                for title in self.client.titleList:
                    if str(title).split(".")[0] == titleID:
                        found = True

                if found:
                    self.client.titleNumber = int(titleID)
                    for title in self.client.titleList:
                        if str(title).split(".")[0] == titleID:
                            self.client.titleStars = int(str(title).split(".")[1])
                    self.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(self.client.gender).writeShort(titleID).toByteArray())
        
        @self.command(alies=["die", "kill"])
        async def mort(self):
            if not self.client.isDead and not self.client.room.disableMortCommand:
                self.client.isDead = True
                if not self.client.room.noAutoScore: self.client.playerScore += 1
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()
        
        @self.command(args=1)
        async def mjj(self, roomName):
            if roomName.startswith("#"):
                if roomName[1:] in self.server.minigames:
                    self.client.enterRoom(f"{self.client.langue.lower()}-{roomName}" + "1")
            else:
                self.client.enterRoom(({0:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[self.client.lastGameMode]) + roomName)
        
        @self.command
        async def ping(self):
            self.client.sendClientMessage("ping ~%s" % str(self.client.PInfo[2]), 1)
            
        @self.command(level=9,roomOwner=True)
        async def mulodrome(self):
             if not self.client.room.isMulodrome:
                for player in self.client.room.clients.copy().values():
                    player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == self.client.playerName else 0)
        
        @self.command(alies=["temps"], level=1)
        async def time(self):
            self.client.playerTime += abs(Utils.getSecondsDiff(self.client.loginTime))
            self.client.loginTime = Utils.getTime()
            temps = map(int, [self.client.playerTime // 86400, self.client.playerTime // 3600 % 24, self.client.playerTime // 60 % 60, self.client.playerTime % 60])
            self.client.sendLangueMessage("", "$TempsDeJeu", *temps)
        
        @self.command
        async def tutorial(self):
            self.client.enterRoom("\x03[Tutorial] %s" %(self.client.playerName))
            
        @self.command(level=1)
        async def facebook(self):
            self.client.sendPacket(Identifiers.old.send.Facebook_URL, [""])
            self.client.shopCheeses += 20
        
        
        
# Tribe commands
        @self.command(level=1,tribe=2046, args=1)
        async def inv(self, playerName):
            if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                player = self.server.players.get(playerName)
                player.invitedTribeHouses.append(self.client.tribeName)
                player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                self.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>"+player.playerName+"</V>")
        
        @self.command(level=1,tribe=2046, args=1)
        async def invkick(self, playerName):
            if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                player = self.server.players.get(playerName)
                if self.client.tribeName in player.invitedTribeHouses:
                    player.invitedTribeHouses.remove(self.client.tribeName)
                    self.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                    player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + self.client.playerName + "</V>")
                    if player.roomName == "*" + chr(3) + self.client.tribeName:
                        player.enterRoom(self.server.recommendRoom(self.client.langue))

        @self.command(level=1,tribe=2046)
        async def neige(self):
            if self.client.room.isSnowing:
                self.client.room.startSnow(0, 0, not self.client.room.isSnowing)
                self.client.room.isSnowing = False
            else:
                self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)
                self.client.room.isSnowing = True

        @self.command(level=1,tribe=2046, args=1)
        async def module(self, moduleid):
            if moduleid == "":
                self.client.sendClientMessage("Module list:", 1)
                for key in self.server.officialminigames:
                    self.client.sendMessage(f"<VP>#{key}</VP> : {self.client.room.getPlayersCountbyRoom('#'+key)}")
            elif moduleid[:1] == "stop":
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.stopModule()
            else:
                module = self.server.minigames.get(moduleid[:1])
                if module != None:
                    self.client.room.luaRuntime = Lua(self.client.room, self.server)
                    self.client.room.luaRuntime.owner = self.client.playerName
                    self.client.room.luaRuntime.RunCode(module)





        @self.command(level=5, roomOwner=True,tribe=2046,args=1)
        async def npp(self, code):
            if self.client.room.isVotingMode:
                return
            if code.startswith("@"):
                if len(code[1:]) < 1 or not code[1:].isdigit():
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                mapInfo = await self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == None:
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                self.client.room.forceNextMap = code
                self.client.sendLangueMessage("", f"$ProchaineCarte {code}")
            elif code.isdigit():
                self.client.room.forceNextMap = f"{code}"
                self.client.sendLangueMessage("", f"$ProchaineCarte {code}")
        @self.command(level=5, roomOwner=True,tribe=2046)
        async def np(self, code=''):
            if self.currentArgsCount == 0:
                await self.client.room.mapChange()
                return

            if self.client.room.isVotingMode:
                return

            if code.startswith("@"):
                if len(code[1:]) < 1 or not code[1:].isdigit():
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                mapInfo = await self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == None:
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return

                self.client.room.forceNextMap = code
                if self.client.room.changeMapTimer != None:
                    try:self.client.room.changeMapTimer.cancel()
                    except:self.client.room.changeMapTimer = None
                await self.client.room.mapChange()

            elif code.isdigit():
                self.client.room.forceNextMap = f"{code}"
                if self.client.room.changeMapTimer != None:
                    try:self.client.room.changeMapTimer.cancel()
                    except:self.client.room.changeMapTimer = None
                await self.client.room.mapChange()

# Arbitre Commands    
        @self.command(level=7, arb=True, args=1)
        async def ninja(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                if self.server.players[player.playerName].followed == None:
                    if player.playerName != self.client.playerName:
                        roomName = player.room.name
                        if not roomName == "" and not roomName == self.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            self.client.isHidden = True
                            self.client.sendPlayerDisconnect()
                            self.client.isDead = True
                            self.client.enterRoom(roomName)
                            self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(player.playerName).writeBoolean(True).toByteArray())
                            self.server.players[player.playerName].followed = self.client
                            self.client.sendServerMessage(self.client.playerName+ " has ninja'd the player "+player.playerName)
                else:
                    self.client.isHidden = False
                    self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF("").writeBoolean(False).toByteArray())
                    self.client.enterRoom(self.client.lastroom)
                    self.server.players[player.playerName].followed == None
            else:
                self.client.playerException.Invoke("unknownuser")
    
        @self.command(alies=['deban'], level=7, arb=True, args=1)
        async def unban(self, playerName):
            result = self.server.checkBanUser(playerName)
            if result == 1:
                self.server.removeTempBan(playerName)
                if playerName in self.server.reports:
                    self.server.reports[playerName]['bannedby'] = ""
                    self.server.reports[playerName]['banhours'] = 0
                    self.server.reports[playerName]['banreason'] = ""
                    self.server.reports[playerName]['state'] = "disconnected"
                self.client.sendClientMessage(f"The player {playerName} got unbanned.", 1)
                self.client.sendServerMessageOthers(f"{self.client.playerName} unbanned the player {playerName}.")
                self.server.saveCasier(playerName, "UNBAN", self.client.playerName, "", "")
            elif result == -1:
                self.client.playerException.Invoke("usernotbanned", playerName)
            else:
                self.client.playerException.Invoke("unknownuser")
    
        @self.command(level=7, arb=True, args=1)
        async def mute(self, playerName):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.playerException.Invoke("useralreadymuted", playerName)
                else:
                    time = args[1] if (len(args) >= 2) else ""
                    reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 9999999 if (hours > 9999999) else hours
                    self.server.mutePlayer(playerName, hours, reason, self.client.playerName, True, False)
                    self.client.sendClientMessage(f"The player {playerName} got muted", 1)
            else:
                self.client.playerException.Invoke("unknownuser")
                
        @self.command(level=7, arb=True, args=1)
        async def imute(self, playerName):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.playerException.Invoke("useralreadymuted", playerName)
                else:
                    time = args[1] if (len(args) >= 2) else ""
                    reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 9999999 if (hours > 9999999) else hours
                    self.server.mutePlayer(playerName, hours, reason, self.client.playerName, True, True)
                    self.client.sendClientMessage(f"The player {playerName} got muted", 1)
            else:
                self.client.playerException.Invoke("unknownuser")
    
        @self.command(alies=['demute'], level=7, arb=True, args=1)
        async def unmute(self, playerName):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.sendServerMessageOthers(f"{self.client.playerName} unmuted the player {playerName}.")
                    self.client.sendClientMessage(f"The player {playerName} got unmuted.", 1)
                    self.server.removeModMute(playerName)
                    self.client.isMute = False
                    self.server.saveCasier(playerName, "UNMUTE", self.client.playerName, "", "")
                    if playerName in self.server.reports:
                        self.server.reports[playerName]['isMuted'] = False
                        self.server.reports[playerName]['muteHours'] = 0
                        self.server.reports[playerName]['muteReason'] = ""
                        self.server.reports[playerName]['mutedBy'] = ""
                else:
                    self.client.playerException.Invoke("usernotmuted")
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def nomip(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                ipList=playerName+"'s last known IP addresses:"
                for rs in self.Cursor['loginlogs'].find({'Username':playerName}):
                    ipList += "<br>" + rs['Ip']
                self.client.sendClientMessage(ipList, 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        
        @self.command(level=7, arb=True, args=1)
        async def ipnom(self, ipAddress):
            List = "Logs for the IP address ["+ipAddress+"]:"
            for rs in self.Cursor['loginlogs'].find({'Ip':ipAddress}):
                if self.server.checkConnectedAccount(rs['Username']):
                    List += "<br>" + rs['Username'] + " <G>(online)</G>"
                else:
                    List += "<br>" + rs['Username']
            self.client.sendClientMessage(List, 1)

        @self.command(level=7, arb=True)
        async def lsc(self):
            result = {}
            for room in self.server.rooms.values():
                if room.community in result:
                    result[room.community] = result[room.community] + room.getSourisCount()
                else:
                    result[room.community] = room.getSourisCount()
            message = ""
            for community in result.items():
                if community[1] > 0:
                    message += "<BL>%s:<BL> <V>%s</V>\n" %(community[0].upper(), community[1])
            message += "<J>Total players:</J> <R>%s</R>" %(sum(result.values()))
            self.client.sendLogMessage(message)

        @self.command(level=7, arb=True)
        async def lsmodo(self):
            Moderateurs = ""
            for player in self.server.players.copy().values():
                if player.privLevel == 8:
                    Moderateurs += "<font color='#C565FE'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if Moderateurs != "":
                self.client.sendMessage(Moderateurs.rstrip("\n"))
            else:
                self.client.sendClientMessage("Don't have any online Moderators at moment.", 1)

        @self.command(level=7, arb=True)
        async def lsarb(self):
            Arbitres = ""
            for player in self.server.players.copy().values():
                if player.isArbitre or player.privLevel == 7:
                    Arbitres += "<font color='#B993CA'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if Arbitres != "":
                self.client.sendMessage(Arbitres.rstrip("\n"))
            else:
                self.client.sendClientMessage("Don't have any online Arbitres at moment.", 1)

        @self.command(level=7, arb=True)
        async def closeroom(self, roomName=''):
            if roomName != '':
                try:
                    for client in [*self.server.rooms[roomName].clients.values()]:
                        client.enterRoom('1')
                    self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                    self.client.sendClientMessage(f"The room {roomName} got closed.", 1)
                except KeyError:
                    self.client.sendClientMessage("The room [<J>"+roomName+"</J>] doesn't exists.", 1)
            else:
                roomName = self.client.room.name
                for player in [*self.client.room.clients.copy().values()]:
                    player.enterRoom('1')
                self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                self.client.sendClientMessage(f"The room {roomName} got closed.", 1)

        @self.command(alies=['desbanip'], level=7, args=1, arb=True)
        async def unbanip(self, ipAddress):
            decip = Utils.DecodeIP(ip)
            if decip in self.server.IPPermaBanCache:
                self.server.IPPermaBanCache.remove(decip)
                self.Cursor['ippermaban'].delete({'Ip':decip})
                self.client.sendServerMessageOthers(f"{self.client.playerName} unbanned the ip address {ip}.")
                self.client.sendClientMessage(f"The ip address {ip} got unbanned.", 1)
            else:
                self.client.sendClientMessage("The IP isn't banned.", 1)

        @self.command(level=7, args=1, arb=True)
        async def prison(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                if player.isPrisoned:
                    player.isPrisoned = False
                    self.client.sendServerMessageOthers(f"{player.playerName} unprisoned by {self.client.playerName}.")
                    self.client.sendClientMessage(f"{player.playerName} got unprisoned.", 1)
                    player.enterRoom("1")
                else:
                    player.enterRoom("*Bad Girls")
                    player.isPrisoned = True
                    self.client.sendServerMessageOthers(f"{player.playerName} prisoned by {self.client.playerName}.")
                    self.client.sendClientMessage(f"{player.playerName} got prisoned.", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=1, arb=True)
        async def delrecord(self, mapCode):
            if self.server.checkRecordMap(mapCode):
                await self.client.room.CursorMaps.execute("update Maps set Time = ? and Player = ? and RecDate = ? where Code = ?", [0, "", 0, str(mapCode)])
                self.client.sendServerMessage("The map's record: @"+str(mapCode)+" was removed by <BV>"+str(self.client.playerName)+"</BV>.")
            else:
                self.client.sendClientMessage("The map isn't have a record.")

        @self.command(level=7, args=1, arb=True)
        async def mumute(self, playerName):
            if self.server.checkConnectedAccount(playerName):
                self.server.sendMumute(playerName, self.client.playerName)
                self.client.sendClientMessage(""+ playerName + " got mumuted.", 1)

        @self.command(level=7, args=1, arb=True)
        async def find(self, text):
            result = ""
            for player in self.server.players.copy().values():
                if player.playerName.startswith(text):
                    result += "<BV>%s</BV> -> %s\n" %(player.playerName, player.room.name)
            result = result.rstrip("\n")
            self.client.sendClientMessage(result, 1) if result != "" else self.client.sendClientMessage("No results were found.", 1)

        @self.command(alies=['clearvotebans'], level=7, args=1, arb=True)
        async def clearban(self, playerName):
            if self.server.checkConnectedAccount(playerName):
                player = self.server.players.get(playerName)
                if player != None:
                    player.voteBan = []
                    self.client.sendServerMessageOthers(f"{self.client.playerName} removed all ban votes of {playerName}.")
                    self.client.sendClientMessage(f"Successfully removed all ban votes of {playerName}", 1)
                else:
                     self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=1, arb=True)
        async def ip(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                self.client.sendClientMessage(f"<BV>{playerName}</BV> -> {Utils.EncodeIP(player.ipAddress)} ({player.ipCountry})", 1)
            else:
                self.client.playerException.Invoke("unknownuser")
        
        @self.command(level=7, args=1, arb=True)
        async def kick(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                player.room.removeClient(player)
                player.transport.close()
                self.client.sendServerMessageOthers("The player {playerName} has been kicked by {self.client.playerName}.")
                self.client.sendClientMessage(f"The player {playerName} got kicked", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(alies=["room*", "salon*", "sala*"], level=7, args=1, arb=True)
        async def commu(self, community):
            community = community[0:2].upper()
            try:
                self.client.langue = community
                self.client.langueID = Langues.getLangues().index(community)
                self.client.enterRoom(community if command != "commu" else self.server.recommendRoom(community))
            except:
                self.client.sendClientMessage(f"The community {community} is invalid.", 1)
                
        @self.command(level=7, args=1, arb=True)
        async def roomkick(self, playerName):
            if player != None:
                self.client.sendServerMessageOthers(f" {player.playerName} has been roomkicked from [{str.lower(player.room.name)}] by {self.client.playerName}.")
                self.client.sendClientMessage(f"{player.playerName} got kicked from the room.", 1)
                player.startBulle(self.server.recommendRoom(player.langue))
            else:
                self.client.playerException.Invoke("unknownuser")
                        
        @self.command(alies=['join'], level=7, args=1, arb=True)
        async def follow(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                self.client.enterRoom(player.roomName)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=1, arb=True)
        async def chatlog(self, playerName):
            self.client.modoPwet.openChatLog(playerName)

        @self.command(level=7)
        async def creator(self):
            self.client.sendClientMessage("Room [<J>"+self.client.room.name+"</J>]'s creator: <BV>"+self.client.room.roomCreator+"</BV>", 1)


# Modo Commands

        @self.command(level=8)
        async def clearchat(self):
            self.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 10000).toByteArray())

        @self.command(level=8, args=2)
        async def moveplayer(self, playerName, roomName):
            player = self.server.players.get(playerName)
            if player != None:
                newRoom = player.room.name
                player.startBulle(roomName)
                self.client.sendServerMessageOthers(f"{player.playerName} has been moved from ({str.lower(newRoom)}) to ({str.lower(player.room.name)}) by {self.client.playerName}.")
                self.client.sendClientMessage(f"{player.playerName} has been moved from {str.lower(newRoom)} to {str.lower(player.room.name)} ", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

# Admin Commands
        @self.command(level=9)
        async def move(self, roomName):
            for player in [*self.client.room.clients.copy().values()]:
                player.enterRoom(self.argsNotSplited)

        @self.command(level=9)
        async def updatesql(self):
            self.server.updateServer()
            self.client.sendServerMessageAdminOthers(f"The database was updated by {self.client.playerName}.")
            self.client.sendClientMessage("The database got updated.", 1)

        @self.command(alies=['re', 'revive'], level=9, args=1)
        async def respawn(self, playerName):
            if playerName in self.client.room.clients:
                self.client.room.respawnSpecific(playerName)
                self.client.sendClientMessage(f"Successfull respawned {playerName}.", 1)

        @self.command(alies=['setroundtime'], level=9, args=1)
        async def settime(self, time):
            time = int(time)
            time = 5 if time < 1 else (32767 if time > 32767 else time)
            for player in self.client.room.clients.copy().values():
                player.sendRoundTime(time)
            self.client.room.changeMapTimers(time)
            self.client.sendClientMessage(f"Successfull added {time} seconds to current round.", 1)

        @self.command(alies=['removepermmap', 'harddel'], level=9, args=1)
        async def removemap(self, mapCode=''):
            if mapCode == '':
                mapCode = self.client.room.mapCode
            mapCode = mapCode.replace('@', '')
            await self.client.room.CursorMaps.execute("delete from Maps where Code = ?", [mapCode])
            self.client.sendClientMessage(f"Successfull deleted the map: @{mapCode} from database.", 1)
        
        @self.command(level=9, args=3)
        async def addcode(self, name, type, amount):
            data = json.loads(open('./include/json/codes.json','r').read())
            if T == "fraises" or T == "cheeses":
                data['codes'].append({'name': name.upper(), 'type': T, 'amount': amount, 'havegot': 0})
                with open('./include/json/codes.json', 'w') as F:
                    json.dump(data, F)
                self.client.sendClientMessage(f"Successfull added a code {name}", 1)
            else:
                self.client.sendClientMessage("The type of code is invalid.", 1)
        
# Owner Commands
        @self.command(owner=True)
        async def reload(self):
            if self.client.playerName in self.owners:
                try:
                    await self.server.reloadServer()
                    self.client.sendClientMessage("Successfull reloaded all modules.", 1)
                except Exception as e:
                    self.client.sendClientMessage(f"Failed reload all modules. Error: {e}", 1)
        
        @self.command(owner=True)
        async def luaadmin(self):
            self.client.isLuaAdmin = not self.client.isLuaAdmin
            self.client.sendClientMessage("You can run lua programming as administrator." if self.client.isLuaAdmin else "You can't run lua programming as administrator.", 1)

        @self.command(owner=True)
        async def serverconfigs(self):
            with open("./include/configs.properties", 'r') as File:
                Log = File.read()
                File.close()
            self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

        @self.command(alies=['restart'], owner=True)
        async def reboot(self):
            self.server.sendServerRestart()
            
        @self.command(owner=True, args=1)
        async def deleteuser(self, playerName):
            if self.server.checkExistingUser(playerName):
                self.Cursor['users'].delete_one({'Username':playerName})
                self.client.sendServerMessageAdminOthers(f"The account {playerName} was deleted by {self.client.playerName}")
                self.client.sendClientMessage(f"The account {playerName} got deleted.", 1)
            else:
                self.client.playerException.Invoke("unknownuser")
                
        @self.command(owner=True, args=2)
        async def changepassword(self, playerName, newPassword):
            player = self.server.players.get(playerName)
            if player != None:
                salt = b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0'
                hashtext = base64.b64encode(hashlib.sha256(hashlib.sha256(newPassword.encode()).hexdigest().encode() + salt).digest()).decode()
                self.Cursor['users'].update_one({'Username':playerName},{'$set':{'Password': hashtext}})
                player.updateDatabase()
                player.room.removeClient(player)
                player.transport.close()
            else:
                self.client.playerException.Invoke("unknownuser")
                
        @self.command(owner=True)
        async def resetrecords(self):
            await self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
            self.client.sendServerMessageAdmin("All records of fastracing was deleted by %s."%(self.client.playerName))

        @self.command(owner=True, args=1)
        async def viewlog(self, log_type):
            if log_type == "errors":
                errors = ["Tribulle.log", "Commands.log", "Server.log"]
                for error in errors:
                    with open(f"./include/logs/Errors/{error}", 'r') as File:
                        Log = File.read()
                        File.close()
                    self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                    Log = ""
            elif log_type == "cache":
                message = ""
                for ip in self.server.IPPermaBanCache:
                    message += ip
                self.client.sendLogMessage(message)
                
            elif log_type == "iptemp":
                message = ""
                for ip in self.server.IPTempBanCache:
                    message += ip
                self.client.sendLogMessage(message)
                
            elif log_type == "debug":
                with open(f"./include/logs/Errors/Debug.log", 'r') as File:
                    Log = File.read()
                    File.close()
                self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                
            elif log_type == "promotions":
                message = ""
                for promotion in self.server.shopPromotions:
                    message += str(promotion) + ", "
                self.client.sendLogMessage(message[:-1])
                
            elif log_type == "shopoutfits":
                message = ""
                for promotion in self.server.shopOutfits:
                    message += str(promotion) + ", "
                self.client.sendLogMessage(message[:-1])

        @self.command(owner=True, args=1)
        async def clearlogs(self, type_log):
            if type_log == "reports":
                self.server.reports = {}
                self.client.sendServerMessageAdmin("The player %s cleared all reports from modopwet." %(self.client.playerName))
            elif type_log == "ippermacache":
                self.server.IPPermaBanCache = []
                self.client.sendServerMessageAdmin("The player %s clear the cache of the server." %(self.client.playerName))
            elif type_log == "iptempcache":
                self.server.IPTempBanCache = []
                self.client.sendServerMessageAdmin("The player %s cleared all IP bans." %(self.client.playerName))
            elif type_log == "banlog":
                Cursor['casierlog'].delete_many({})
                Cursor['ippermaban'].delete_many({})
                Cursor['usertempban'].delete_many({})
                self.client.sendServerMessageAdmin("The player %s cleared casier database." %(self.client.playerName))
            elif type_log == "loginlog":
                Cursor['loginlogs'].delete_many({})
                self.client.sendServerMessageAdmin("The player %s cleared loginlog database." %(self.client.playerName))
            elif type_log == "commandlog":
                Cursor['commandlog'].delete_many({})
                self.client.sendServerMessageAdmin("The player %s cleared commandlog database." %(self.client.playerName))

# Predefined Commands in swf.
        @self.command(level=1, args=1)
        async def codecadeau(self, code):
            for i in self.server.gameCodes['codes']:
                if code.upper() == i['name'] and i['havegot'] == 0:
                    r1 = i['type']
                    r2 = i["amount"]
                    if r1 == "cheeses":
                        self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(r2).writeInt(0).toByteArray())
                        self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0).writeInt(r2).toByteArray())
                        self.client.shopCheeses += r2
                        i['havegot'] = 1
                        break
                    elif r1 == "fraises":
                        self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(0).writeInt(r2).toByteArray())
                        self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(1).writeInt(r2).toByteArray())
                        self.client.shopFraises += r2
                        i['havegot'] = 1
                        break
                        
        @self.command(level=7, args=1)
        async def sonar(self, playerName, end=''):
            player = self.server.players.get(playerName)
            if player:
                self.client.sendPacket(Identifiers.send.Minibox_1, ByteArray().writeShort(200).writeUTF("Sonar "+playerName).writeUTF('\n'.join(self.server.sonar[playerName]) if playerName in self.server.sonar else "\n").toByteArray())
                self.server.sonar[playerName] = []
                if end == 'end':
                    if not int(time.time() - self.lastsonar) > 2: 
                        self.currentArgsCount = 1
                    self.lastsonar = time.time()
                if self.currentArgsCount == 1:
                    player.sendPacket(Identifiers.send.Init_Sonar, ByteArray().writeInt(8).writeBoolean(True).writeShort(1).toByteArray())
                else:
                    player.sendPacket(Identifiers.send.End_Sonar, ByteArray().writeInt(8).toByteArray())
                    
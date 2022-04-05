#coding: utf-8
import time, json, re

from lupa import LuaRuntime

from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

import asyncio

class Lua:
    def __init__(self, room, server):
        # Others
        self.room = room
        self.server = server
        # NoneType
        self.owner = None
        self.runtime = None
        # String
        self.name = ""
        self.script = ""
        self.roomFix = False
        # Dict
        self.RoomObjects = {}
        #List
        self.HiddenCommands = []
        # Integer
        self.LastRoomObjectID = 2000

    def SetupRuntimeGlobals(self):
        if self.runtime is None:
            return
        self.globals = self.runtime.globals()

        self.globals['io'] = None
        self.globals['dofile'] = None
        self.globals['module'] = None
        self.globals['require'] = None
        self.globals['loadfile'] = None
        self.globals['table']['foreach'] = self.tableForeach

        self.globals['os']['exit'] = None
        self.globals['os']['getenv'] = None
        self.globals['os']['remove'] = None
        self.globals['os']['rename'] = None
        self.globals['os']['execute'] = None
        self.globals['os']['setlocale'] = None
        self.globals['os']['time'] = lambda: int(time.time() * 1000)

        self.globals['print'] = self.sendLuaMessage

        self.globals['system'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['system']['bindKeyBoard'] = self.room.bindKeyBoard
        #self.globals['system']['bindKeyboard'] = self.room.bindKeyBoard
        self.globals['system']['disableChatCommandDisplay'] = self.disableChatCommandDisplay
        self.globals['system']['bindMouse'] = self.room.bindMouse
        #self.globals['system']['exit'] = 
        self.globals['system']['loadPlayerData'] = self.loadPlayerData
        self.globals['system']['savePlayerData'] = self.savePlayerData
        self.globals['system']['newTimer'] = self.newTimer
        self.globals['system']['addBot'] = self.addBot
        self.globals['system']['loadFile'] = None

        self.globals['ui'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['ui']['showColorPicker'] = self.room.showColorPicker
        self.globals['ui']['setMapName'] = self.setMapName
        self.globals['ui']['setShamanName'] = self.setShamanName
        
        self.globals['ui']['addTextArea'] = self.addTextArea
        self.globals['ui']['removeTextArea'] = self.removeTextArea
        self.globals['ui']['updateTextArea'] = self.updateTextArea
        self.globals['ui']['addPopup'] = self.addPopup
        self.globals['ui']['addLog'] = self.addLog

        self.globals['tfm'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['shamanObject'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['emote'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['exec'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['misc'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        
        self.globals['tfm']['enum']['shamanObject']['arrow'] = 0
        self.globals['tfm']['enum']['shamanObject']['littleBox'] = 1
        self.globals['tfm']['enum']['shamanObject']['box'] = 2
        self.globals['tfm']['enum']['shamanObject']['littleBoard'] = 3
        self.globals['tfm']['enum']['shamanObject']['board'] = 4
        self.globals['tfm']['enum']['shamanObject']['ball'] = 6
        self.globals['tfm']['enum']['shamanObject']['trampoline'] = 7
        self.globals['tfm']['enum']['shamanObject']['anvil'] = 10
        self.globals['tfm']['enum']['shamanObject']['cannon'] = 19
        self.globals['tfm']['enum']['shamanObject']['bomb'] = 23
        self.globals['tfm']['enum']['shamanObject']['balloon'] = 28
        self.globals['tfm']['enum']['shamanObject']['rune'] = 32
        self.globals['tfm']['enum']['shamanObject']['snowBall'] = 34
        self.globals['tfm']['enum']['shamanObject']['iceCube'] = 54
        
        self.globals['tfm']['enum']['emote']['dance'] = 0
        self.globals['tfm']['enum']['emote']['laugh'] = 1
        self.globals['tfm']['enum']['emote']['cry'] = 2
        self.globals['tfm']['enum']['emote']['kiss'] = 3
        self.globals['tfm']['enum']['emote']['angry'] = 4
        self.globals['tfm']['enum']['emote']['clap'] = 5
        self.globals['tfm']['enum']['emote']['sleep'] = 6
        self.globals['tfm']['enum']['emote']['facepaw'] = 7
        self.globals['tfm']['enum']['emote']['sit'] = 8
        self.globals['tfm']['enum']['emote']['confetti'] = 9
        
        self.globals['tfm']['exec']['chatMessage'] = self.chatMessage
        self.globals['tfm']['exec']['playerVictory'] = self.playerVictory
        self.globals['tfm']['exec']['addConjuration'] = self.addConjuration
        self.globals['tfm']['exec']['respawnPlayer'] = self.respawnPlayer
        self.globals['tfm']['exec']['removeCheese'] = self.removeCheese
        self.globals['tfm']['exec']['giveCheese'] = self.giveCheese
        self.globals['tfm']['exec']['giveMeep'] = self.giveMeep
        self.globals['tfm']['exec']['killPlayer'] = self.killPlayer
        self.globals['tfm']['exec']['displayParticle'] = self.displayParticle
        self.globals['tfm']['exec']['setGameTime'] = self.setGameTime
        self.globals['tfm']['exec']['bindKeyBoard'] = self.room.bindKeyBoard
        self.globals['tfm']['exec']['bindKeyboard'] = self.room.bindKeyBoard
        self.globals['tfm']['exec']['setShaman'] = self.setShaman
        self.globals['tfm']['exec']['setTransformationPlayer'] = self.setTransformationPlayer
        self.globals['tfm']['exec']['addShamanObject'] = self.addShamanObject
        self.globals['tfm']['exec']['removeObject'] = self.room.removeObject
        self.globals['tfm']['exec']['movePlayer'] = self.room.movePlayer
        self.globals['tfm']['exec']['bindMouse'] = self.room.bindMouse
        self.globals['tfm']['exec']['newGame'] = self.newGame
        self.globals['tfm']['exec']['moveCheese'] = self.moveCheese
        self.globals['tfm']['exec']['addTextArea'] = self.addTextArea
        self.globals['tfm']['exec']['removeTextArea'] = self.removeTextArea
        self.globals['tfm']['exec']['updateTextArea'] = self.updateTextArea
        self.globals['tfm']['exec']['addPopup'] = self.addPopup
        self.globals['tfm']['exec']['setUIMapName'] = self.setMapName
        self.globals['tfm']['exec']['setUIShamanName'] = self.setShamanName
        self.globals['tfm']['exec']['addImage'] = self.addImage
        self.globals['tfm']['exec']['removeImage'] = self.removeImage
        self.globals['tfm']['exec']['playEmote'] = self.playEmote
        self.globals['tfm']['exec']['giveConsumables'] = self.giveConsumables
        self.globals['tfm']['exec']['setRoomMaxPlayers'] = self.setRoomMaxPlayers
        self.globals['tfm']['exec']['setNameColor'] = self.room.setNameColor
        self.globals['tfm']['exec']['setPlayerScore'] = self.setPlayerScore
        self.globals['tfm']['exec']['addPhysicObject'] = self.room.addPhysicObject
        self.globals['tfm']['exec']['removePhysicObject'] = self.room.removeObject
        self.globals['tfm']['exec']['changePlayerSize'] = self.changePlayerSize

        self.globals['tfm']['exec']['disableAfkDeath'] = self.disableAfkDeath
        self.globals['tfm']['exec']['disableAllShamanSkills'] = self.disableAllShamanSkills
        self.globals['tfm']['exec']['disableAutoNewGame'] = self.disableAutoNewGame
        self.globals['tfm']['exec']['disableAutoScore'] = self.disableAutoScore
        self.globals['tfm']['exec']['disableAutoShaman'] = self.disableAutoShaman
        self.globals['tfm']['exec']['disableAutoTimeLeft'] = self.disableAutoTimeLeft
        self.globals['tfm']['exec']['disablePhysicalConsumables'] = self.disablePhysicalConsumables
        self.globals['tfm']['exec']['snow'] = self.snow
        self.globals['tfm']['exec']['setVampirePlayer'] = self.setVampirePlayer

        self.globals['tfm']['get']['misc']['apiVersion'] = "0.1"
        self.globals['tfm']['get']['misc']['transformiceVersion'] = self.server.Version

        self.globals['tfm']['get']['room']['objectList'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room']['xmlMapInfo'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room']['xmlMapInfo']['permCode'] = self.getPermCode
        self.globals['tfm']['get']['room']['xmlMapInfo']['author'] = self.getauthor
        self.globals['tfm']['get']['room']['xmlMapInfo']['mapCode'] = self.getmapCode
        self.globals['tfm']['get']['room']['xmlMapInfo']['xml'] = self.getxmlmap
        self.RefreshTFMGet()

    def UpdateObjectList(self, olist={}):
        self.RoomObjects = olist

    def RefreshTFMGet(self):
        self.globals['tfm']['get']['room']['name'] = self.room.name
        self.globals['tfm']['get']['room']['community'] = self.room.community
        self.globals['tfm']['get']['room']['currentMap'] = self.room.mapCode
        self.globals['tfm']['get']['room']['maxPlayers'] = self.room.maxPlayers
        self.globals['tfm']['get']['room']['mirroredMap'] = self.room.mapInverted
        self.globals['tfm']['get']['room']['passwordProtected'] = self.room.roomPassword != ""

        self.globals['tfm']['get']['room']['objectList'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room']['playerList'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')

        for object in self.RoomObjects.values():
            self.globals['tfm']['get']['room']['objectList'][object['id']] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
            self.globals['tfm']['get']['room']['objectList'][object['id']]['id'] = object['id']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['type'] = object['type']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['angle'] = object['angle']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['ghost'] = object['ghost']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['vx'] = object['velX']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['vy'] = object['velY']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['x'] = object['posX']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['y'] = object['posY']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['rotationSpeed'] = object['rotationSpeed']
            self.globals['tfm']['get']['room']['objectList'][object['id']]['stationary'] = object['stationary']

        for player in self.room.clients.values():
            self.globals['tfm']['get']['room']['playerList'][player.playerName] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["community"] = player.langue.lower()
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["hasCheese"] = player.hasCheese
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["id"] = player.playerID
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["shamanMode"] = player.shamanType
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["inHardMode"] = player.shamanType
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isDead"] = player.isDead
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isFacingRight"] = player.isMovingRight
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isJumping"] = player.isJumping
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isShaman"] = player.isShaman
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isVampire"] = player.isVampire
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["look"] = player.playerLook
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["movingLeft"] = player.isMovingLeft
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["movingRight"] = player.isMovingRight
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["playerName"] = player.playerName
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["registrationDate"] = player.regDate
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["score"] = player.playerScore
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["title"] = player.titleNumber
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["vx"] = player.velX
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["vy"] = player.velY
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["x"] = player.posX
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["y"] = player.posY

    def FixUnicodeError(self, text=u""):
        if isinstance(text, bytes):
            text = text.decode()
        return text

    def newTimer(self, callback, _time=0, loop=False, arg1=None, arg2=None, arg3=None, arg4=None):
        if loop:
            self.createLoop(_time, callback, arg1, arg2, arg3, arg4)
        else:
            self.server.loop.call_later(_time, callback, arg1, arg2, arg3, arg4)

    def createLoop(self, _time, callback, arg1=None, arg2=None, arg3=None, arg4=None):
        self.server.loop.call_later(0, callback, arg1, arg2, arg3, arg4)
        self.server.loop.call_later(_time, lambda: self.createLoop(_time, callback, arg1, arg2, arg3, arg4))

    def setPlayerScore(self, playerName, score, add = False):
        if add is None:
            add = False
        player = self.room.clients.get(playerName)
        if player:
            if add:
                player.playerScore += score
            else:
                player.playerScore = score
            self.room.sendAll(Identifiers.send.Set_Player_Score, ByteArray().writeInt(player.playerCode).writeShort(player.playerScore).toByteArray())

    def disablePhysicalConsumables(self, status):
        if status == True:
            self.room.disablePhysicalConsumables = True
        else:
            self.room.disablePhysicalConsumables = False
        
    def getPermCode(self):
        mapPerma = self.room.mapPerma
        return mapPerma
    
    def getauthor(self):
        mapName = self.room.mapName
        return mapName
    
    def getmapCode(self):
        mapCode = self.room.mapCode
        return mapCode
    
    def htmlfix(self, text):
        if "<a" in text:
            if not "</a>" in text:
                text = text + "</a>"
        if "<p" in text:
            if not "</p>" in text:
                text = text + "</p>"
        if "<font" in text:
            if not "</font>" in text:
                text = text + "</font>"
        return text
    
    def getxmlmap(self):
        mapXML = self.room.mapXML
        return mapXML
        
    def giveConsumables(self, playerName, consumableId, amount=1):
        player = self.room.clients.get(playerName)
        if player:
            player.sendGiveConsumables(consumableId, amount)

    def addLog(self, text, playerName):
        player = self.room.clients.get(playerName)
        if player != None:
            player.sendLogMessage(text)

    def chatMessage(self, message="", target=None):
        if target == "" or target is None:
            for player in self.room.clients.values():
                player.sendMessage(self.FixUnicodeError(message))
        else:
            player = self.room.clients.get(target)

            if player != None:
                player.sendMessage(self.FixUnicodeError(message))

    def setRoomMaxPlayers(self, maxPlayers):
        self.room.maxPlayers = maxPlayers
        
    def snow(self):
        self.room.startSnow(1000, 60, not self.room.isSnowing)
        
    def setVampirePlayer(self, playerName): #####
        player = self.room.clients.get(playerName)
        if player != None:
            player.sendVampireMode(False)
        
    def addConjuration(self, x, y, bl):
        self.room.sendAll(Identifiers.old.send.Add_Conjuration, [x, y, bl])
        self.server.loop.call_later(10, self.room.sendAll, Identifiers.old.send.Conjuration_Destroy, [int(x), int(y)])
        
    def changePlayerSize(self, name, size):
        size = float(size)
        size = 5.0 if size > 5.0 else size
        size = int(size * 100)
        playerName = Utils.parsePlayerName(name)
        if playerName == "*":
            for player in self.room.clients.copy().values():
                self.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())
        else:
            player = self.server.players.get(playerName)
            if player != None:
                self.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())

    def loadPlayerData(self, playerName):
        data = ""
        try:
            with open(f"./include/lua/playerDatas/{playerName}", "r") as f:
                data = f.read()
                if data == None:
                    data = ""
        except:
                data = ""
        self.emit("PlayerDataLoaded", (playerName, data))
        return data != ""
        
    def addBot(self, npcId, npcName, npcTitle, npcLook, npcPosX, npcPosY, starePlayer, shop="", x=""):
        client = self.room.clients.get(starePlayer)       
        if client != None:
            client.sendPacket(Identifiers.send.NPC, ByteArray().writeInt(npcId).writeUTF(npcName).writeShort(npcTitle).writeBoolean(starePlayer).writeUTF(npcLook).writeShort(npcPosX).writeShort(npcPosY).writeShort(1).writeByte(11).writeShort(0).toByteArray())

    def savePlayerData(self, playerName, data):
        if len(data) > 128000:
            return
        with open(f"./include/lua/playerDatas/{playerName}", "w") as f:
            f.write(data)

    def addImage(self, imageName = "", target = "", xPosition = 50, yPosition = 50, targetPlayer = ""):
        if imageName is None:
            imageName = ""
        if target is None:
            target = ""
        if xPosition is None:
            xPosition == 50
        if yPosition is None:
            yPosition = 50
        if targetPlayer is None:
            targetPlayer = ""
        packet = ByteArray()
        self.room.lastImageID += 1
        packet.writeInt(self.room.lastImageID)
        packet.writeUTF(imageName)
        packet.writeByte(1 if target.startswith("#") else 2 if target.startswith("$") else 3 if target.startswith("%") else 4 if target.startswith("?") else 5 if target.startswith("_") else 6 if target.startswith("!") else 7 if target.startswith("&") else 0)
        target = target[1:]
        packet.writeInt(int(target) if target.isdigit() else self.server.getPlayerCode(Utils.parsePlayerName(target)))
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        if targetPlayer == "":
            self.room.sendAll(Identifiers.send.Add_Image, packet.toByteArray())
        else:
            player = self.room.clients.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Add_Image, packet.toByteArray())

    def removeImage(self, imageId):
        self.room.sendAll(Identifiers.send.Add_Image, ByteArray().writeInt(imageId).toByteArray())

    def playEmote(self, playerName, emoteId, emoteArg = ""):
        if emoteArg is None:
            emoteArg = ""
        player = self.room.clients.get(playerName)
        if player:
            player.sendPlayerEmote(emoteId, emoteArg, False, True)

    def disableChatCommandDisplay(self, command="", hidden=True): ######
        if not command in self.HiddenCommands and hidden:
            self.HiddenCommands.append(self.FixUnicodeError(command))
        elif command in self.HiddenCommands and not hidden:
            self.HiddenCommands.remove(self.FixUnicodeError(command))

    def tableForeach(self, array, callback):
        for key, value in array.items():
            callback(key, value)

    def disableAfkDeath(self, status):
        if status == True:
            self.room.disableAfkKill = True
        else:
            self.room.disableAfkKill = False

    def disableAllShamanSkills(self, status):
        if status == True:
            self.room.noShamanSkills = True
        else:
            self.room.noShamanSkills = False

    def disableAutoNewGame(self, status):
        if status == True:
            self.room.isFixedMap = True
            self.roomFix = True
        else:
            self.room.isFixedMap = False
            self.roomFix = False
        
    def disableAutoScore(self, status):
        if status == True:
            self.room.noAutoScore = True
        else:
            self.room.noAutoScore = False

    def disableAutoShaman(self, status):
        if status == True:
            self.room.noShaman = True
        else:
            self.room.noShaman = False

    def disableAutoTimeLeft(self, status):
        if status == True:
            self.room.never20secTimer = True
        else:
            self.room.never20secTimer = False

    def addPopup(self, id, type, text, targetPlayer="", x=50, y=50, width=0, fixedPos=False):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(self.FixUnicodeError(text)).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = self.room.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())

    def updateTextArea(self, id, text, targetPlayer=""):
        p = ByteArray().writeInt(id).writeUTF(self.FixUnicodeError(text))
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = self.room.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())
    
    def displayParticle(self, particleType=0, xPosition=0, yPosition=0, xSpeed=0, ySpeed=0, xAcceleration=0, yAcceleration=0, targetPlayer=""):
        self.room.displayParticle(particleType, xPosition, yPosition, xSpeed, ySpeed, xAcceleration, yAcceleration, targetPlayer)

    def removeTextArea(self, id, targetPlayer=""):
        p = ByteArray().writeInt(id)
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            player = self.room.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def addTextArea(self, id, text, targetPlayer="", x=50, y=50, width=0, height=0, backgroundColor=0x324650, borderColor=0, backgroundAlpha=1, t=False, fixedPos=True, op=False):
        if backgroundAlpha:
            backgroundAlpha *= 100
        else:
            backgroundAlpha = 0
        if not targetPlayer:
            targetPlayer = ""
        if x is None:
            x = 50
        if y is None:
            y = 50
        if width is None:
            width = 0
        if height is None:
            height = 0
        if backgroundColor is None:
            backgroundColor = 0x324650
        if borderColor is None:
            borderColor = 0
        if backgroundAlpha is None:
            backgroundAlpha = 0
        if fixedPos is None:
            fixedPos = False

        p = ByteArray().writeInt(int(id))
        p.writeUTF(self.FixUnicodeError(text))
        p.writeShort(int(x)).writeShort(int(y))
        p.writeShort(int(width))
        p.writeShort(int(height))
        p.writeInt(int(backgroundColor))
        p.writeInt(int(borderColor))
        p.writeByte(int(100 if backgroundAlpha > 100 else backgroundAlpha))
        p.writeBoolean(fixedPos)
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            player = self.room.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def setTransformationPlayer(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Can_Transformation, 1)
            
    def setMapName(self, message=""):
        self.room.sendAll(Identifiers.send.Set_Map_Name, ByteArray().writeUTF(str(message)).toByteArray())
        
    def setShamanName(self, message=""):
        self.room.sendAll(Identifiers.send.Set_Shaman_Name, ByteArray().writeUTF(str(message)).toByteArray())

    def giveCheese(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead and not player.hasCheese:
            player.sendGiveCheese(0)

    def playerVictory(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)

        if player != None and not player.isDead:
            if not player.hasCheese:
                self.giveCheese(playerName)

            player.playerWin(1, 0)

    def respawnPlayer(self, target=""):
        playerName = Utils.parsePlayerName(target)
        if playerName in self.room.clients:
            self.room.respawnSpecific(playerName)

    def removeCheese(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead and player.hasCheese:
            player.hasCheese = False
            player.sendRemoveCheese()

    def giveMeep(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead:
            player.sendPacket(Identifiers.send.Can_Meep, 1)

    def killPlayer(self, target=""):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if not player.isDead:
            player.isDead = True
            if player.room.noAutoScore:
                player.playerScore += 1
            player.sendPlayerDied()
            player.room.checkChangeMap()

    def setGameTime(self, time=0, add=False):
        if add is None:
            add = False
        if str(time).isdigit():
            if add:
                iTime = self.room.roundTime + (self.room.gameStartTime - Utils.getTime()) + self.room.addTime + int(time)
            else:
                iTime = int(time)
            iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
            for player in self.room.clients.values():
                player.sendRoundTime(iTime)

            self.room.roundTime = iTime
            self.room.changeMapTimers(iTime)

    def setShaman(self, target=""):
        player = self.room.clients.get(Utils.parsePlayerName(target))
        if player != None:
            player.isShaman = True
            self.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeByte(player.shamanType).writeShort(player.shamanLevel).writeShort(player.Skills.getShamanBadge()).toByteArray())

    def moveCheese(self, x=0, y=0):
        self.room.sendAll(Identifiers.old.send.Move_Cheese, [x, y])

    def addShamanObject(self, type=0, x=0, y=0, angle=0, vx=0, vy=0, ghost=False):
        self.LastRoomObjectID += 1

        p = ByteArray()
        p.writeInt(self.LastRoomObjectID)
        p.writeShort(type)
        p.writeShort(x)
        p.writeShort(y)
        p.writeShort(angle)
        p.writeByte(vx)
        p.writeByte(vy)
        p.writeByte(1 if not ghost else 0)
        p.writeByte(0)
        self.room.sendAll(Identifiers.send.Spawn_Object, p.toByteArray())

        return self.LastRoomObjectID

    def newGame(self, mapCode=None, mirroredMap=False):
        self.room.forceNextMap = mapCode
        self.room.mapInverted = mirroredMap

        self.room.changeMapTimers(0)
        self.room.canChangeMap = True
        if self.roomFix:
            self.room.isFixedMap = True
        if self.room.changeMapTimer != None:
            self.room.changeMapTimer.cancel()
        self.room.mapChange()
        if self.roomFix:
            self.room.isFixedMap = True
            
    def sendLuaMessage(self, *args):
        message = ""
        for x in args:
            message += (self.globals.tostring(x) if self.globals.type(x) != "userdata" else "userdata") + ("  " if len(args)>1 else "")
        if message != "" and not self.owner is None:
            self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] %s" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str(message)))

    def EventLoop(self):
        if not self.runtime is None:
            self.RefreshTFMGet()
            elapsed = (Utils.getTime() - self.room.gameStartTime) * 1000
            remaining = ((self.room.roundTime + self.room.addTime) - (Utils.getTime() - self.room.gameStartTime)) * 1000
            self.emit('Loop', (elapsed if elapsed >= 0 else 0, remaining if remaining >= 0 else 0))

            self.server.addCallLater(0.5, self.EventLoop)

    def emit(self, eventName="", args=()):
        if self.runtime is None:
            return

        self.RefreshTFMGet()
        if eventName == "NewGame":
            self.RoomObjects = {}

        if type(args) == tuple:
            args_strPack = ""

            for x in args:
                args_strPack += (str(x) if type(x) != str and type(x) != bool else '"%s"' % (x) if type(x) != bool else ("true" if x else "false")) + ","
        else:
            args_strPack = (str(args) if type(args) != str and type(args) != bool else '"%s"' % (args) if type(args) != bool else ("true" if args else "false")) + ","

        try:
            self.runtime.execute("if(event%s)then event%s(%s) end" % (str(eventName), str(eventName), args_strPack[:-1]))
        except Exception as error:
            if not self.owner is None:
                self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>]<R>%s</R>" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str(error)))

    def RunCode(self, code=""):
        for while_stmt in re.findall('while[\s+(].*[\s+)]do', code): #while loop
            id = int(time.time())
            code = code.replace(while_stmt, """
            local __while__%s = {
                time = os.time() +  0.4,
                callback = function(self)
                    if (os.time() - self.time >= 0) then
                        error("Lua destroyed: Runtime Too Long")
                    end 
                    
                    return (%s)
                end
            }
            while(__while__%s:callback())do""" % (id, while_stmt[5:-2], id))
    
        if self.runtime is None:
            self.runtime = LuaRuntime()
            self.SetupRuntimeGlobals()

        try:
            ts = time.time()
            self.runtime.execute(code)
            self.EventLoop()
            te = time.time() - ts

            if not self.owner is None:
                self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] Script loaded in <J>%.2f</J>s." % (self.owner.playerName, str(time.strftime("%H:%M:%S")), te))
                


            self.script = code
        except Exception as error:
            self.script = ""

            if not self.owner is None:
                self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>]<R>%s</R>" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str(error)))

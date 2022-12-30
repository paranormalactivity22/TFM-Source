#coding: utf-8
import time, json, re, asyncio, math, random
from lupa import LuaRuntime
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

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
        # Boolean
        self.roomFix = False
        self.running = True
        # Dict
        self.RoomObjects = {}
        self.loops = {}
        #List
        self.HiddenCommands = []
        self.imagesadd = []
        # Integer
        self.LastRoomObjectID = 2000
        self.lastloopid = 1
        self.lastnpc = 1
        self.maxData = 128000
    
    def FixUnicodeError(self, text=u""):
        if isinstance(text, bytes):
            text = text.decode()
        return text

    def Permissions(self):
        if self.owner is None: 
            return True
        if self.owner.isLuaCrew or self.owner.privLevel == 9 or self.owner.privLevel == 3 or self.owner.isLuaCrew:
            return True
        return False
    
    def Forbidden(self, function):
        self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] <BL>%s</BL>" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str("You're not allowed to use the function "+str(function))))

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

    def createLoop(self, _id, _time, callback):
        if not self.running: return
        self.server.loop.call_later(0, callback)
        d = self.server.loop.call_later(_time, lambda: self.createLoop(_id, _time, callback))
        if _id in self.loops:
            self.loops[_id] = d
        else:
            return d

    def tableForeach(self, array, callback):
        for key, value in array.items():
            callback(key, value)
               
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

            self.server.loop.call_later(0.5, self.EventLoop)

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
        self.globals['string']['rep'] = lambda t, x: str(t * int(x))
        self.globals['print'] = self.sendLuaMessage

        self.globals['math']['abs'] = abs
        self.globals['math']['acos'] = math.acos
        self.globals['math']['asin'] = math.asin
        self.globals['math']['atan'] = math.atan
        self.globals['math']['atan2'] = math.atan2
        self.globals['math']['ceil'] = math.ceil
        self.globals['math']['cos'] = math.cos
        self.globals['math']['cosh'] = math.cosh
        self.globals['math']['deg'] = math.degrees
        self.globals['math']['exp'] = math.exp
        self.globals['math']['floor'] = math.floor
        self.globals['math']['fmod'] = math.fmod
        self.globals['math']['frexp'] = math.frexp
        self.globals['math']['ldexp'] = math.ldexp
        self.globals['math']['log'] = math.log
        self.globals['math']['max'] = max
        self.globals['math']['min'] = min
        self.globals['math']['modf'] = math.modf
        self.globals['math']['pi'] = math.pi
        self.globals['math']['pow'] = math.pow
        self.globals['math']['rad'] = math.radians
        self.globals['math']['random'] = random.random
        self.globals['math']['randomseed'] = random.seed
        self.globals['math']['sin'] = math.sin
        self.globals['math']['sinh'] = math.sinh
        self.globals['math']['sqrt'] = math.sqrt
        self.globals['math']['tan'] = math.tan
        self.globals['math']['tanh'] = math.tanh

        self.globals['system'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['system']['bindKeyboard'] = self.room.bindKeyBoard
        self.globals['system']['bindMouse'] = self.room.bindMouse
        self.globals['system']['disableChatCommandDisplay'] = self.disableChatCommandDisplay
        self.globals['system']['exit'] = self.stopModule
        self.globals['system']['giveEventGift'] = self.giveEventGift
        self.globals['system']['loadFile'] = self.loadFile
        self.globals['system']['loadPlayerData'] = self.loadPlayerData
        self.globals['system']['newTimer'] = self.newTimer
        self.globals['system']['removeTimer'] = self.removeTimer
        self.globals['system']['saveFile'] = self.saveFile
        self.globals['system']['savePlayerData'] = self.savePlayerData

        self.globals['ui'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['ui']['addLog'] = self.addLog
        self.globals['ui']['addPopup'] = self.room.addPopup
        self.globals['ui']['addTextArea'] = self.room.addTextArea
        self.globals['ui']['removeTextArea'] = self.room.removeTextArea
        self.globals['ui']['setMapName'] = self.setMapName
        self.globals['ui']['setShamanName'] = self.setShamanName
        self.globals['ui']['showColorPicker'] = self.room.showColorPicker
        self.globals['ui']['updateTextArea'] = self.room.updateTextArea

        self.globals['tfm'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['shamanObject'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['emote'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['bonus'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['ground'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['enum']['particle'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['exec'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['misc'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        
        self.globals['tfm']['exec']['addBonus'] = self.addBonus
        self.globals['tfm']['exec']['addConjuration'] = self.addConjuration
        self.globals['tfm']['exec']['addImage'] = self.addImage
        self.globals['tfm']['exec']['addJoint'] = self.addJoint
        self.globals['tfm']['exec']['addPhysicObject'] = self.room.addPhysicObject
        self.globals['tfm']['exec']['addShamanObject'] = self.addShamanObject
        self.globals['tfm']['exec']['attachBalloon'] = self.attachBalloon
        self.globals['tfm']['exec']['bindKeyboard'] = self.room.bindKeyBoard
        self.globals['tfm']['exec']['changePlayerSize'] = self.changePlayerSize
        self.globals['tfm']['exec']['chatMessage'] = self.chatMessage
        self.globals['tfm']['exec']['disableAfkDeath'] = self.disableAfkDeath
        self.globals['tfm']['exec']['disableAllShamanSkills'] = self.disableAllShamanSkills
        self.globals['tfm']['exec']['disableAutoNewGame'] = self.disableAutoNewGame
        self.globals['tfm']['exec']['disableAutoScore'] = self.disableAutoScore
        self.globals['tfm']['exec']['disableAutoShaman'] = self.disableAutoShaman
        self.globals['tfm']['exec']['disableAutoTimeLeft'] = self.disableAutoTimeLeft
        self.globals['tfm']['exec']['disableMortCommand'] = self.disableMortCommand
        self.globals['tfm']['exec']['disablePhysicalConsumables'] = self.disablePhysicalConsumables
        self.globals['tfm']['exec']['displayParticle'] = self.displayParticle
        self.globals['tfm']['exec']['explosion'] = self.explosion
        self.globals['tfm']['exec']['freezePlayer'] = self.freezePlayer
        self.globals['tfm']['exec']['getPlayerSync'] = self.getPlayerSync
        self.globals['tfm']['exec']['giveCheese'] = self.giveCheese
        self.globals['tfm']['exec']['giveConsumables'] = self.giveConsumables
        self.globals['tfm']['exec']['giveMeep'] = self.giveMeep
        self.globals['tfm']['exec']['giveTransformations'] = self.giveTransformations
        self.globals['tfm']['exec']['killPlayer'] = self.killPlayer
        self.globals['tfm']['exec']['linkMice'] = self.linkMice
        self.globals['tfm']['exec']['lowerSyncDelay'] = self.lowerSyncDelay
        self.globals['tfm']['exec']['moveCheese'] = self.moveCheese
        self.globals['tfm']['exec']['moveObject'] = self.moveObject
        self.globals['tfm']['exec']['movePlayer'] = self.room.movePlayer
        self.globals['tfm']['exec']['newGame'] = self.newGame
        self.globals['tfm']['exec']['playEmote'] = self.playEmote
        self.globals['tfm']['exec']['playerVictory'] = self.playerVictory
        self.globals['tfm']['exec']['removeBonus'] = self.removeBonus
        self.globals['tfm']['exec']['removeCheese'] = self.removeCheese
        self.globals['tfm']['exec']['removeImage'] = self.removeImage #kkkkkk
        self.globals['tfm']['exec']['removeJoint'] = self.removeJoint
        self.globals['tfm']['exec']['removeObject'] = self.room.removeObject
        self.globals['tfm']['exec']['removePhysicObject'] = self.RemovePhysicObject
        self.globals['tfm']['exec']['respawnPlayer'] = self.respawnPlayer
        self.globals['tfm']['exec']['setAutoMapFlipMode'] = self.setAutoMapFlipMode
        self.globals['tfm']['exec']['setGameTime'] = self.setGameTime
        self.globals['tfm']['exec']['setNameColor'] = self.room.setNameColor
        self.globals['tfm']['exec']['setPlayerScore'] = self.setPlayerScore
        self.globals['tfm']['exec']['setPlayerSync'] = self.setPlayerSync
        self.globals['tfm']['exec']['setRoomMaxPlayers'] = self.setRoomMaxPlayers
        self.globals['tfm']['exec']['setRoomPassword'] = self.setRoomPassword
        self.globals['tfm']['exec']['setShaman'] = self.setShaman
        self.globals['tfm']['exec']['setUIMapName'] = self.setMapName
        self.globals['tfm']['exec']['setUIShamanName'] = self.setShamanName
        self.globals['tfm']['exec']['setVampirePlayer'] = self.setVampirePlayer
        self.globals['tfm']['exec']['setWorldGravity'] = self.setWorldGravity
        self.globals['tfm']['exec']['snow'] = self.snow

        self.globals['tfm']['get']['misc']['apiVersion'] = "0.28"
        self.globals['tfm']['get']['misc']['transformiceVersion'] = self.server.Version

        self.globals['tfm']['get']['room']['objectList'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room']['xmlMapInfo'] = self.runtime.eval('setmetatable({}, {__len = function(self) local count = 0;for i in next, self do count = count+1 end;return count;end})')
        self.globals['tfm']['get']['room']['xmlMapInfo']['permCode'] = self.getPermCode
        self.globals['tfm']['get']['room']['xmlMapInfo']['author'] = self.getauthor
        self.globals['tfm']['get']['room']['xmlMapInfo']['mapCode'] = self.getmapCode
        self.globals['tfm']['get']['room']['xmlMapInfo']['xml'] = self.getxmlmap
        
        #self.globals['debug']['disableEventLog'] = self.disableEventLog
        self.RefreshTFMGet()

    def RefreshTFMGet(self):
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
        self.globals['tfm']['enum']['shamanObject']['orangePortal'] = 26
        self.globals['tfm']['enum']['shamanObject']['blueBalloon'] = 28
        self.globals['tfm']['enum']['shamanObject']['redBalloon'] = 29
        self.globals['tfm']['enum']['shamanObject']['greenBalloon'] = 30
        self.globals['tfm']['enum']['shamanObject']['yellowBalloon'] = 31
        self.globals['tfm']['enum']['shamanObject']['rune'] = 32
        self.globals['tfm']['enum']['shamanObject']['chicken'] = 33
        self.globals['tfm']['enum']['shamanObject']['snowBall'] = 34
        self.globals['tfm']['enum']['shamanObject']['cupidonArrow'] = 35
        self.globals['tfm']['enum']['shamanObject']['apple'] = 39
        self.globals['tfm']['enum']['shamanObject']['sheep'] = 40
        self.globals['tfm']['enum']['shamanObject']['littleBoardIce'] = 45
        self.globals['tfm']['enum']['shamanObject']['littleBoardChocolate'] = 46
        self.globals['tfm']['enum']['shamanObject']['iceCube'] = 54
        self.globals['tfm']['enum']['shamanObject']['cloud'] = 57
        self.globals['tfm']['enum']['shamanObject']['bubble'] = 59
        self.globals['tfm']['enum']['shamanObject']['tinyBoard'] = 60
        self.globals['tfm']['enum']['shamanObject']['companionCube'] = 61
        self.globals['tfm']['enum']['shamanObject']['stableRune'] = 62
        self.globals['tfm']['enum']['shamanObject']['ballonFish'] = 65
        self.globals['tfm']['enum']['shamanObject']['longBoard'] = 67
        self.globals['tfm']['enum']['shamanObject']['triangle'] = 68
        self.globals['tfm']['enum']['shamanObject']['sBoard'] = 69
        self.globals['tfm']['enum']['shamanObject']['paperPlane'] = 80
        self.globals['tfm']['enum']['shamanObject']['rock'] = 85
        self.globals['tfm']['enum']['shamanObject']['pumpkinBall'] = 89
        self.globals['tfm']['enum']['shamanObject']['tombstone'] = 90
        self.globals['tfm']['enum']['shamanObject']['paperBall'] = 95
        
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
        self.globals['tfm']['enum']['emote']['flag'] = 10
        self.globals['tfm']['enum']['emote']['marshmallow'] = 11
        self.globals['tfm']['enum']['emote']['selfie'] = 12
        self.globals['tfm']['enum']['emote']['highfive'] = 13
        self.globals['tfm']['enum']['emote']['highfive_1'] = 14
        self.globals['tfm']['enum']['emote']['highfive_2'] = 15
        self.globals['tfm']['enum']['emote']['partyhorn'] = 16
        self.globals['tfm']['enum']['emote']['hug'] = 17
        self.globals['tfm']['enum']['emote']['hug_1'] = 18
        self.globals['tfm']['enum']['emote']['hug_2'] = 19
        self.globals['tfm']['enum']['emote']['jigglypuff'] = 20
        self.globals['tfm']['enum']['emote']['kissing'] = 21
        self.globals['tfm']['enum']['emote']['kissing_1'] = 22
        self.globals['tfm']['enum']['emote']['kissing_2'] = 23
        self.globals['tfm']['enum']['emote']['carnaval'] = 24
        self.globals['tfm']['enum']['emote']['rockpaperscissors'] = 25
        self.globals['tfm']['enum']['emote']['rockpaperscissors_1'] = 26
        self.globals['tfm']['enum']['emote']['rockpaperscissor_2'] = 27
        
        self.globals['tfm']['enum']['bonus']['point'] = 0
        self.globals['tfm']['enum']['bonus']['speed'] = 1
        self.globals['tfm']['enum']['bonus']['death'] = 2
        self.globals['tfm']['enum']['bonus']['spring'] = 3
        self.globals['tfm']['enum']['bonus']['booster'] = 5
        self.globals['tfm']['enum']['bonus']['electricArc'] = 6
        
        self.globals['tfm']['enum']['ground']['wood'] = 0
        self.globals['tfm']['enum']['ground']['ice'] = 1
        self.globals['tfm']['enum']['ground']['trampoline'] = 2
        self.globals['tfm']['enum']['ground']['lava'] = 3
        self.globals['tfm']['enum']['ground']['chocolate'] = 4
        self.globals['tfm']['enum']['ground']['earth'] = 5
        self.globals['tfm']['enum']['ground']['grass'] = 6
        self.globals['tfm']['enum']['ground']['sand'] = 7
        self.globals['tfm']['enum']['ground']['cloud'] = 8
        self.globals['tfm']['enum']['ground']['water'] = 9
        self.globals['tfm']['enum']['ground']['stone'] = 10
        self.globals['tfm']['enum']['ground']['snow'] = 11
        self.globals['tfm']['enum']['ground']['rectangle'] = 12
        self.globals['tfm']['enum']['ground']['circle'] = 13
        self.globals['tfm']['enum']['ground']['invisible'] = 14
        self.globals['tfm']['enum']['ground']['web'] = 15
        self.globals['tfm']['enum']['ground']['yellowGrass'] = 17
        self.globals['tfm']['enum']['ground']['pinkGrass'] = 18
        self.globals['tfm']['enum']['ground']['acid'] = 19
        
        self.globals['tfm']['enum']['particle']['whiteGlitter'] = 0
        self.globals['tfm']['enum']['particle']['blueGlitter'] = 1
        self.globals['tfm']['enum']['particle']['orangeGlitter'] = 2
        self.globals['tfm']['enum']['particle']['cloud'] = 3
        self.globals['tfm']['enum']['particle']['dullWhiteGlitter'] = 4
        self.globals['tfm']['enum']['particle']['heart'] = 5
        self.globals['tfm']['enum']['particle']['bubble'] = 6
        self.globals['tfm']['enum']['particle']['tealGlitter'] = 9
        self.globals['tfm']['enum']['particle']['spirit'] = 10
        self.globals['tfm']['enum']['particle']['yellowGlitter'] = 11
        self.globals['tfm']['enum']['particle']['ghostSpirit'] = 12
        self.globals['tfm']['enum']['particle']['redGlitter'] = 13
        self.globals['tfm']['enum']['particle']['waterBubble'] = 14
        self.globals['tfm']['enum']['particle']['plus1'] = 15
        self.globals['tfm']['enum']['particle']['plus10'] = 16
        self.globals['tfm']['enum']['particle']['plus12'] = 17
        self.globals['tfm']['enum']['particle']['plus14'] = 18
        self.globals['tfm']['enum']['particle']['plus16'] = 19
        self.globals['tfm']['enum']['particle']['meep'] = 20
        self.globals['tfm']['enum']['particle']['redConfetti'] = 21
        self.globals['tfm']['enum']['particle']['greenConfetti'] = 22
        self.globals['tfm']['enum']['particle']['blueConfetti'] = 23
        self.globals['tfm']['enum']['particle']['yellowConfetti'] = 24
        self.globals['tfm']['enum']['particle']['diagonalRain'] = 25
        self.globals['tfm']['enum']['particle']['curlyWind'] = 26
        self.globals['tfm']['enum']['particle']['wind'] = 27
        self.globals['tfm']['enum']['particle']['rain'] = 28
        self.globals['tfm']['enum']['particle']['star'] = 29
        self.globals['tfm']['enum']['particle']['littleRedHeart'] = 30
        self.globals['tfm']['enum']['particle']['littlePinkHeart'] = 31
        self.globals['tfm']['enum']['particle']['daisy'] = 32
        self.globals['tfm']['enum']['particle']['bell'] = 33
        self.globals['tfm']['enum']['particle']['egg'] = 34
        self.globals['tfm']['enum']['particle']['projection'] = 35
        self.globals['tfm']['enum']['particle']['mouseTeleportation'] = 36
        self.globals['tfm']['enum']['particle']['shamanTeleportation'] = 37
        self.globals['tfm']['enum']['particle']['lollipopConfetti'] = 38
        self.globals['tfm']['enum']['particle']['yellowCandyConfetti'] = 39
        self.globals['tfm']['enum']['particle']['pinkCandyConfetti'] = 40
        
        self.globals['tfm']['get']['room']['name'] = self.room.name
        self.globals['tfm']['get']['room']['community'] = self.room.community
        self.globals['tfm']['get']['room']['language'] = self.room.community
        self.globals['tfm']['get']['room']['currentMap'] = self.room.mapCode
        self.globals['tfm']['get']['room']['maxPlayers'] = self.room.maxPlayers
        self.globals['tfm']['get']['room']['mirroredMap'] = self.room.mapInverted
        self.globals['tfm']['get']['room']['uniquePlayers'] = len(self.room.clients)
        self.globals['tfm']['get']['room']['passwordProtected'] = self.room.roomPassword != ""
        self.globals['tfm']['get']['room']['isTribeHouse'] = self.room.isTribeHouse

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
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["isFacingRight"] = player.isFacingRight
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

            self.globals['tfm']['get']['room']['playerList'][player.playerName]["tribeName"] = player.tribeName
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["vx"] = player.velX
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["vy"] = player.velY
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["x"] = player.posX
            self.globals['tfm']['get']['room']['playerList'][player.playerName]["y"] = player.posY


    ### system. Functions
    def disableChatCommandDisplay(self, command="", hidden=True):
        if not command in self.HiddenCommands and hidden:
            self.HiddenCommands.append(self.FixUnicodeError(command))
        elif command in self.HiddenCommands and not hidden:
            self.HiddenCommands.remove(self.FixUnicodeError(command))

    def loadFile(self, id):
        if self.Permissions() == True:
            data = ""
            try:
                with open(f"./include/lua/playerDatas/module-team/{self.owner.playerName}/{id}", "r") as f:
                    data = f.read()
                    if data == None:
                        data = ""
            except:
                data = ""
            self.emit("FileLoaded", (self.owner.playerName, data))
            return data != ""
        else:
            self.Forbidden("system.loadFile")

    def loadPlayerData(self, playerName):
        if self.Permissions() == True:
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
        else:
            self.Forbidden("system.loadPlayerData")
        
    def newTimer(self, callback, _time=0, loop=False, *args):
        _time = _time / 1000
        if loop:
            self.lastloopid+=1
            d = self.createLoop(self.lastloopid, _time, lambda: callback(*args))
            self.loops[self.lastloopid] = d
            return self.lastloopid
        else:
            self.lastloopid+=1
            d = self.server.loop.call_later(_time, lambda: callback(*args))
            self.loops[self.lastloopid] = d
            return self.lastloopid

    def removeTimer(self, _id):
        if self.Permissions() == True:
            _id = int(_id)
            if _id in self.loops:
                self.loops[_id].cancel()
                while _id in self.loops:
                    del self.loops[_id]
        else:
            self.Forbidden("system.removeTimer")

    def saveFile(self, data, id):
        if self.Permissions() == True:
            if len(data) > self.maxData:
                return
            try:
                with open(f"./include/lua/playerDatas/module-team/{self.owner.playerName}/{id}", "a+") as f:
                    f.write(data)
            except:
                import os
                os.mkdir(os.path.join("./include/lua/playerDatas/module-team/", self.owner.playerName), 0o6666)
                with open(f"./include/lua/playerDatas/module-team/{self.owner.playerName}/{id}", "a+") as f:
                    f.write(data)
            self.emit("FileSaved", (self.owner.playerName, data))
        else:
            self.Forbidden("system.saveFile")

    def savePlayerData(self, playerName, data):
        if self.Permissions() == True:
            if len(data) > self.maxData:
                return
            with open(f"./include/lua/playerDatas/{playerName}", "a+") as f:
                f.write(data)
        else:
            self.Forbidden("system.savePlayerData")

    ### ui. Functions
    def addLog(self, text, playerName):
        if self.Permissions() == True:
            player = self.room.clients.get(playerName)
            if player != None:
                player.sendLogMessage(text)
        else:
            self.Forbidden("ui.addLog")

    def setMapName(self, message=""):
        self.room.sendAll(Identifiers.send.Set_Map_Name, ByteArray().writeUTF(str(message)).toByteArray())
        
    def setShamanName(self, message=""):
        self.room.sendAll(Identifiers.send.Set_Shaman_Name, ByteArray().writeUTF(str(message)).toByteArray())

    ### tfm.exec. Functions
    def addBonus(self, type=1, x=0, y=0, id=0, angle=0, visible=True, targetPlayer=""):
        p = ByteArray()
        p.writeShort(x)
        p.writeShort(y)
        p.writeByte(type)
        p.writeShort(angle)
        p.writeInt(id)
        p.writeBoolean(visible)
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll([5, 14], p.toByteArray())
        else:
            player = self.room.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([5, 14], p.toByteArray())

    def addConjuration(self, x, y, duration=10000):
        self.room.sendAll(Identifiers.old.send.Add_Conjuration, [x, y, duration])
        self.server.loop.call_later(duration / 1000, self.room.sendAll, Identifiers.old.send.Conjuration_Destroy, [int(x), int(y)])

    def addImage(self, imageName, target, xPosition = 50, yPosition = 50, targetPlayer = "", scaleX = 1, scaleY = 1, angle = 0, alpha = 1, AnchorX = 0, AnchorY = 0):
        packet = ByteArray()
        self.room.lastImageID += 1
        packet.writeInt(self.room.lastImageID)
        self.imagesadd.append(self.room.lastImageID)
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

    def addJoint(self, id, ground1, ground2, jointDefinition):
        pass
        #self.room.sendAll(Identifiers.send.Add_Joint, [id, ground1, ground2, jointDefinition])
        
        #self.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if "width" in bodyDef else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef else 0).writeBoolean(bool(bodyDef["foreground"]) if "foreground" in bodyDef else False).writeShort(int(bodyDef["friction"]) if "friction" in bodyDef else 0).writeShort(int(bodyDef["restitution"]) if "restitution" in bodyDef else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef else 0).writeBoolean("color" in bodyDef).writeInt(int(bodyDef["color"]) if "color" in bodyDef else 0).writeBoolean(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef else True).writeBoolean(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef else True).writeBoolean(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef else 0).writeShort(int(bodyDef["linearDamping"]) if "linearDamping" in bodyDef else 0).writeShort(int(bodyDef["angularDamping"]) if "angularDamping" in bodyDef else 0).writeBoolean(False).writeUTF("").writeBoolean(False).toByteArray())

    def addShamanObject(self, type=0, x=0, y=0, angle=0, vx=0, vy=0, ghost=False, options=[]):
        self.LastRoomObjectID += 1
        _id = self.LastRoomObjectID
        self.RoomObjects[_id] = {'id': _id, 'type': type, 'angle': angle, 'ghost': ghost, 'velX': vx, 'velY': vy, 'posX': x, 'posY': y, 'rotationSpeed':(vx+vy)/2, 'stationary': (vx == 0 and vy == 0)}
        self.RefreshTFMGet()
        p = ByteArray()
        p.writeInt(_id)
        p.writeShort(type)
        p.writeShort(x)
        p.writeShort(y)
        p.writeShort(angle)
        p.writeByte(vx)
        p.writeByte(vy)
        p.writeBoolean(not ghost)
        p.writeByte(0)
        self.room.sendAll(Identifiers.send.Spawn_Object, p.toByteArray())
        return _id

    def attachBalloon(self, playerName, isAttached=True, colorType=1, ghost=False, speed=1):
        colorType = 4 if colorType > 4 else 1 if colorType < 1 else colorType
        player = self.server.players.get(playerName)
        if player != None:
            p = self.room.objectID + 1
            player.sendPlaceObject(p,28,player.posX,player.posY-25,0,0,0,not ghost,True,colorType)
            if isAttached:
                self.room.sendAll(Identifiers.send.SetPositionToAttach, ByteArray().writeByte(-1).toByteArray())
                self.room.sendAll(Identifiers.send.AttachPlayer, ByteArray().writeInt(player.playerCode).writeInt(p).writeInt(speed*1000).toByteArray())

    def changePlayerSize(self, name, size=1):
        size = float(size)
        size = 5.0 if size > 5.0 or size < 0.1 else size
        size = int(size * 100)
        playerName = Utils.parsePlayerName(name)
        if playerName == "*":
            for player in self.room.clients.copy().values():
                self.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())
        else:
            player = self.server.players.get(playerName)
            if player != None:
                self.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())

    def chatMessage(self, message, target=""):
        if self.Permissions() == True:
            if target == "":
                for player in self.room.clients.values():
                    player.sendMessage(self.FixUnicodeError(message))
            else:
                player = self.room.clients.get(target)

                if player != None:
                    player.sendMessage(self.FixUnicodeError(message))
        else:
            self.Forbidden("tfm.exec.chatMessage")

    def disableAfkDeath(self, status=True):
        self.room.disableAfkKill = status
        
    def disableAllShamanSkills(self, status=True):
        self.room.noShamanSkills = status

    def disableAutoNewGame(self, status=True):
        self.room.isFixedMap = status
        self.roomFix = status
        
    def disableAutoScore(self, status=True):
        self.room.noAutoScore = status

    def disableAutoShaman(self, status=True):
        self.room.noShaman = status

    def disableAutoTimeLeft(self, status=True):
        self.room.never20secTimer = status
    
    def disableMortCommand(self, status=False):
        self.room.disableMortCommand = status
        
    def disablePhysicalConsumables(self, status=False):
        self.room.disablePhysicalConsumables = status
    
    def displayParticle(self, particleType, xPosition, yPosition, xSpeed=0, ySpeed=0, xAcceleration=0, yAcceleration=0, targetPlayer=""):
        packet = ByteArray()
        packet.writeByte(particleType)
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        packet.writeShort(xSpeed)
        packet.writeShort(ySpeed)
        packet.writeShort(xAcceleration)
        packet.writeShort(yAcceleration)
        if targetPlayer == "":
            self.room.sendAll(Identifiers.send.Display_Particle, packet.toByteArray())
        else:
            player = self.server.players.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Display_Particle, packet.toByteArray())

    def explosion(self, x, y, power, distance, miceOnly=False):
        for player in self.server.players.values():
            player.sendPacket([5, 17], [int(x), int(y), int(power), int(distance), bool(miceOnly)])

    def freezePlayer(self, playerName, freeze=True, displayIce=True):
        player = self.room.clients.get(playerName)
        if player:
            player.sendPacket([100, 66], ByteArray().writeBoolean(freeze).writeBoolean(displayIce).toByteArray())

    def getPlayerSync(self):
        if self.Permissions() == True:
            self.chatMessage("Current Sync: "+self.room.currentSyncName, self.owner.playerName)
            return self.room.currentSyncName
        else:
            self.Forbidden("tfm.exec.getPlayerSync")

    def giveCheese(self, target):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead and not player.hasCheese:
            player.sendGiveCheese(0)

    def giveConsumables(self, playerName, consumableId, amount=1):
        if self.Permissions() == True:
            player = self.room.clients.get(playerName)
            if player:
                player.giveConsumable(consumableId, amount)
        else:
            self.Forbidden("tfm.exec.giveConsumables")

    def giveMeep(self, target, status=True):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead:
            player.sendPacket(Identifiers.send.Can_Meep, status)

    def giveTransformations(self, target, status=True):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None:
            if status == True:
                player.sendPacket([27, 10], 1)
                player.hasLuaTransformations = True
            else:
                player.sendPacket([27, 10], 0)
                player.hasLuaTransformations = False

    def killPlayer(self, target):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if not player.isDead:
            player.isDead = True
            if player.room.noAutoScore:
                player.playerScore += 1
            player.sendPlayerDied()
            player.room.checkChangeMap()

    def linkMice(self, Name, Target, status=True):
        player = self.server.players.get(Name)
        player1 = self.server.players.get(Target)
        if player != None and player1 != None:
            if status == True:
                self.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(status).writeInt(player.playerCode).writeInt(player1.playerCode).toByteArray())
            else:
                self.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(status).writeInt(player.playerCode).toByteArray())
            
    def lowerSyncDelay(self, playerName):
        if self.Permissions() == True:
            player = self.server.players.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Lower_Sync_Delay, [player.playerName])
        else:
            self.Forbidden("tfm.exec.lowerSyncDelay")

    def moveCheese(self, x, y):
        self.room.sendAll(Identifiers.old.send.Move_Cheese, [x, y])
            
    def moveObject(self, id, xy, vy, d=False, x=0, y=0, r=False, i=0, b=False):
        self.RoomObjects[id]['velX'] = x
        self.RoomObjects[id]['velY'] = y
        self.RoomObjects[id]['posX'] = xy
        self.RoomObjects[id]['posY'] = vy
        self.RoomObjects[id]['angle'] = i
        self.RefreshTFMGet()
        packet = ByteArray()
        packet.writeInt(id)
        packet.writeShort(xy)
        packet.writeShort(vy)
        packet.writeBoolean(d)
        packet.writeShort(x)
        packet.writeShort(y)
        packet.writeBoolean(r)
        packet.writeShort(i)
        packet.writeBoolean(b)
        self.room.sendAll(Identifiers.send.Move_Object, packet.toByteArray())

    def newGame(self, mapCode="", mirroredMap=False):
        self.room.forceNextMap = str(mapCode)
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

    def playEmote(self, playerName, emoteId, emoteArg=""):
        player = self.room.clients.get(playerName)
        if player:
            player.sendPlayerEmote(emoteId, emoteArg, False, True)

    def playerVictory(self, target):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)

        if player != None and not player.isDead:
            if not player.hasCheese:
                self.giveCheese(playerName)

            player.playerWin(1, 0)

    def removeBonus(self, id=0, targetPlayer=""):
        p = ByteArray().writeInt(id)
        if targetPlayer == "" or not targetPlayer:
            self.room.sendAll([5, 15], p.toByteArray())
        else:
            player = self.room.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([5, 15], p.toByteArray())
              
    def removeCheese(self, target):
        playerName = Utils.parsePlayerName(target)
        player = self.room.clients.get(playerName)
        if player != None and not player.isDead and player.hasCheese:
            player.hasCheese = False
            player.sendRemoveCheese()
              
    def removeImage(self, imageId):
        self.room.sendAll(Identifiers.send.Add_Image, ByteArray().writeInt(imageId).toByteArray())
        
    def removeJoint(self, id):
        self.room.sendAll(Identifiers.send.Remove_Joint, [id])
        
    def RemovePhysicObject(self, id):
        self.room.sendAll(Identifiers.send.Remove_Physic_Object, [id])

    def respawnPlayer(self, target):
        playerName = Utils.parsePlayerName(target)
        if playerName in self.room.clients:
            self.room.respawnSpecific(playerName)



    def setAutoMapFlipMode(self, status=False):
        self.room.autoMapFlipMode = status

    def setGameTime(self, time=0, add=False):
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

    def setPlayerScore(self, playerName, score, amount=False):
        if amount is None:
            amount = False
        player = self.room.clients.get(playerName)
        if player:
            if amount:
                player.playerScore += score
            else:
                player.playerScore = score
            self.room.sendAll(Identifiers.send.Set_Player_Score, ByteArray().writeInt(player.playerCode).writeShort(player.playerScore).toByteArray())

    def setPlayerSync(self, playerName):
        if self.Permissions() == True:
            player = self.room.clients.get(playerName)
            if player != None:
                player.isSync = True
                self.room.currentSyncCode = player.playerCode
                self.room.currentSyncName = player.playerName
                self.chatMessage("New Sync: "+str(player.playerName), self.owner.playerName)
        else:
            self.Forbidden("tfm.exec.setPlayerSync")

    def setRoomMaxPlayers(self, maxPlayers):
        if self.Permissions() == True:
            if maxPlayers > 0:
                self.room.maxPlayers = maxPlayers
        else:
            self.Forbidden("tfm.exec.setRoomMaxPlayers")

    def setRoomPassword(self, password):
        if self.Permissions() == True:
            if len(password) > 0:
                self.room.roomPassword = password
            else:
                self.room.roomPassword = ""
        else:
            self.Forbidden("tfm.exec.setRoomPassword")

    def setShaman(self, target):
        player = self.room.clients.get(Utils.parsePlayerName(target))
        if player != None:
            player.isShaman = True
            self.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeByte(player.shamanType).writeShort(player.shamanLevel).writeShort(player.Skills.getShamanBadge()).toByteArray())

    def setVampirePlayer(self, playerName, status=True):
        player = self.room.clients.get(playerName)
        if player != None:
            player.sendVampireMode(status)
            
    def setWorldGravity(self, x=0, y=10):
        for player in self.server.players.values():
            if x == 0:
                player.room.sendAll(Identifiers.old.send.Gravity, [0, y])
            elif y == 0:
                player.room.sendAll(Identifiers.old.send.Gravity, [x, 8])
            else:
                player.room.sendAll(Identifiers.old.send.Gravity, [x, y])
    
    def snow(self, time=60, power=10):
        self.room.startSnow(time, power, not self.room.isSnowing)
    
    ### Others
    
    def getPermCode(self):
        mapPerma = self.room.mapPerma
        return mapPerma
    
    def getauthor(self):
        mapName = self.room.mapName
        return mapName
    
    def getmapCode(self):
        mapCode = self.room.mapCode
        return mapCode
    
    def getxmlmap(self):
        mapXML = self.room.mapXML
        return mapXML
                        
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
            if (eventName == "FileLoaded" or eventName == "FileSaved" or eventName == "PlayerDataLoaded") and self.Permissions() == True:
                self.runtime.execute("if(event%s)then event%s(%s) end" % (str(eventName), str(eventName), args_strPack[:-1]))
            elif eventName != "FileLoaded" and eventName != "FileSaved" and eventName != "PlayerDataLoaded":
                self.runtime.execute("if(event%s)then event%s(%s) end" % (str(eventName), str(eventName), args_strPack[:-1]))
            else:
                Forbidden(str(eventName))
        except Exception as error:
            if not self.owner is None:
                self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] <BL>%s</BL>" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str(error)))
   
    def stopModule(self, playerName="", action=0):
        self.room.isMinigame = False
        self.room.minigame = None
        self.runtime = None
        self.running = False
        self.room.startSnow(0, 10, False)

        if self.room.isTribeHouse:
            self.room.countStats = False
            self.room.isTribeHouse = True
            self.room.autoRespawn = True
            self.room.never20secTimer = True
            self.room.noShaman = True
            self.room.disableAfkKill = True
            self.room.isFixedMap = True
            self.room.roundTime = 0

        if self.room.changeMapTimer != None:
            self.room.changeMapTimer.cancel()
        self.room.changeMapTimers(5)
        self.room.canChangeMap = True
        self.room.mapChange()

        if self.LastRoomObjectID > 2000:
            while self.LastRoomObjectID > 2000:
                self.room.removeObject(self.LastRoomObjectID)
                self.LastRoomObjectID -= 1

        for i in self.imagesadd:
            self.removeImage(i)

        for _id in self.loops:
            self.loops[_id].cancel()

        self.imagesadd = []
        self.loops = {}

        if playerName != "" and not self.room.minigame is None:
            if not self.room.minigame.owner is None:
                self.room.minigame.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] %s by: <J>%s</J>" % (playerName, str(time.strftime("%H:%M:%S")), "Module stopped" if action == 0 else "Another module was loaded", str(playerName)))

    def giveEventGift(self, playerName, gift=""):
        if self.Permissions() == True:
            pass
            
        else:
            self.Forbidden("system.giveEventGift")

    def RunCode(self, code=""):
        #if self.running:
            #self.stopModule()
         #for while_stmt in re.findall('while[\s+(].*[\s+)]do', code): #while loop
             #id = int(time.time())
             #code = code.replace(while_stmt, """
             #local __while__%s = {
                 #time = os.time() +  0.4,
                 #callback = function(self)
                     #if (os.time() - self.time >= 0) then
                         #error("Lua destroyed: Runtime Too Long")
                     #end 
                    #
                    # return (%s)
                # end
             #}
            # while(__while__%s:callback())do""" % (id, while_stmt[5:-2], id))
    
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
                self.owner.sendLuaMessage("[<V>%s.lua</V>][<N>%s</N>] <BL>%s</BL>" % (self.owner.playerName, str(time.strftime("%H:%M:%S")), str(error)))
#coding: utf-8
import re, json, random, urllib.request, time as _time, struct, asyncio, binascii, base64, zlib

loop = asyncio.get_event_loop()

# Game
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Lua import Lua
from collections import deque
from datetime import datetime

class Packets:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.data = {}
        self.packets = {}
        self.Cursor = player.Cursor
        self.isOpenedHelpCommand = False
        self.__init_2()
        
    def packet(self,func=None,args=[]):
        if not func: return lambda x: self.packet(x,args)
        else: 
            if func.__name__ in dir(Identifiers.recv):
                exec(f"self.ccc = Identifiers.recv.{func.__name__}")
                self.packets[self.ccc[0] << 8 | self.ccc[1]] = [args,func]

    async def parsePacket(self, packetID, C, CC, packet):
        ccc = C << 8 | CC
        args = []
        self.packet = packet
        if ccc in self.packets:
            for i in self.packets[ccc][0]:
                exec(f"self.value = self.packet.{i}()")
                args.append(self.value)
            await self.packets[ccc][1](self, *args)
            
            if (self.packet.bytesAvailable()):
                print("[%s] Struct Error - C: %s - CC: %s - packet: %s" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
                
        else:
            if self.server.isDebug:
                print("[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
                with open("./include/logs/Errors/Debug.log", "a") as f:
                    f.write("[%s] Packet not implemented - C: %s - CC: %s - packet: %s\n" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
                f.close()
                
    def __init_2(self):
        @self.packet
        async def Old_Protocol(self):
            data = self.packet.readUTFBytes(self.packet.readShort())
            if isinstance(data, (bytes, bytearray)):
                data = data.decode()
            await self.parsePacketUTF(data)
            
        @self.packet(args=['readInt'])
        async def Object_Sync(self, roundCode):
            if roundCode == self.client.room.lastRoundCode:
                p = ByteArray()
                while (self.packet.bytesAvailable()):
                    p.writeInt(self.packet.readInt())
                    code = self.packet.readShort()
                    p.writeShort(code)
                    if code != 1:
                        p.writeBytes(self.packet.readUTFBytes(18)).writeBoolean(True)
                self.client.room.sendAllOthers(self.client, Identifiers.send.Sync, p.toByteArray())


        @self.packet(args=['readInt', 'readBoolean', 'readBoolean', 'readInt', 'readInt', 'readShort', 'readShort', 'readBoolean', 'readShort'])
        async def Mouse_Movement(self, a, e, e2, posX, posY, velX, velY, jump, idk):
            packet2 = ByteArray().writeInt(self.client.playerCode).toByteArray() + ByteArray().writeInt(a).writeBoolean(e).writeBoolean(e2).writeInt(posX).writeInt(posY).writeShort(velX).writeShort(velY).writeBoolean(jump).writeShort(idk).toByteArray()
            if (e,e2) != (False,False):
                self.client.isFacingRight = self.client.isMovingRight = e
                self.client.isMovingLeft = e2
            else:
                self.client.isMovingRight = e
                self.client.isMovingLeft = e2
            if not self.client.posY == 0 and not self.client.posX == 0:
                lasty, lastx = self.client.posY, self.client.posX
            else:
                lasty, lastx = 0, 0
            self.client.posX, self.client.posY = posX * 800 // 2700, posY * 800 // 2700
            if not lasty == 0 and not lastx == 0:
                if not lasty == self.client.posY or not lastx == self.client.posX:
                    self.client.ResetAfkKillTimer()
                    if self.client.isAfk:
                        self.client.isAfk = False
            self.client.velX, self.client.velY, self.client.isJumping = velX, velY, jump
            self.client.room.sendAllOthers(self.client, Identifiers.send.Player_Movement, packet2)

 
        @self.packet(args=['readInt', 'readByte']) ####################
        async def Mort(self, roundCode, loc_1):
            if roundCode == self.client.room.lastRoundCode:
                self.client.isDead = True
                if not self.client.room.noAutoScore: self.client.playerScore += 1
                self.client.sendPlayerDied()

                if self.client.room.getPlayerCountUnique() >= self.server.needToFirst:
                    if self.client.room.isSurvivor:
                        for client in self.client.room.clients.copy().values():
                            if client.isShaman:
                                client.survivorDeath += 1
                                player.missions.upMission('3', 1)
                                if client.survivorDeath % 4 == 0:
                                    player.giveConsumable(2260, survivorDeath / 4, 0)
                                client.survivorDeath = 0

                if not self.client.room.currentShamanName == "":
                    player = self.client.room.clients.get(self.client.room.currentShamanName)

                    if player != None and not self.client.room.noShamanSkills:
                        if player.bubblesCount > 0:
                            if self.client.room.getAliveCount() != 1:
                                player.bubblesCount -= 1
                                self.client.sendPlaceObject(self.client.room.objectID + 2, 59, self.client.posX, 450, 0, 0, 0, True, True)

                        if player.desintegration:
                            self.client.Skills.sendSkillObject(6, self.client.posX, 395, 0)
                self.client.room.checkChangeMap()
    
        @self.packet(args=['readBoolean'])
        async def Player_Position(self, direction):
            self.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
            
        @self.packet(args=['readBoolean'])
        async def Shaman_Position(self, direction):
            self.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
    
        @self.packet(args=['readByte'])
        async def Crouch(self, crouch_type):
            self.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(self.client.playerCode).writeByte(crouch_type).writeByte(0).toByteArray())
    
    
        @self.packet(args=['readShort', 'readShort', 'readShort', 'readShort'])
        async def Map_26(self, posX, posY, width, height):
            if self.client.room.currentMap == 26:
                bodyDef = {}
                bodyDef["type"] = 12
                bodyDef["width"] = width
                bodyDef["height"] = height
                self.client.room.addPhysicObject(-1, posX, posY, bodyDef)
        
        @self.packet(args=['readByte', 'readShort', 'readShort'])
        async def Shaman_Message(self, type, x, y):
            self.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())

        @self.packet(args=['readInt'])
        async def Convert_Skill(self, objectID):
            self.client.Skills.sendConvertSkill(objectID)
        
        @self.packet(args=['readInt'])
        async def Demolition_Skill(self, objectID):
            self.client.Skills.sendDemolitionSkill(objectID)
        
        @self.packet(args=['readShort', 'readShort', 'readShort'])
        async def Projection_Skill(self, posX, posY, _dir):
            self.client.Skills.sendProjectionSkill(posX, posY, _dir)
            
        @self.packet(args=['readByte', 'readInt', 'readInt', 'readShort', 'readShort', 'readShort'])
        async def Enter_Hole(self, holeType, roundCode, monde, distance, holeX, holeY):
            if roundCode == self.client.room.lastRoundCode and (self.client.room.currentMap == -1 or monde == self.client.room.currentMap or self.client.room.EMapCode != 0):
                await self.client.playerWin(holeType, distance)
        
        @self.packet(args=['readInt', 'readShort', 'readShort', 'readShort'])
        async def Get_Cheese(self, roundCode, cheeseX, cheeseY, distance):
            if roundCode == self.client.room.lastRoundCode:
                self.client.sendGiveCheese(distance)
        
        @self.packet(args=['readByte', 'readInt', 'readShort', 'readShort', 'readShort', 'readShort', 'readByte', 'readByte', 'readBoolean', 'readBoolean'])
        async def Place_Object(self, roundCode, objectID, code, px, py, angle, vx, vy, dur, origin):
            if not self.client.isShaman:
                return
                
            if self.client.room.isTotemEditor:
                if self.client.tempTotem[0] < 20:
                    self.client.tempTotem[0] = int(self.client.tempTotem[0]) + 1
                    self.client.sendTotemItemCount(self.client.tempTotem[0])
                    self.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, int(dur)]))
            else:
                if code == 44:
                    if not self.client.useTotem:
                        self.client.sendTotem(self.client.totem[1], px, py, self.client.playerCode)
                        self.client.useTotem = True

                self.client.sendPlaceObject(objectID, code, px, py, angle, vx, vy, dur, False)
                self.client.Skills.placeSkill(objectID, code, px, py, angle)
            if self.client.room.luaRuntime != None:
                data = self.client.room.luaRuntime.runtime.eval("{}")
                data["id"] = objectID
                data["type"] = code
                data["x"] = px
                data["y"] = py
                data["angle"] = angle
                data["ghost"] = not dur
                self.client.room.luaRuntime.emit("SummoningEnd", (self.client.playerName, code, px, py, angle, vx, vy, data))
        
        @self.packet(args=['readInt', 'readShort', 'readShort'])
        async def Ice_Cube(self, playerCode, px, py):
            if self.client.isShaman and not self.client.isDead and not self.client.room.isSurvivor and self.client.room.numCompleted > 1:
                if self.client.iceCount != 0 and playerCode != self.client.playerCode:
                    for player in self.client.room.clients.copy().values():
                        if player.playerCode == playerCode and not player.isShaman:
                            player.isDead = True
                            if not self.client.room.noAutoScore: self.client.playerScore += 1
                            player.sendPlayerDied()
                            self.client.sendPlaceObject(self.client.room.objectID + 2, 54, px, py, 0, 0, 0, True, True)
                            self.client.iceCount -= 1
                            self.client.room.checkChangeMap()
        
        @self.packet(args=['readShort'])
        async def Bridge_Break(self, bridgeCode):
            if self.client.room.currentMap in [6, 10, 110, 116]:
                self.client.room.sendAllOthers(self.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
        
        @self.packet(args=['readInt'])
        async def Defilante_Points(self, something):
            self.client.defilantePoints += 1
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("PlayerBonusGrabbed", (self.client.playerName, something))
        
        @self.packet(args=['readInt', 'readInt'])
        async def Restorative_Skill(self, objectID, id):
            self.client.Skills.sendRestorativeSkill(objectID, id)
        
        @self.packet(args=['readShort'])
        async def Recycling_Skill(self, id):
            self.client.Skills.sendRecyclingSkill(id)
            
        @self.packet(args=['readInt', 'readInt'])
        async def Gravitational_Skill(self, velX, velY):
            self.client.Skills.sendGravitationalSkill(0, velX, velY)

        @self.packet(args=['readInt'])
        async def Antigravity_Skill(self, objectID):
            self.client.Skills.sendAntigravitySkill(objectID)

        @self.packet(args=['readByte', 'readInt'])
        async def Handymouse_Skill(self, handyMouseByte, objectID):
            if self.client.room.lastHandymouse[0] == -1:
                self.client.room.lastHandymouse = [objectID, handyMouseByte]
            else:
                self.client.Skills.sendHandymouseSkill(handyMouseByte, objectID)
                self.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                self.client.room.lastHandymouse = [-1, -1]
                
        @self.packet(args=['readUTF', 'readUTF','readByte'])
        async def Enter_Room(self, community, roomName, custom):
            if self.client.playerName in ["", " "]:
                self.client.transport.close()
            else:
                if roomName == "":
                    self.client.startBulle(self.server.recommendRoom(self.client.langue))
                elif not roomName == self.client.roomName or not self.client.room.isEditor or not len(roomName) > 64 or not self.client.roomName == "%s-%s" %(self.client.langue, roomName):
                    if self.client.privLevel < 7: 
                        roomName = self.server.checkRoom(roomName, self.client.langue)
                    roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
                    if roomEnter == None or self.client.privLevel >= 7:
                        self.client.startBulle(roomName)
                    else:
                        if roomEnter.roomPassword != "":
                            self.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                        else:
                            self.client.startBulle(roomName)

        @self.packet(args=['readUTF', 'readUTF'])
        async def Room_Password(self, roomPass, roomName):
            roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
            if roomEnter == None or self.client.privLevel >= 7:
                self.client.startBulle(roomName)
            else:
                if not roomEnter.roomPassword == roomPass:
                    self.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                else:
                    self.client.startBulle(roomName)
        
        @self.packet(args=['readUTF'])
        async def Chat_Message(self, message):
            message = message.replace("&amp;#", "&#").replace("<", "&lt;")
            if self.client.isGuest:
                self.client.sendLangueMessage("", "$Créer_Compte_Parler")
                return
                
            elif message == "!lb":
                self.client.sendLeaderBoard()
                return
                
            elif message == "!listrec":
                await self.client.sendPlayerRecords()
                return
                
            elif message.startswith("!") and self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("ChatCommand", (self.client.playerName, message[1:]))
                if message[1:] in self.client.room.luaRuntime.HiddenCommands:
                    return
                    
            elif not message == "" and len(message) < 256:
                if self.client.isMute:
                    muteInfo = self.server.getModMuteInfo(self.client.playerName)
                    timeCalc = Utils.getHoursDiff(muteInfo[1])          
                    if timeCalc <= 0:
                        self.client.isMute = False
                        if self.client.playerName in self.server.reports:
                            self.server.reports[self.client.playerName]['isMuted'] = False
                            self.server.reports[self.client.playerName]['muteHours'] = 0
                            self.server.reports[self.client.playerName]['muteReason'] = ""
                            self.server.reports[self.client.playerName]['mutedBy'] = ""
                        self.server.removeModMute(self.client.playerName)
                    else:
                        self.client.sendModMuteMessage(self.client.playerName, timeCalc, muteInfo[0], True)
                else:
                    if _time.time() - self.client.MessageTime > 3:
                        if message != self.client.lastMessage:
                            self.client.lastMessage = message
                            if self.client.isMumute:
                                self.client.room.sendAllChat(self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, 2)
                            else:
                                self.client.room.sendAllChat(self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.server.checkMessage(message))
                        else:
                            self.client.sendLangueMessage("", "$Message_Identique")
                        self.client.MessageTime = _time.time()
                    else:
                        self.client.sendLangueMessage("", "$Doucement")

                if not self.client.playerName in self.server.chatMessages:
                    messages = deque([], 60)
                    messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                    self.server.chatMessages[self.client.playerName] = {}
                    self.server.chatMessages[self.client.playerName][self.client.roomName] = messages
                elif not self.client.roomName in self.server.chatMessages[self.client.playerName]:
                    messages = deque([], 60)
                    messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                    self.server.chatMessages[self.client.playerName][self.client.roomName] = messages
                else:
                    self.server.chatMessages[self.client.playerName][self.client.roomName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message, self.client.roomName])
                    
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("ChatMessage", (self.client.playerName, message))
        
        @self.packet(args=['readByte', 'readUTF'])
        async def Staff_Chat(self, type, message):
            if self.client.privLevel < 2:
                return
            self.client.sendAllModerationChat(type, message)
        
        @self.packet(args=['readUTF'])
        async def Commands(self, command):
            if _time.time() - self.client.CMDTime > 1:
                await self.client.Commands.parseCommand(command)
                self.client.CMDTime = _time.time()
        
        @self.packet(args=['readByte', 'readInt', 'readUTF'])
        async def Player_Emote(self, emoteID, playerCode, flag=''):
            self.client.sendPlayerEmote(emoteID, flag, True, False)
            if playerCode != -1:
                if emoteID == 14:
                    self.client.sendPlayerEmote(14, flag, False, False)
                    self.client.sendPlayerEmote(15, flag, False, False)
                    player = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                    if player != None:
                        player.sendPlayerEmote(14, flag, False, False)
                        player.sendPlayerEmote(15, flag, False, False)

                elif emoteID == 18:
                    self.client.sendPlayerEmote(18, flag, False, False)
                    self.client.sendPlayerEmote(19, flag, False, False)
                    player = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                    if player != None:
                        player.sendPlayerEmote(17, flag, False, False)
                        player.sendPlayerEmote(19, flag, False, False)

                elif emoteID == 22:
                    self.client.sendPlayerEmote(22, flag, False, False)
                    self.client.sendPlayerEmote(23, flag, False, False)
                    player = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                    if player != None:
                        player.sendPlayerEmote(22, flag, False, False)
                        player.sendPlayerEmote(23, flag, False, False)

                elif emoteID == 26:
                    self.client.sendPlayerEmote(26, flag, False, False)
                    self.client.sendPlayerEmote(27, flag, False, False)
                    player = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                    if player != None:
                        player.sendPlayerEmote(26, flag, False, False)
                        player.sendPlayerEmote(27, flag, False, False)
                        self.client.room.sendAll(Identifiers.send.Joquempo, ByteArray().writeInt(self.client.playerCode).writeByte(random.randint(0, 2)).writeInt(player.playerCode).writeByte(random.randint(0, 2)).toByteArray())

            if self.client.isShaman:
                self.client.Skills.parseEmoteSkill(emoteID)
            
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("EmotePlayed", (self.client.playerName, emoteID))
            
        @self.packet(args=['readByte'])
        async def Player_Emotions(self, emotionID):
            self.client.sendEmotion(emotionID)
            
        @self.packet(args=['readBoolean'])
        async def Player_Shaman_Fly(self, fly):
            self.client.Skills.sendShamanFly(fly)
        
        @self.packet
        async def Player_Shop_List(self):
            self.client.Shop.sendShopList(True)

        @self.packet(args=['readByte'])
        async def Player_Buy_Skill(self, skill):
            self.client.Skills.buySkill(skill)
            
        @self.packet
        async def Player_Redistribute(self):
            self.client.Skills.redistributeSkills()

        @self.packet(args=['readUTF', 'readByte', 'readUTF'])
        async def Player_Report(self, playerName, type, comments):
            self.client.modoPwet.makeReport(playerName, type, comments)
        
        @self.packet(args=['readByte'])
        async def Player_Ping1(self, ping):
            if (_time.time() - self.client.PInfo[1]) >= 5:
                self.client.PInfo[1] = _time.time()
                self.client.sendPacket(Identifiers.send.Ping, ByteArray().writeByte(self.client.PInfo[0]).writeByte(0).toByteArray())
                self.client.PInfo[0] += 1
                if self.client.PInfo[0] == 31:
                    self.client.PInfo[0] = 0
                    
        @self.packet(args=['readShort', 'readShort'])
        async def Player_Meep(self, posX, posY):
            self.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(self.client.playerCode).toByteArray())
            self.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(self.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if self.client.isShaman else 5).toByteArray())
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("PlayerMeep", (self.client.playerName))
        
        @self.packet
        async def Player_Vampire(self):
            self.client.sendVampireMode(True)
            
        @self.packet(args=['readUTF'])
        async def Player_Calendar(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                p = ByteArray()
                p.writeUTF(playerName)
                p.writeUTF(player.playerLook)
                p.writeInt(len(player.aventurePoints.values()))
                p.writeShort(len(player.titleList))
                p.writeShort(len(player.shopBadges))
                #p.writeShort(len(self.server.calendarioSystem.keys())) any way to see if the aventure is working correctly ?
                p.writeShort(len(self.server.events))
                for aventure in self.server.events:
                    p.writeShort(9)
                    p.writeByte(1)
                    p.writeShort(self.server.events[aventure]["id"])
                    p.writeInt(self.server.events[aventure]["starting_date"])
                    p.writeInt(self.client.aventurePoints[aventure] if aventure in self.client.aventurePoints.keys() else 0)
                    p.writeBoolean(_time.time() > self.server.events[aventure]["ending_date"])
                    p.writeByte(len(self.server.events[aventure]["items"]))
                    for item in self.server.events[aventure]["items"]:
                        items = item.split(":")
                        p.writeByte(items[0])
                        p.writeBoolean(False) # true - readUTF,  false - readShort
                        p.writeShort(items[1])
                        p.writeInt(items[2])
                        p.writeByte(self.server.getPointsColor(playerName, aventure, items[1], items[0], items[3]))
                        p.writeByte(1)
                        p.writeShort(self.server.getAventureCounts(playerName, aventure, items[1], items[0]))
                        p.writeShort(items[3])
                    p.writeByte(len(self.server.events[aventure]["counts"]))
                    for item in self.server.events[aventure]["counts"]:
                        items = item.split(":")
                        p.writeByte(items[0])
                        p.writeBoolean(False) # true - readUTF,  false - readShort
                        p.writeShort(items[1])
                        p.writeInt(self.server.getAventureItems(playerName, aventure, int(items[0]), int(items[1])))
                self.client.sendPacket(Identifiers.send.Adventures, p.toByteArray())
            
            
        @self.packet
        async def Tribe_House(self):
            if not self.client.tribeName == "":
                self.client.startBulle("*\x03%s" %(self.client.tribeName))

        @self.packet(args=['readUTF'])
        async def Tribe_Invite(self, playerName):
            player = self.server.players.get(playerName)
            if player != None and player.tribeName in self.client.invitedTribeHouses:
                if self.server.rooms.get("*%s%s" %(chr(3), player.tribeName)) != None:
                    if self.client.room.roomName != "*%s%s" %(chr(3), player.tribeName):
                        self.client.startBulle("*%s%s" %(chr(3), player.tribeName))
                else:
                    player.sendLangueMessage("", "$InvTribu_MaisonVide")

        @self.packet(args=['readByte'])
        async def Equip_Clothe(self, _id):
            self.client.Shop.equipClothe(_id)
                    
        @self.packet(args=['readByte'])
        async def Save_Clothe(self, _id):
            self.client.Shop.saveClothe(_id)
                    
        @self.packet
        async def Shop_Info(self):
            self.client.Shop.sendShopInfo()
                
        @self.packet(args=['readInt'])
        async def Equip_Item(self, _id):
            self.client.Shop.equipItem(_id)
            
        @self.packet(args=['readInt', 'readBoolean'])
        async def Equip_Item(self, _id, status):
            self.client.Shop.buyItem(_id, status)
        
        @self.packet(args=['readInt', 'readBoolean'])
        async def Buy_Item(self, _id, status):
           self.client.Shop.buyItem(_id, status)
          
        @self.packet(args=['readInt', 'readBoolean'])
        async def Buy_Custom(self, _id, status):
            self.client.Shop.customItemBuy(_id, status)

        @self.packet(args=['readInt', 'readByte'])
        async def Custom_Item(self, fullItem, length):
            customs = []
            i = 0
            while i < length:
                customs.append(self.packet.readInt())
                i += 1
            self.client.Shop.customItem(fullItem, customs)

        @self.packet(args=['readByte', 'readBoolean'])
        async def Buy_Clothe(self, _id, status):
            self.client.Shop.buyClothe(_id, status)
            
        @self.packet(args=['readShort', 'readUTF'])
        async def Buy_Full_Look_Confirm(self, _id, status):
            self.client.Shop.buyFullLookConfirm(_id, status)

        @self.packet(args=['readShort', 'readBoolean'])
        async def Buy_Shaman_Item(self, _id, status):
            self.client.Shop.buyShamanItem(_id, status)

        @self.packet(args=['readInt'])
        async def Equip_Shaman_Item(self, _id):
            self.client.Shop.equipShamanItem(_id)

        @self.packet(args=['readInt', 'readBoolean'])
        async def Buy_Shaman_Custom(self, _id, status):
            self.client.Shop.customShamanItemBuy(_id, status)

        @self.packet(args=['readInt', 'readByte'])
        async def Custom_Item(self, fullItem, length):
            customs = []
            i = 0
            while i < length:
                customs.append(self.packet.readInt())
                i += 1
            self.client.Shop.customShamanItem(fullItem, customs)

        @self.packet(args=['readUTF', 'readBoolean', 'readInt', 'readUTF'])
        async def Send_gift1(self, playerName, isShamanItem, fullItem, message):
            self.client.Shop.sendShopGift(playerName, isShamanItem, fullItem, message)

        @self.packet(args=['readInt', 'readBoolean', 'readUTF', 'readBoolean'])
        async def Gift_result(self, giftID, isOpen, message, isMessage):
            self.client.Shop.giftResult(giftID, isOpen, message, isMessage)
        
        @self.packet(args=['readBoolean'])
        async def Modopwet(self, isOpen):
            if self.client.privLevel >= 7:
                self.client.modoPwet.openModoPwet(isOpen)
                p = ByteArray().writeShort(31)
                for i in ['GB', 'FR', 'RU', 'BR', 'ES', 'CN', 'TR', 'VK', 'PL', 'HU', 'NL', 'RO', 'ID', 'DE', 'E2', 'AR', 'PH', 'LT', 'JP', 'CH', 'FI', 'CZ', 'HR', 'SK', 'BG', 'LV', 'HE', 'IT', 'ET', 'AZ', 'PT']: p.writeUTF(i)
                self.client.sendPacket(Identifiers.send.Modopwet_Add_Language, p.toByteArray())
                self.client.isModoPwet = isOpen

        @self.packet(args=['readUTF', 'readByte'])
        async def Delete_Report(self, playerName, closeType):
            self.client.modoPwet.deleteReport(playerName, closeType)

        @self.packet(args=['readUTF', 'readByte'])
        async def Watch(self, playerName, isWatching):
            if self.client.privLevel >= 7:
                if not self.client.playerName == playerName:
                    roomName = self.server.players[playerName].roomName if playerName in self.server.players else ""
                    if not roomName == "" and not roomName == self.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                        if not isWatching:
                            if self.server.players[playerName].followed == None:
                                self.client.isHidden = True
                                self.client.sendPlayerDisconnect()
                                self.client.isDead = True
                                self.client.enterRoom(roomName)
                                self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(playerName).writeBoolean(True).toByteArray())
                                self.server.players[playerName].followed = self.client
                            else:
                                self.client.isHidden = False
                                self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF("").writeBoolean(False).toByteArray())
                                self.client.enterRoom(self.client.lastroom)
                                self.server.players[playerName].followed = None
                        else:
                            self.client.enterRoom(roomName)
        
        @self.packet(args=['readUTF', 'readBoolean'])
        async def Ban_Hack(self, playerName, silent):
            if self.client.privLevel >= 7:
                self.client.modoPwet.banHack(playerName, silent)

        @self.packet(args=['readUTF', 'readBoolean', 'readBoolean', 'readBoolean'])
        async def Change_Langue(self, langue, modopwetOnlyPlayerReports, sortBy, reOpen):
            if self.client.privLevel >= 7:
                self.client.modoPwetLangue = langue.upper()
                self.client.sendPacket(Identifiers.send.Modopwet_Update_Language)
                if reOpen:
                    self.client.modoPwet.openModoPwet(self.client.isModoPwet, modopwetOnlyPlayerReports, sortBy)
                
        @self.packet(args=['readBoolean', 'readByte'])
        async def Modopwet_Notifications(self, isTrue, leng):
            if self.client.privLevel >= 7:
                self.client.isModoPwetNotifications = isTrue
                self.client.Notifications = []
                x = 0
                while leng > x:
                    self.client.Notifications.append(self.packet.readUTF())
                    x+=1

        @self.packet(args=['readUTF'])
        async def Chat_Log(self, playerName):
            self.client.modoPwet.openChatLog(playerName)

        @self.packet(args=['readUTF', 'readUTF', 'readUTF', 'readUTF'])
        async def Create_Account(self, playerName, password, email, captcha):
            if self.client.checkTimeAccount() or self.server.isDebug:
                if self.server.checkExistingUser(playerName):
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(3).writeUTF(playerName).writeUTF("").toByteArray())
                elif not re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", playerName):
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeUTF("").writeUTF("").toByteArray())
                elif not self.client.currentCaptcha == captcha:
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(7).writeUTF("").writeUTF("").toByteArray())
                else:
                    tag = "".join([str(random.choice(range(9))) for x in range(4)])
                    playerName += "#" + tag
                    self.client.sendAccountTime()
                    self.server.lastPlayerID += 1
                    self.client.canLogin[2] = True
                    self.client.canLogin[3] = True
                    self.Cursor['users'].insert_one({"Username":playerName,"Password":password,"PlayerID":self.server.lastPlayerID,"PrivLevel":1,"TitleNumber":0,"FirstCount":0,"CheeseCount":0,"ShamanCheeses":0,"ShopCheeses":self.server.initialCheeses,"ShopFraises":self.server.initialFraises,"ShamanSaves":0,"ShamanSavesNoSkill":0,"HardModeSaves":0,"HardModeSavesNoSkill":0,"DivineModeSaves":0,"DivineModeSavesNoSkill":0,"BootcampCount":0,"ShamanType":0,"ShopItems":"","ShamanItems":"","Clothes":"","Look":"1;0,0,0,0,0,0,0,0,0,0,0","ShamanLook":"0,0,0,0,0,0,0,0,0,0","MouseColor":"78583a","ShamanColor":"95d9d6","RegDate":Utils.getTime(),"Badges":"","CheeseTitleList":"","FirstTitleList":"","ShamanTitleList":"","ShopTitleList":"","BootcampTitleList":"","HardModeTitleList":"","DivineModeTitleList":"","SpecialTitleList":"","BanHours":0,"ShamanLevel":0,"ShamanExp":0,"ShamanExpNext":0,"Skills":"","LastOn":32,"FriendsList":"","IgnoredsList":"","Gender":0,"LastDivorceTimer":0,"Marriage":"","TribeCode":0,"TribeRank":0,"TribeJoined":0,"Gifts":"","Messages":"","SurvivorStats":"0,0,0,0","RacingStats":"0,0,0,0","DefilanteStats":"0,0,0","Consumables":"","EquipedConsumables":"","Pet":0,"PetEnd":0,"Fur":0,"FurEnd":0,"ShamanBadges":"","EquipedShamanBadge":0,"totemitemcount":0,"totem":"","VisuDone":"","customitems":"","langue":self.client.langue,"AventureCounts":"","AventurePoints":"24:0","AventureSaves":0,"user_community":self.client.computerLanguage,"avatar":"0.jpg","Email":email,"Letters":"","Time":0,"Karma":0,"Roles":"{}"})
                    await self.client.loginPlayer(playerName, password, "\x03[Tutorial] %s" %(playerName))
                    self.client.sendServerMessage("The ip %s created account <V>%s</V>. (<J>%s</J>)." %(self.client.ipAddress, playerName, self.client.langue))
            else:
                self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeByte(0).writeByte(0).writeUTF(playerName).toByteArray())

        @self.packet(args=['readUTF','readUTF','readUTF','readUTF','readInt'])
        async def Login(self, playerName, password, url, startRoom, resultKey):
            # Login Keys
            if len(self.server.loginKeys) > 0:
                tempauth = self.server.authKey
                for value in self.server.loginKeys:
                    if value != "":
                        tempauth ^= value
                self.client.canLogin[2] = True if tempauth == resultKey else False # aiotfm
            else:
                self.client.canLogin[2] = True

            # URL
            if len(self.server.serverURL) > 0:
                for _url in self.server.serverURL:
                    if url.startswith(_url):
                        self.client.canLogin[3] = True
                        break
            else:
                self.client.canLogin[3] = True

            if playerName == "" and password != "":
                self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
            else:
                await self.client.loginPlayer(playerName, password, startRoom)
                
        

        @self.packet(args=['readUTF'])
        async def New_Survey(self, description):
            if self.client.privLevel != 9:
                return
            description = '[' + description + ']'
            options = []
            while self.packet.bytesAvailable():
                options.append(self.packet.readUTF())
            if len(options) > 0:
                packet1 = ByteArray()
                packet2 = ByteArray()
                packet1.writeInt(self.client.playerID).writeUTF("").writeBoolean(False).writeUTF(description)
                packet2.writeInt(1).writeUTF("").writeBoolean(False).writeUTF(description)
                for option in options:
                    packet1.writeUTF(option)
                    packet2.writeUTF(option)
              
                for player in self.server.players.copy().values():
                    if player.langue == self.client.langue:
                        player.sendPacket(Identifiers.send.Survey, packet1.toByteArray())
                    else:
                        player.sendPacket(Identifiers.send.Survey, packet2.toByteArray())
            else:
                self.client.sendClientMessage("Your survey must require one option.", True)
                
        @self.packet(args=['readInt', 'readByte'])
        async def Survey_Answer(self, playerID, optionID):
            for player in self.server.players.copy().values():
                if playerID == player.playerID:
                    player.sendPacket(Identifiers.send.Survey_Answer, ByteArray().writeByte(optionID).toByteArray())

        @self.packet(args=['readUTF'])
        async def Survey_Result(self, description):
            if self.client.privLevel != 9:
                return
            description = '[' + description + ']'
            options = []
            while self.packet.bytesAvailable():
                options.append(self.packet.readUTF())
            p = ByteArray()
            p.writeInt(0).writeUTF("").writeBoolean(False).writeUTF(description)
            for result in results:
                p.writeUTF(result)
            
            for player in self.server.players.copy().values():
                if player.langue == self.client.langue and player.playerName != self.client.playerName:
                    player.sendPacket(Identifiers.send.Survey, p.toByteArray())

        @self.packet
        async def Captcha(self):
            self.client.currentCaptcha = random.choice(list(self.server.captchaList))
            self.client.sendPacket(Identifiers.send.Captcha, self.server.captchaList[self.client.currentCaptcha][0])


        @self.packet
        async def Player_MS(self):
            self.client.sendPacket(Identifiers.send.Player_MS)

        @self.packet
        async def Dummy(self):
            if self.client.awakeTimer != None: self.client.awakeTimer.cancel()
            self.client.awakeTimer = self.server.loop.call_later(120, self.client.transport.close)

        @self.packet(args=['readUTF'])
        async def Temps_Client(self, temps):
            self.client.sendPacket(Identifiers.send.Temps_Client, ByteArray().writeUTF(temps).toByteArray())
            
        @self.packet(args=['readShort'])
        async def Player_Info(self, info):
            self.client.sendPacket(Identifiers.send.Player_Info, ByteArray().writeByte(0).writeUTF(info).toByteArray())

        @self.packet(args=['readShort'])
        async def Player_FPS(self, info):
            self.client.sendPacket(Identifiers.send.Player_FPS, ByteArray().writeByte(0).writeUTF(info).toByteArray())

        @self.packet(args=['readByte'])
        async def Rooms_List(self, mode):
            self.client.lastGameMode = mode
            self.client.sendGameMode(mode)

        @self.packet
        async def Request_Info(self):
            #self.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://localhost/tfm/info.php").toByteArray()) # ?
            f = 1
                
        @self.packet(args=['readShort'])
        async def Transformation_Object(self, objectID):
            if (not self.client.isDead and self.client.room.currentMap in self.client.room.transformationMaps) or self.client.room.isFuncorp or self.client.hasLuaTransformations:
                self.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(self.client.playerCode).writeShort(objectID).toByteArray())

            
        @self.packet(args=['readByte', 'readByte', 'readUnsignedByte', 'readUnsignedByte', 'readUTF'])
        async def Game_Log(self, errorC, errorCC, oldC, oldCC, error):
            if self.server.isDebug:
                if errorC == 1 and errorCC == 1:
                    print("[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, oldCC, error))
                    with open("./include/logs/Errors/Debug.log", "a") as f:
                        f.write("[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, oldCC, error))
                    f.close()
                elif errorC == 60 and errorCC == 1:
                    if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                    print("[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, error))
                    with open("./include/logs/Errors/Debug.log", "a") as f:
                        f.write("[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, error))
                    f.close()
                else:
                    testfunc = ''
                    ccc = [errorC, errorCC]
                    for i in dir(Identifiers.send):
                        if '__' in i: continue
                        exec(f"self.valuer = Identifiers.send.{i}")
                        if self.valuer == ccc:
                            testfunc = i
                    print("[%s] [%s] GameLog Error - Func: %s C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, testfunc, errorC, errorCC, error))
                    with open("./include/logs/Errors/Debug.log", "a") as f:
                        f.write("[%s] [%s] GameLog Error - Func: %s C: %s CC: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, testfunc, errorC, errorCC, error))
                    f.close()
            
        @self.packet(args=['readByte'])
        async def Player_Ping(self, VC):
            if self.client.PInfo[0] == VC + 1:
                self.client.PInfo[2] = int((_time.time() - self.client.PInfo[1])*1000)

        @self.packet(args=['readByte', 'readByte'])
        async def Change_Shaman_Type(self, type, noshmskills):
            self.client.isNoShamanSkills = noshmskills
            self.client.shamanType = type
            self.client.sendShamanType(type, (self.client.shamanSaves >= self.server.minimumNormalSaves and self.client.hardModeSaves >= self.server.minimumHardSaves), self.client.isNoShamanSkills)

        @self.packet(args=['readUTF', 'readByte', 'readUTFBytes'])
        async def Letter(self, playerName, type_letter, letters):
            consumables = {0:29, 1:30, 2:2241, 3:2330, 4:2351, 5:2522}
            if type_letter in consumables:
                count = self.client.playerConsumables[consumables[type_letter]] - 1
                if count <= 0:
                    del self.client.playerConsumables[consumables[type_letter]]
                else:
                    self.client.playerConsumables[consumables[type_letter]] = count
                    
                self.client.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.client.playerCode).writeShort(consumables[type_letter]).toByteArray())
                self.client.sendUpdateInventoryConsumable(consumables[type_letter], count)
                
            player = self.server.players.get(playerName)
            if (player != None):
                p = ByteArray()
                p.writeUTF(self.client.playerName)
                p.writeUTF(self.client.playerLook)
                p.writeByte(type)
                p.writeBytes(letters)
                player.sendPacket(Identifiers.send.Letter, p.toByteArray())
                self.client.sendLangueMessage("", "$MessageEnvoye")
            else:
                playerID = self.server.getPlayerID(playerName)
                hashed_letters = self.Cursor['users'].find_one({'PlayerID':playerID})['Letters']
                if playerID != -1:
                    hashed_letters += ("" if len(hashed_letters) == 0 else "$") + "|".join(map(str, [self.client.playerName, str(int(self.client.mouseColor, 16)) + "##" + str(self.client.playerLook), type_letter, base64.b64encode(zlib.compress(letters)).decode()]))
                    self.Cursor['users'].update_one({'PlayerID':playerID},{'$set':{'Letters':hashed_letters}})
                else:
                    self.client.sendLangueMessage("", "$Joueur_Existe_Pas")

        @self.packet
        async def Send_gift(self):
            self.client.sendPacket(Identifiers.send.Send_gift, ByteArray().writeByte(1).toByteArray())
                
        @self.packet(args=['readUTF', 'readUTF', 'readUTF'])
        async def Computer_Info(self, info, os_type, os_version):
            self.client.computerLanguage = info
            self.client.computerOS = os_type
            self.client.computerOSVersion = os_version
            self.client.canLogin[0] = True if len(info) > 0 and len(os_type) > 0 and len(os_version) > 0 else False
            
        @self.packet(args=['readInt'])
        async def Change_Shaman_Color(self, color):
            color = packet.readInt()
            self.client.shamanColor = "%06X" %(0xFFFFFF & color)
            
        @self.packet
        async def Tribulle_API(self):
            self.client.sendPacket(Identifiers.send.Tribulle_Token, ByteArray().writeUTF("https://disneyclient.com/info.php").toByteArray())
            
        @self.packet
        async def Lua_Script(self):
            script = self.packet.readUTFBytes(int.from_bytes(self.packet.read(3),'big')).decode()
            if(self.client.privLevel in [9, 4] or self.client.isLuaCrew) or ((self.client.privLevel == 5 or self.client.isFunCorpPlayer) and self.room.isFuncorp) or self.server.isDebug:
                if not self.client.isLuaAdmin:
                    if self.client.room.luaRuntime == None:
                        self.client.room.luaRuntime = Lua(self.client.room, self.server)
                    self.client.room.luaRuntime.owner = self.client
                    self.client.room.luaRuntime.RunCode(script)
                else: self.client.runLuaScript(script)

        @self.packet(args=['readShort', 'readBoolean', 'readShort', 'readShort', 'readShort', 'readShort'])
        async def Key_Board(self, key, down, posX, posY, xPlayerVelocity, yPlayerVelocity):
            if self.client.room.isBootcamp and key == 71:
                if not self.client.isDead:
                    self.client.isDead = True
                    if not self.client.room.noAutoScore: self.client.playerScore += 1
                    self.client.sendPlayerDied()
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("Keyboard", (self.client.playerName, key, down, posX, posY, xPlayerVelocity, yPlayerVelocity))
            
        @self.packet(args=['readShort', 'readShort'])
        async def Mouse_Click(self, posX, posY):                 
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("Mouse", (self.client.playerName, posX, posY))

        @self.packet(args=['readInt', 'readUTF'])
        async def Popup_Answer(self, popupID, answer):
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("PopupAnswer", (popupID, self.client.playerName, answer))
        
        @self.packet(args=['readInt', 'readUTF'])
        async def Text_Area_Callback(self, textAreaID, event):
            print(event)
            if event in ["lbileri","lbgeri","lbkapat"]:
                self.client.lbSayfaDegis(event=="lbileri", event=="lbkapat")
                return 
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("TextAreaCallback", (textAreaID, self.client.playerName, event))

        @self.packet(args=['readInt', 'readUTF', 'readInt', 'readUTF'])
        async def Color_Picked(self, colorPickerId, player, color, title):
            if self.client.room.luaRuntime != None:
                self.client.room.luaRuntime.emit("ColorPicked", (colorPickerId, player, color))
        
        @self.packet
        async def Reload_Cafe(self):
            if not self.client.isReloadCafe:
                await self.client.Cafe.loadCafeMode()
                self.client.isReloadCafe = True
                self.server.loop.call_later(2, setattr, self.client, "isReloadCafe", False)
        
        @self.packet(args=['readInt'])
        async def Open_Cafe_Topic(self, topicID):
            await self.client.Cafe.openCafeTopic(topicID)
            
        @self.packet(args=['readUTF', 'readUTF'])
        async def Create_New_Cafe_Topic(self, message, title):
            await self.client.Cafe.createNewCafeTopic(message, title)
        
        @self.packet(args=['readInt', 'readUTF'])
        async def Create_New_Cafe_Post(self, topicID, message):
            await self.client.Cafe.createNewCafePost(topicID, message)

        @self.packet(args=['readBoolean'])
        async def Open_Cafe(self, isCafeOpen):
            self.client.isCafe = isCafeOpen

        @self.packet(args=['readInt', 'readInt', 'readBoolean'])
        async def Vote_Cafe_Post(self, topicID, postID, mode):
            await self.client.Cafe.voteCafePost(topicID, postID, mode)

        @self.packet(args=['readInt'])
        async def Delete_Cafe_Message(self, postID):
            if self.client.privLevel >= 7:
                await self.client.Cafe.deleteCafePost(postID)

        @self.packet(args=['readInt', 'readUTF'])
        async def Delete_All_Cafe_Message(self, topicID, playerName):
            if self.client.privLevel >= 7:
                await self.client.Cafe.deleteAllCafePost(topicID, playerName)

        @self.packet
        async def Mulodrome_Close(self):
            self.client.room.sendAll(Identifiers.send.Mulodrome_End)

        @self.packet(args=['readByte', 'readByte'])
        async def Mulodrome_Join(self, team, position):
            if len(self.client.mulodromePos) != 0:
                self.client.room.sendAll(Identifiers.send.Mulodrome_Leave, chr(self.client.mulodromePos[0]) + chr(self.client.mulodromePos[1]))

            self.client.mulodromePos = [team, position]
            self.client.room.sendAll(Identifiers.send.Mulodrome_Join, ByteArray().writeByte(team).writeByte(position).writeInt(self.client.playerID).writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
            if self.client.playerName in self.client.room.redTeam: self.client.room.redTeam.remove(self.client.playerName)
            if self.client.playerName in self.client.room.blueTeam: self.client.room.blueTeam.remove(self.client.playerName)
            if team == 1:
                self.client.room.redTeam.append(self.client.playerName)
            else:
                self.client.room.blueTeam.append(self.client.playerName)

        @self.packet(args=['readByte', 'readByte'])
        async def Mulodrome_Leave(self, team, position):
            team, position = packet.readByte(), packet.readByte()
            self.client.room.sendAll(Identifiers.send.Mulodrome_Leave, ByteArray().writeByte(team).writeByte(position).toByteArray())
            if team == 1:
                for playerName in self.client.room.redTeam:
                    if self.client.room.clients[playerName].mulodromePos[1] == position:
                        self.client.room.redTeam.remove(playerName)
                        break
            else:
                for playerName in self.client.room.blueTeam:
                    if self.client.room.clients[playerName].mulodromePos[1] == position:
                        self.client.room.blueTeam.remove(playerName)
                        break

        @self.packet
        async def Mulodrome_Play(self):
            if not len(self.client.room.redTeam) == 0 or not len(self.client.room.blueTeam) == 0:
                self.client.room.isMulodrome = True
                self.client.room.isRacing = True
                self.client.room.noShaman = True
                self.client.room.mulodromeRoundCount = 0
                self.client.room.never20secTimer = True
                self.client.room.sendAll(Identifiers.send.Mulodrome_End)
                await self.client.room.mapChange()
        
        @self.packet
        async def Open_Inventory(self):
            self.client.sendInventoryConsumables()

        @self.packet(args=['readShort'])
        async def Use_Consumable(self, id):
            self.client.useConsumable(id)
            
        @self.packet(args=['readShort', 'readBoolean'])
        async def Equip_Consumable(self, id, equip):
            if equip:
                if id in self.client.equipedConsumables:
                    self.client.equipedConsumables.remove(id)
                self.client.equipedConsumables.append(id)
            else:
                self.client.equipedConsumables.remove(id)

        @self.packet(args=['readUTF'])
        async def Trade_Invite(self, playerName):
            self.client.tradeInvite(playerName)
                
        @self.packet(args=['readUTF'])
        async def Cancel_Trade(self, playerName):
            self.client.cancelTrade(playerName)
            
        @self.packet(args=['readShort', 'readBoolean'])
        async def Trade_Add_Consusmable(self, id, isAdd):
            self.client.tradeAddConsumable(id, isAdd)

        @self.packet(args=['readBoolean'])
        async def Trade_Result(self, isAccept):
                self.client.tradeResult(isAccept)


        @self.packet(args=['readShort'])
        async def Tribulle(self, code):
            self.client.tribulle.parseTribulleCode(code, self.packet)

        @self.packet(args=['readUTF'])
        async def Set_Language(self, langue):
            langue = langue.upper()
            self.client.langue = langue
            if "-" in self.client.langue:
                self.client.langue = self.client.langue.split("-")[1]
            self.client.langueID = Utils.getLangueID(self.client.langue)
            self.client.sendPacket(Identifiers.send.Set_Language, ByteArray().writeUTF(langue).writeUTF(self.server.langs.get(self.client.langue.lower())[1]).writeShort(0).writeBoolean(False).writeBoolean(True).writeUTF('').toByteArray())
        
        @self.packet
        async def Language_List(self):
            data = ByteArray().writeShort(len(self.server.langs)).writeUTF(self.client.langue.lower())
            for info in self.server.langs.get(self.client.langue.lower()):
                data.writeUTF(info)

            for info in self.server.languages:
                if info[0] != self.client.langue.lower():
                    data.writeUTF(info[0])
                    data.writeUTF(info[1])
                    data.writeUTF(info[2])
            self.client.sendPacket(Identifiers.send.Language_List, data.toByteArray())
            
        @self.packet()
        async def BotProtection(self):
            self.packet.decryptIdentification(self.server.packetKeys, str(self.client.verifycoder).encode())
            code = self.packet.readInt()
            self.client.canLogin[1] = (code != self.client.verifycoder)

        @self.packet(args=['readUTF'])
        async def Open_Community_Partner(self, partner):
            if partner == "DisneyClient":
                self.client.sendPacket(Identifiers.send.Open_Link, ByteArray().writeUTF("http://disneyclient.com").toByteArray())

        @self.packet(args=['readShort', 'readShort', 'readShort', 'readShort', 'readUTF', 'readBoolean'])
        async def Invocation(self, objectCode, posX, posY, rotation, position, invocation):
            if self.client.isShaman:
                showInvocation = True
                if self.client.room.isSurvivor:
                    showInvocation = invocation
                pass
                if showInvocation:
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Invocation, ByteArray().writeInt(self.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("SummoningStart", (self.client.playerName, objectCode, posX, posY, rotation))

        @self.packet
        async def Remove_Invocation(self):
            if self.client.isShaman:
                self.client.room.sendAllOthers(self.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(self.client.playerCode).toByteArray())
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("SummoningCancel", (self.client.playerName))

        @self.packet(args=['readByte'])
        async def Change_Shaman_Badge(self, badge):
            if str(badge) or badge == 0 in self.client.shamanBadges:
                self.client.equipedShamanBadge = str(badge)
                self.client.sendProfile(self.client.playerName)

        @self.packet(args=['readByte'])
        async def NPC_Functions(self, id):
            if id == 4:
                self.client.openNpcShop(self.packet.readUTF())
            else:
                self.client.buyNPCItem(self.packet.readByte())

        
            #elif CC == Identifiers.recv.Transformice.Question: 
            #    pass

        @self.packet(args=['readByte'])
        async def Map_Info(self, cheesesCount):
            self.client.room.cheesesList = []
            i = 0
            while i < cheesesCount // 2:
                cheeseX, cheeseY = self.packet.readShort(), self.packet.readShort()
                self.client.room.cheesesList.append([cheeseX, cheeseY])
                i += 1
            
            self.client.room.holesList = []
            holesCount = self.packet.readByte()
            i = 0
            while i < holesCount // 3:
                holeType, holeX, holeY = self.packet.readShort(), self.packet.readShort(), self.packet.readShort()
                self.client.room.holesList.append([holeType, holeX, holeY])
                i += 1
                
        @self.packet(args=['readByte'])
        async def Crazzy_Packet(self, type):
            if type == 2:
                posX = int(self.packet.readShort())
                posY = int(self.packet.readShort())
                lineX = int(self.packet.readShort())
                lineY = int(self.packet.readShort())
                self.client.room.sendAllOthers(self.client, Identifiers.send.Crazzy_Packet, self.client.getCrazzyPacket(2,[self.client.playerCode, self.client.drawingColor, posX, posY, lineX, lineY]))
        
        @self.packet(args=['readShort'])
        async def Full_Look(self, look):
            self.client.Shop.buyFullLook(str(look))
            
        @self.packet
        async def Open_Missions(self):
            self.client.missions.sendMissions()
            
        @self.packet(args=['readShort'])
        async def Change_Mission(self, missionID):
            self.client.missions.changeMission(str(missionID))

        @self.packet(args=['readInt', 'readInt'])
        async def Report_Cafe_Post(self, PostID, TopicID):
            await self.client.Cafe.ReportCafeTopic(TopicID, PostID)

        @self.packet
        async def Send_Warnings(self):
            await self.client.Cafe.sendWarnings()

        @self.packet(args=['readInt', 'readBoolean'])
        async def Check_Cafe_Message(self, topicID, delete):
            await self.client.Cafe.CheckMessageType(topicID, delete)

        @self.packet(args=['readByte', 'readByte', 'readInt'])
        async def Sonar_System(self, code, key, time):
            if self.client.playerName not in self.server.sonar:
                return
            if key == 0 and code == 2: return
            chars = {1:"↑ (Last Jump)", 38:"↑",37:"←",39:"→",40:"↓",87:"↑",68:"→",65:"←",83:"↓"}
            self.server.sonar[self.client.playerName].append(f"<BL>{chars[key]}<G> + <V>{time}</V> ms")
                           
        @self.packet(args=['readInt'])
        async def Attach_Player(self, playerCode):
            self.client.room.sendAll(Identifiers.send.SetPositionToAttach, ByteArray().writeByte(-1).toByteArray()) # Detach
            self.client.room.sendAll(Identifiers.send.AttachPlayer, ByteArray().writeInt(playerCode).writeInt(self.client.playerCode).writeInt(1*1000).toByteArray())

        @self.packet
        async def NotAttach_Player(self):
            self.client.room.sendAll(Identifiers.send.SetPositionToAttach, ByteArray().writeByte(-1).toByteArray())

        @self.packet
        async def Open_Outfits(self):
            if self.client.privLevel not in [3, 9] and not self.client.isFashionSquad:
                return
            p = ByteArray()
            p.writeInt(len(self.server.shopOutfitsCheck))
            for id in self.server.shopOutfitsCheck:
                p.writeInt(int(id))
                p.writeUTF(self.server.shopOutfitsCheck[id][3])
                p.writeInt(int(self.server.shopOutfitsCheck[id][1]))
                p.writeUTF(str(datetime.fromtimestamp(int(self.server.shopOutfitsCheck[id][4]),tz=None)).split(' ')[0])
                p.writeUTF(self.server.shopOutfitsCheck[id][0])
                p.writeByte(2 if not int(self.server.shopOutfitsCheck[id][5]) else 3)
            self.client.sendPacket(Identifiers.send.Open_Outfits, p.toByteArray())

        @self.packet(args=['readUTF', 'readShort', 'readUTF', 'readUTF'])
        async def Add_Outfit(self, name, bg, date, look):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
            if name != "name" and date != "date" and look != "look":
                date = int(date)
                self.server.shopData["fullLooks"].append({"id":self.server.lastoutfitid(),"name":name,"look":look,"bg":bg,"start":date,"discount":20, "perm":0})
                self.server.updateShop()
                return await self.parsePacket(1,149,12,ByteArray())
            else:
                self.client.sendClientMessage("Invalid arguments.", 1)

        @self.packet(args=['readInt'])
        async def Remove_Outfit(self, id):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
            for i in self.server.shopData["fullLooks"]:
                if int(i["id"]) == id:
                    self.server.shopData["fullLooks"].remove(i)
                    break
            self.server.updateShop()
            await self.parsePacket(1,149,12,ByteArray())

        @self.packet(args=['readUTF'])
        async def View_Posts(self, playerName):
            await self.client.Cafe.ViewCafeMessages(playerName)

        @self.packet
        async def Open_Sales(self):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
            packet = ByteArray()
            packet.writeEncoded(len(self.server.promotions))
            x = 1
            self.data = {}
            for promo in self.server.promotions:
                packet.writeEncoded(x)
                packet.writeUTF(f'{promo[0]},{promo[1]}')
                self.data[x] = [promo[0],promo[1]]
                try: timer = promo[4]
                except: timer = _time.time()
                packet.writeUTF(str(datetime.fromtimestamp(int(timer),tz=None)))
                packet.writeUTF(str(datetime.fromtimestamp(int(promo[3]),tz=None)))
                packet.writeEncoded(promo[2])
                packet.writeEncoded(2) # 2 if is not on shop and 1 if is on shop 
                x += 1
            self.client.sendPacket(Identifiers.send.Open_Sales, packet.toByteArray())
             
        @self.packet(args=['readUTF', 'readUTF', 'readUTF', 'readByte'])
        async def Add_Sale(self, item_id, starting_date, ending_date, amount):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
            if item_id != "item id" and starting_date != "starting date" and ending_date != "ending date": 
                self.server.promotions.append([int(item_id.split(',')[0]),int(item_id.split(',')[1]),amount,int(ending_date),int(starting_date)])
                self.server.updatePromotions()
                self.server.loadPromotions()
                return await self.parsePacket(1,149,16,ByteArray())
            else:
                self.client.sendClientMessage("Invalid arguments", 1)
            
        @self.packet(args=['readInt'])
        async def Remove_Sale(self, id):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
            if not id in self.data: return
            for promotion in self.server.promotions:
                if promotion[0] == self.data[id][0] and promotion[1] == self.data[id][1]:
                    self.server.promotions.remove(promotion)
                    i = 0
                    while i < len(self.server.shopPromotions):
                        if self.server.shopPromotions[i][0] == promotion[0] and self.server.shopPromotions[i][1] == promotion[1]:
                            del self.server.shopPromotions[i]
                        i += 1
                    break
            self.server.updatePromotions()
            await self.parsePacket(1,149,16,ByteArray())
            
        @self.packet
        async def Ranking(self):
            data, sltdat = ByteArray().writeEncoded(1).writeEncoded(69), {}
            for str2 in ["CheeseCount","FirstCount","ShamanCheeses","RacingStats","BootcampCount","SurvivorStats","DefilanteStats"]:
                sldt, t = {}, 1
                data.writeEncoded(10)
                for rs in self.Cursor['users'].find().sort(str2,-1):
                    if isinstance(rs[str2],str): sldt[rs['Username']] = int(rs[str2].split(',')[2])
                    if t < 11:
                        if not isinstance(rs[str2],str): data.writeEncoded(t).writeUTF(rs['Username']).writeEncoded(rs[str2]).writeEncoded(t)

                    if rs['Username'] == self.client.playerName:
                        if not isinstance(rs[str2],str): sltdat[str2] = [t, rs[str2]]
                        if t > 11: break
                    t+=1
                
                if sldt != {}:
                    sldt, tr = {k: v for k, v in sorted(sldt.items(), key=lambda item: item[1],reverse=1)}, 1
                    for i in sldt:
                        if tr < 11: data.writeEncoded(tr).writeUTF(i).writeEncoded(sldt[i]).writeEncoded(tr)
                        if i == self.client.playerName: sltdat[str2] = [tr, sldt[i]]
                        tr+=1
            
            for str2 in ["CheeseCount","FirstCount","ShamanCheeses","RacingStats","BootcampCount","SurvivorStats","DefilanteStats"]: data.writeEncoded(sltdat[str2][1]).writeEncoded(sltdat[str2][0])
            self.client.sendPacket([144, 36], data.toByteArray())

            #elif CC == 9: # [144, 19] --> CC -> 9
            #    return
            
# [Chatta] Packet not implemented - C: 149 - CC: 23 - packet: b'\x00\x00\x00\x00\x01\x00\x00\x00\xc8\x00\x00\x00\x14\x00\x00\x00\x14'
# [Chatta] Struct Error - C: 176 - CC: 47 - packet: b"\xaa\xe3\x96\xa9BH\x80L\xde\xadq\x1a\xe4\tL\xd5m\x84\xf4\x83<\xf9-'!\xdf\xda\x00I\xcd\xd2j\x1b\xf2\xf4\x00\x97\xa1h\xe0\x8b7\xc4o\xce\xbb\x00zc\xd3\x94\xfe"
# [Chatta#0001] Struct Error - C: 5 - CC: 38 - packet: b'\x00\x03sex\x01\x01\x01\x01\x012\x00\x00\x00d\x00,\x01\x8a'

    async def parsePacketUTF(self, packet):
        values = packet.split('\x01')
        C, CC, values = ord(values[0][0]), ord(values[0][1]), values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                self.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                self.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                self.server.loop.call_later(10, self.client.sendConjurationDestroy, int(values[0]), int(values[1]))
                self.client.room.sendAll(Identifiers.old.send.Add_Conjuration, values)
                return

            elif CC == Identifiers.old.recv.Player.Snow_Ball:
                self.client.sendPlaceObject(0, 34, int(values[0]), int(values[1]), 0, 0, 0, False, True)
                return

            elif CC == Identifiers.old.recv.Player.Bomb_Explode:
                self.client.room.sendAll(Identifiers.old.send.Bomb_Explode, values)
                return

        elif C == Identifiers.old.recv.Room.C:
            if CC == Identifiers.old.recv.Room.Anchors:
                self.client.room.sendAll(Identifiers.old.send.Anchors, values)
                self.client.room.anchors.extend(values)
                return

            elif CC == Identifiers.old.recv.Room.Begin_Spawn:
                if not self.client.isDead:
                    self.client.room.sendAll(Identifiers.old.send.Begin_Spawn, [self.client.playerCode] + values)
                return

            elif CC == Identifiers.old.recv.Room.Spawn_Cancel:
                self.client.room.sendAll(Identifiers.old.send.Spawn_Cancel, [self.client.playerCode])
                return

            elif CC == Identifiers.old.recv.Room.Totem_Anchors:
                if self.client.room.isTotemEditor:
                    if self.client.tempTotem[0] < 20:
                        self.client.tempTotem[0] = int(self.client.tempTotem[0]) + 1
                        self.client.sendTotemItemCount(self.client.tempTotem[0])
                        self.client.tempTotem[1] += "#3#" + chr(1).join(map(str, [values[0], values[1], values[2]]))
                return

            elif CC == Identifiers.old.recv.Room.Move_Cheese:
                self.client.room.sendAll(Identifiers.old.send.Move_Cheese, values)
                return

            elif CC == Identifiers.old.recv.Room.Bombs:
                self.client.room.sendAll(Identifiers.old.send.Bombs, values)
                return

        elif C == Identifiers.old.recv.Balloons.C:
            if CC == Identifiers.old.recv.Balloons.Place_Balloon:
                self.client.room.sendAll(Identifiers.old.send.Balloon, values)
                return

            elif CC == Identifiers.old.recv.Balloons.Remove_Balloon:
                self.client.room.sendAllOthers(self.client, Identifiers.old.send.Balloon, [self.client.playerCode, "0"])
                return

        elif C == Identifiers.old.recv.Map.C:
            if CC == Identifiers.old.recv.Map.Vote_Map:
                if len(values) == 0:
                    self.client.room.receivedNo += 1
                else:
                    self.client.room.receivedYes += 1
                return

            elif CC == Identifiers.old.recv.Map.Load_Map:
                values[0] = values[0].replace("@", "")
                self.client.room.EMapLoaded = 0
                if values[0].isdigit():
                    code = int(values[0])
                    await self.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                    rs = await self.client.room.CursorMaps.fetchone()
                    if rs:
                        if self.client.playerName == rs["Name"] or self.client.privLevel >= 6:
                            self.client.sendPacket(Identifiers.old.send.Load_Map, [rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]])
                            self.client.room.EMapXML = rs["XML"]
                            self.client.room.EMapLoaded = code
                            self.client.room.EMapValidated = False
                        else:
                            self.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                    else:
                        self.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                else:
                    self.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                return

            elif CC == Identifiers.old.recv.Map.Validate_Map:
                mapXML = values[0]
                if self.client.room.isEditor:
                    self.client.sendPacket(Identifiers.old.send.Map_Editor, [""])
                    self.client.room.EMapValidated = False
                    self.client.room.EMapCode = 1
                    self.client.room.EMapXML = mapXML
                    await self.client.room.mapChange()
                return

            elif CC == Identifiers.old.recv.Map.Map_Xml:
                self.client.room.EMapXML = values[0]
                return

            elif CC == Identifiers.old.recv.Map.Return_To_Editor:
                self.client.room.EMapCode = 0
                self.client.sendPacket(Identifiers.old.send.Map_Editor, ["", ""])
                return

            elif CC == Identifiers.old.recv.Map.Export_Map:
                isTribeHouse = len(values) != 0
                if self.client.cheeseCount < 1500 and self.client.privLevel not in [6, 9] and not isTribeHouse:
                    self.client.sendMessage("<ROSE>You need 1500 cheeses to export a map.")
                elif self.client.shopCheeses < (40 if isTribeHouse else 1500) and self.client.privLevel < 6:
                    self.client.sendPacket(Identifiers.old.send.Editor_Message, ["", ""])
                elif self.client.room.EMapValidated or isTribeHouse:
                    if self.client.privLevel < 6:
                        self.client.shopCheeses -= 40 if isTribeHouse else 1500

                    code = 0
                    if self.client.room.EMapLoaded != 0:
                        code = self.client.room.EMapLoaded
                        await self.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [self.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        self.server.lastMapEditeurCode += 1
                        code = self.server.lastMapEditeurCode
                        await self.client.room.CursorMaps.execute("insert into Maps (Code, Name, XML, YesVotes, NoVotes, Perma, Del) values (?, ?, ?, ?, ?, ?, ?)", [code, self.client.playerName, self.client.room.EMapXML, 0, 0, 22 if isTribeHouse else 0, 0])
                    self.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                    self.client.enterRoom(self.server.recommendRoom(self.client.langue))
                    self.client.sendPacket(Identifiers.old.send.Map_Exported, [code])
                return

            elif CC == Identifiers.old.recv.Map.Reset_Map:
                self.client.room.EMapLoaded = 0
                return

            elif CC == Identifiers.old.recv.Map.Exit_Editor:
                self.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                self.client.enterRoom(self.server.recommendRoom(self.client.langue))
                return

        elif C == Identifiers.old.recv.Draw.C:
            if CC == Identifiers.old.recv.Draw.Drawing:
                if self.client.privLevel >= 9:
                    self.client.room.sendAllOthers(self.client, Identifiers.old.send.Drawing_Start, values)
                return

            elif CC == Identifiers.old.recv.Draw.Point:
                if self.client.privLevel >= 9:
                    self.client.room.sendAllOthers(self.client, Identifiers.old.send.Drawing_Point, values)
                return

            elif CC == Identifiers.old.recv.Draw.Clear:
                if self.client.privLevel >= 9:
                    self.client.room.sendAll(Identifiers.old.send.Drawing_Clear, values)
                return

        if self.server.isDebug:
            print("[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s" %(self.client.playerName, C, CC, repr(values)))
            with open("./include/logs/Errors/Debug.log", "a") as f:
                f.write("[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s\n" %(self.client.playerName, C, CC, repr(values)))
            f.close()
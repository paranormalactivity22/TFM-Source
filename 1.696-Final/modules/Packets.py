#coding: utf-8
import re, json, random, urllib.request, time as _time, struct, asyncio

loop = asyncio.get_event_loop()

# Game
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Lua import Lua
from collections import deque

class Packets:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor
        self.isOpenedHelpCommand = False
        self.temps = {}

    async def parsePacket(self, packetID, C, CC, packet):
        if C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTFBytes(packet.readShort())
                if isinstance(data, (bytes, bytearray)):
                    data = data.decode()
                loop.create_task(self.parsePacketUTF(data))
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                roundCode = packet.readInt()
                if roundCode == self.client.room.lastRoundCode:
                    p = ByteArray()
                    while (packet.bytesAvailable()):
                        p.writeShort(packet.readShort())
                        code = packet.readShort()
                        p.writeShort(code)
                        if (code != 1 and code != -1):
                            p.writeBytes(packet.readUTFBytes(16)).writeBoolean(True)
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Sync, p.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                packet2 = ByteArray().writeInt(self.client.playerCode).toByteArray() + packet.toByteArray()
                a, e = packet.readInt(), packet.readShort()
                #a, droiteEnCours, packet.readInt(), packet.readBoolean()
                #self.client.isMovingRight = droiteEnCours
                #self.client.isMovingLeft = gaucheEnCours
                if not self.client.posY == 0 and not self.client.posX == 0:
                    lasty, lastx = self.client.posY, self.client.posX
                else:
                    lasty, lastx = 0, 0
                self.client.posX, self.client.posY = packet.readInt() * 800 // 2700, packet.readInt() * 800 // 2700
                if not lasty == 0 and not lastx == 0:
                    if not lasty == self.client.posY or not lastx == self.client.posX:
                        self.client.ResetAfkKillTimer()
                        if self.client.isAfk:
                            self.client.isAfk = False
                self.client.velX, self.client.velY, self.client.isJumping = packet.readShort(), packet.readShort(), packet.readBoolean()
                self.client.room.sendAllOthers(self.client, Identifiers.send.Player_Movement, packet2)
                return
            
            elif CC == Identifiers.recv.Sync.Mort:
                self.temps = {}
                roundCode, loc_1 = packet.readInt(), packet.readByte()
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
                return

            elif CC == Identifiers.recv.Sync.Player_Position:
                direction = packet.readBoolean()
                self.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Shaman_Position:
                direction = packet.readBoolean()
                self.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Crouch:
                crouch = packet.readByte()
                self.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(self.client.playerCode).writeByte(crouch).writeByte(0).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Consumable_Object:
                if self.client.room.currentSyncName != self.client.playerName:
                    return
                posX = packet.readShort();
                posY = packet.readShort();
                velX = packet.readShort();
                velY = packet.readShort();
                code = packet.readShort();
                self.client.sendPlaceObject(0, code, posX, posY, 0, velX, velY, True, True);
                return
                
        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if self.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()
                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    self.client.room.addPhysicObject(-1, posX, posY, bodyDef)
                return

            elif CC == Identifiers.recv.Room.Shaman_Message:
                type, x, y = packet.readByte(), packet.readShort(), packet.readShort()
                self.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Convert_Skill:
                objectID = packet.readInt()
                self.client.Skills.sendConvertSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Demolition_Skill:
                objectID = packet.readInt()
                self.client.Skills.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                self.client.Skills.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
                self.temps = {}
                holeType, roundCode, monde, distance, holeX, holeY = packet.readByte(), packet.readInt(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == self.client.room.lastRoundCode and (self.client.room.currentMap == -1 or monde == self.client.room.currentMap or self.client.room.EMapCode != 0):
                    self.client.playerWin(holeType, distance)
                return

            elif CC == Identifiers.recv.Room.Get_Cheese:
                roundCode, cheeseX, cheeseY, distance = packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == self.client.room.lastRoundCode:
                    self.client.sendGiveCheese(distance)
                return

            elif CC == Identifiers.recv.Room.Place_Object:
                if not self.client.isShaman:
                    return
                if self.client.isShaman:
                    roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
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
                return

            elif CC == Identifiers.recv.Room.Ice_Cube:
                playerCode, px, py = packet.readInt(), packet.readShort(), packet.readShort()
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
                return

            elif CC == Identifiers.recv.Room.Bridge_Break:
                if self.client.room.currentMap in [6, 10, 110, 116]:
                    bridgeCode = packet.readShort()
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Defilante_Points:
                self.client.defilantePoints += 1
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("PlayerBonusGrabbed", (self.client.playerName, packet.readInt()))
                return

            elif CC == Identifiers.recv.Room.Restorative_Skill:
                objectID, id = packet.readInt(), packet.readInt()
                self.client.Skills.sendRestorativeSkill(objectID, id)
                return

            elif CC == Identifiers.recv.Room.Recycling_Skill:
                id = packet.readShort()
                self.client.Skills.sendRecyclingSkill(id)
                return

            elif CC == Identifiers.recv.Room.Gravitational_Skill:
                velX, velY = packet.readInt(), packet.readInt()
                self.client.Skills.sendGravitationalSkill(0, velX, velY)
                return

            elif CC == Identifiers.recv.Room.Antigravity_Skill:
                objectID = packet.readInt()
                self.client.Skills.sendAntigravitySkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Handymouse_Skill:
                handyMouseByte, objectID = packet.readByte(), packet.readInt()
                if self.client.room.lastHandymouse[0] == -1:
                    self.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    self.client.Skills.sendHandymouseSkill(handyMouseByte, objectID)
                    self.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                    self.client.room.lastHandymouse = [-1, -1]
                return

            elif CC == Identifiers.recv.Room.Enter_Room:
                self.temps = {}
                community, roomName = packet.readUTF(), packet.readUTF()
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
                return

            elif CC == Identifiers.recv.Room.Room_Password:
                roomPass, roomName = packet.readUTF(), packet.readUTF()
                roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
                if roomEnter == None or self.client.privLevel >= 7:
                    self.client.startBulle(roomName)
                else:
                    if not roomEnter.roomPassword == roomPass:
                        self.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                    else:
                        self.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Send_Music: 
                if not self.client.isGuest:
                    id = Utils.getYoutubeID(packet.readUTF())
                    if not id == None:
                        data = json.loads(urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails" %(id)).read())
                        if not data["pageInfo"]["totalResults"] == 0:
                            duration = Utils.Duration(data["items"][0]["contentDetails"]["duration"])
                            duration = 300 if duration > 300 else duration
                            title = data["items"][0]["snippet"]["title"]
                            if filter(lambda music: music["By"] == self.client.playerName, self.client.room.musicVideos):
                                self.client.sendLangueMessage("", "$ModeMusic_VideoEnAttente")
                            elif filter(lambda music: music["Title"] == title, self.client.room.musicVideos):
                                self.client.sendLangueMessage("", "$DejaPlaylist")
                            else:
                                self.client.sendLangueMessage("", "$ModeMusic_AjoutVideo", "<V>" + str(len(self.client.room.musicVideos) + 1))
                                self.client.room.musicVideos.append({"By": self.client.playerName, "Title": title, "Duration": str(duration), "VideoID": id})
                                if len(self.client.room.musicVideos) == 1:
                                    self.client.sendMusicVideo(True)
                                    self.client.room.isPlayingMusic = True
                                    self.client.room.musicSkipVotes = 0
                        else:
                            self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                    else:
                        self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                return

            elif CC == Identifiers.recv.Room.Music_Time:
                time = packet.readInt()
                if len(self.client.room.musicVideos) > 0:
                    self.client.room.musicTime = time
                    duration = self.client.room.musicVideos[0]["Duration"]
                    if time >= int(duration) - 5 and self.client.room.canChangeMusic:
                        self.client.room.canChangeMusic = False
                        del self.client.room.musicVideos[0]
                        self.client.room.musicTime = 0
                        if len(self.client.room.musicVideos) >= 1:
                            self.client.sendMusicVideo(True)
                        else:
                            self.client.room.isPlayingMusic = False
                return

            elif CC == Identifiers.recv.Room.Send_PlayList:
                packet = ByteArray().writeShort(len(self.client.room.musicVideos))
                for music in self.client.room.musicVideos:
                    packet.writeUTF(str(music["Title"].encode("UTF-8"))).writeUTF(str(music["By"].encode("UTF-8")))
                self.client.sendPacket(Identifiers.send.Music_PlayList, packet.toByteArray())
                return
             
        elif C == Identifiers.recv.Chat.C: ################
            if CC == Identifiers.recv.Chat.Chat_Message:
                message = packet.readUTF().replace("&amp;#", "&#").replace("<", "&lt;")
                if self.client.isGuest:
                    self.client.sendLangueMessage("", "$Créer_Compte_Parler")
                    return
                    
                elif message == "!lb":
                    self.client.sendLeaderBoard()
                    return
                    
                elif message == "!listrec":
                    self.client.sendPlayerRecords()
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
                        if message != self.client.lastMessage:
                            self.client.lastMessage = message
                            if self.client.isMumute:
                                self.client.room.sendAllChat(self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, 2)
                            else:
                                self.client.room.sendAllChat(self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.server.checkMessage(message))
                        else:
                            self.client.sendLangueMessage("", "$Message_Identique")
                        #else:
                            #self.client.sendLangueMessage("", "$Doucement")

                    if not self.client.playerName in self.server.chatMessages:
                        messages = deque([], 60)
                        messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                        self.server.chatMessages[self.client.playerName] = messages
                    else:
                        self.server.chatMessages[self.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                        
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("ChatMessage", (self.client.playerName, message))
                return

            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF()
                if self.client.privLevel < 2:
                    return
                self.client.sendAllModerationChat(type, message)
                return
                
            elif CC == Identifiers.recv.Chat.Commands:
                command = packet.readUTF()
                if _time.time() - self.client.CMDTime > 1:
                    loop.create_task(self.client.Commands.parseCommand(command))
                    self.client.CMDTime = _time.time()
                return

        elif C == Identifiers.recv.Player.C:
            if CC == Identifiers.recv.Player.Emote:
                emoteID, playerCode = packet.readByte(), packet.readInt()
                flag = packet.readUTF() if emoteID == 10 else ""
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
                return
                    
            elif CC == Identifiers.recv.Player.Langue:
                self.client.langueID = packet.readByte()
                if self.client.langueID:
                    self.client.langue = Utils.getLangues(self.client.langueID)
                else:
                    self.client.langue = "EN"
                return

            elif CC == Identifiers.recv.Player.Emotions:
                emotion = packet.readByte()
                self.client.sendEmotion(emotion)
                return

            elif CC == Identifiers.recv.Player.Shaman_Fly:
                fly = packet.readBoolean()
                self.client.Skills.sendShamanFly(fly)
                return

            elif CC == Identifiers.recv.Player.Shop_List:
                self.client.Shop.sendShopList()
                return

            elif CC == Identifiers.recv.Player.Buy_Skill:
                skill = packet.readByte()
                self.client.Skills.buySkill(skill)
                return

            elif CC == Identifiers.recv.Player.Redistribute:
                self.client.Skills.redistributeSkills()
                return

            elif CC == Identifiers.recv.Player.Report:
                playerName, type, comments = packet.readUTF(), packet.readByte(), packet.readUTF()
                self.client.modoPwet.makeReport(playerName, type, comments)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - self.client.PInfo[1]) >= 5:
                    self.client.PInfo[1] = _time.time()
                    self.client.sendPacket(Identifiers.send.Ping, ByteArray().writeByte(self.client.PInfo[0]).writeByte(0).toByteArray())
                    self.client.PInfo[0] += 1
                    if self.client.PInfo[0] == 31:
                        self.client.PInfo[0] = 0
                return

            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                self.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(self.client.playerCode).toByteArray())
                self.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(self.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if self.client.isShaman else 5).toByteArray())
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("PlayerMeep", (self.client.playerName))
                return

            elif CC == Identifiers.recv.Player.Bolos: 
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                imageID = (9 if id == 1 else 39 if id == 2 else 40 if id == 3 else 41 if id == 4 else 42 if id == 5 else 43)
                p = ByteArray()
                p.writeByte(24)
                p.writeByte(1)
                p.writeByte(2)
                p.writeUTF(str(self.client.playerCode))
                p.writeUTF(str(id))
                self.client.room.sendAll([16, 10], p.toByteArray())
                self.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(self.client.playerCode).writeUTF("x_transformice/x_aventure/x_recoltables/x_%s.png" % (9 if id == 1 else 39 if id == 2 else 40 if id == 3 else 41 if id == 4 else 42 if id == 5 else 43)).writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                self.client.sendPacket([100, 101], "\x01\x00")
                self.client.hasArtefact = True
                self.client.artefactID = imageID
                return

            elif CC == Identifiers.recv.Player.Vampire:
                self.client.sendVampireMode(True)
                return
                
            elif CC == Identifiers.recv.Player.Calendar: ###################
                playerName = packet.readUTF()
                player = self.server.players.get(playerName)
                if player != None:
                    p = ByteArray()
                    p.writeUTF(playerName)
                    p.writeUTF(player.playerLook)
                    p.writeInt(len(player.aventurePoints.values()))
                    p.writeShort(len(player.titleList))
                    p.writeShort(len(player.shopBadges))
                    p.writeShort(len(self.server.calendarioSystem.keys()))
                    for aventure in self.server.calendarioSystem.keys():
                        p.writeShort(9)
                        p.writeByte(1)
                        p.writeShort(aventure)
                        p.writeInt(self.server.calendarioSystem[aventure][0])
                        p.writeShort(self.client.aventurePoints[aventure] if aventure in self.client.aventurePoints.keys() else 0)
                        p.writeByte(1 if aventure < self.server.adventureID else 0)
                        p.writeByte(len(self.server.calendarioSystem[aventure][1:]))
                        for item in self.server.calendarioSystem[aventure][1:]:
                            items = item.split(":")
                            p.writeByte(items[0])
                            p.writeBoolean(True)
                            p.writeShort(items[1])
                            p.writeShort(items[2])
                            p.writeByte(self.server.getPointsColor(playerName, aventure, items[1], items[0], items[3]))
                            p.writeByte(1)
                            p.writeShort(self.server.getAventureCounts(playerName, aventure, items[1], items[0]))#items that you have idk bro sry i have to go cya
                            p.writeShort(items[3])
                        p.writeByte(len(self.server.calendarioCount[aventure]))
                        for item in self.server.calendarioCount[aventure]:
                            items = item.split(":")
                            p.writeByte(items[0])
                            p.writeBoolean(True)
                            p.writeShort(items[1])
                            p.writeShort(self.server.getAventureItems(playerName, aventure, int(items[0]), int(items[1])))
                    self.client.sendPacket([8, 70], p.toByteArray())
                return

        elif C == Identifiers.recv.Buy_Fraises.C:  ################
            print(C, CC)
            if CC == Identifiers.recv.Buy_Fraises.PayPal:
                isSteam = packet.readBoolean()
                if not isSteam:
                    p = ByteArray()
                    p.writeBoolean(True).writeInt(100).writeShort(69).writeInt(599).writeUTF("USD") #5.99 * 100 = 599 - price | 69 - amount
                    """
                    Are there any available offers (Boolean)
                    Unknown (Int)
                    Fraises (Short)
                    Money (Int), money = money / 100
                    Currency (String)
                    """
                    self.client.sendPacket([12, 12], p.toByteArray())
                else:
                    p = ByteArray()
                    p.writeByte(1).writeInt(99).writeShort(100).writeShort(0).writeShort(0).writeUTF("EUR") # First Item
                    p.writeByte(2).writeInt(499).writeShort(500).writeShort(0).writeShort(0).writeUTF("EUR") # Second Item
                    p.writeByte(3).writeInt(999).writeShort(1100).writeShort(1000).writeShort(100).writeUTF("EUR") # Third Item
                    p.writeByte(4).writeInt(1499).writeShort(1700).writeShort(1500).writeShort(200).writeUTF("EUR") # Fourth Item
                    p.writeByte(5).writeInt(1999).writeShort(2400).writeShort(2000).writeShort(400).writeUTF("EUR") # Fifth Item
                    """
                    ID (Byte)
                    Money (Int)
                    Fraises (Short)
                    Free Fraises (Short, Short)
                    """
                    self.client.sendPacket([100, 90], p.toByteArray())
                    
            elif CC == Identifiers.recv.Buy_Fraises.inGamePurchase:
                self.client.sendPacket([12, 2], ByteArray().writeUTF("https://bai.com").writeUTF("https://bai.com").toByteArray())
            
            elif CC == Identifiers.recv.Buy_Fraises.inSteamPurchase:
                
                return
            
            elif CC == Identifiers.recv.Buy_Fraises.Cancel_Transaction:
                return
                            
            return

        elif C == Identifiers.recv.Tribe.C:
            if CC == Identifiers.recv.Tribe.Tribe_House:
                if not self.client.tribeName == "":
                    self.client.startBulle("*\x03%s" %(self.client.tribeName))
                return

            elif CC == Identifiers.recv.Tribe.Tribe_Invite:
                playerName = packet.readUTF()
                player = self.server.players.get(playerName)
                if player != None and player.tribeName in self.client.invitedTribeHouses:
                    if self.server.rooms.get("*%s%s" %(chr(3), player.tribeName)) != None:
                        if self.client.room.roomName != "*%s%s" %(chr(3), player.tribeName):
                            self.client.startBulle("*%s%s" %(chr(3), player.tribeName))
                    else:
                        player.sendLangueMessage("", "$InvTribu_MaisonVide")
                return

        elif C == Identifiers.recv.Shop.C:
            if CC == Identifiers.recv.Shop.Equip_Clothe:
                self.client.Shop.equipClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Save_Clothe:
                self.client.Shop.saveClothe(packet)
                return
            
            elif CC == Identifiers.recv.Shop.Info:
                self.client.Shop.sendShopInfo()
                return

            elif CC == Identifiers.recv.Shop.Equip_Item:
                self.client.Shop.equipItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Item:
                self.client.Shop.buyItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Custom:
                self.client.Shop.customItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Item:
                self.client.Shop.customItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Clothe:
                self.client.Shop.buyClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Visu_Done:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                lookBuy = p.readUTF()
                look = self.server.shopOutfitsCheck[visuID].split(";")
                look[0] = int(look[0])
                count = 0
                if self.client.shopFraises >= self.client.priceDoneVisu:
                    for visual in look[1].split(","):
                        if not visual == "0":
                            item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                            item = int(item)
                            itemID = self.client.getFullItemID(count, item)
                            itemInfo = self.client.getItemInfo(count, item)
                            if len(self.client.shopItems) == 1:
                                if not self.client.Shop.checkInShop(itemID):
                                    self.client.shopItems += str(itemID)+"_" if self.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in self.client.custom:
                                        self.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in self.client.custom:
                                            self.client.custom.append(str(itemID))
                            else:
                                if not self.client.Shop.checkInShop(str(itemID)):
                                    self.client.shopItems += str(itemID)+"_" if self.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in self.client.custom:
                                        self.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in self.client.custom:
                                            self.client.custom.append(str(itemID))
                        count += 1
                        
                    self.client.clothes.append("%02d/%s/%s/%s" %(len(self.client.clothes), lookBuy, "78583a", "fade55" if self.client.shamanSaves >= 1000 else "95d9d6"))
                    furID = self.client.getFullItemID(22, look[0])
                    self.client.shopItems += str(furID) if self.client.shopItems == "" else "," + str(furID)
                    self.client.shopFraises -= self.client.priceDoneVisu
                self.client.Shop.sendShopList(False)

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Item:
                self.client.Shop.buyShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Equip_Shaman_Item:
                self.client.Shop.equipShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Custom:
                self.client.Shop.customShamanItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Shaman_Item:
                self.client.Shop.customShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Send_gift:
                self.client.Shop.sendShopGift(packet)
                return

            elif CC == Identifiers.recv.Shop.Gift_result:
                self.client.Shop.giftResult(packet)
                return

        elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if self.client.privLevel >= 7:
                    isOpen = packet.readBoolean()
                    self.client.modoPwet.openModoPwet(isOpen)
                    self.client.isModoPwet = isOpen    
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if self.client.privLevel >= 7:
                    playerName, closeType = packet.readUTF(), packet.readByte()
                    self.client.modoPwet.deleteReport(playerName, int(closeType))
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if self.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    isWatching = packet.readByte()
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
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if self.client.privLevel >= 7:
                    playerName, silent = packet.readUTF(), packet.readBoolean()
                    self.client.modoPwet.banHack(playerName, silent)
                return

            elif CC == Identifiers.recv.Modopwet.Change_Langue:
                if self.client.privLevel >= 7:
                    langue, modopwetOnlyPlayerReports, sortBy = packet.readUTF(), packet.readBoolean(), packet.readBoolean()
                    self.client.modoPwetLangue = langue.upper()
                    self.client.modoPwet.openModoPwet(self.client.isModoPwet, modopwetOnlyPlayerReports, sortBy)
                return
                
            elif CC == Identifiers.recv.Modopwet.Modopwet_Notifications:
                if self.client.privLevel >= 7:
                    isTrue = packet.readBoolean()
                    self.client.isModoPwetNotifications = isTrue  
                return    
                
            elif CC == Identifiers.recv.Modopwet.Chat_Log:
                if self.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    self.client.modoPwet.openChatLog(playerName)
                return

        elif C == Identifiers.recv.Login.C: ################
            if CC == Identifiers.recv.Login.Create_Account:
                playerName, password, email, captcha, url, test = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF()
                if True: #self.client.checkTimeAccount()
                    createTime = _time.time() - self.client.CRTTime
                    if createTime < 5.2:
                        #self.server.sendStaffMessage(7, "[<V>#</V>] The ip <J>"+self.client.ipAddress+"</J> is creating so fast accounts <FC><a event='banip:"+str(self.client.ipAddress)+"'>Suspect</a></FC>'")
                        self.client.transport.close()
                        return
                    
                    canLogin = False
                    for urlCheck in self.server.serverURL:
                        if url.startswith(urlCheck):
                            canLogin = True
                            break

                    if not canLogin:
                        self.client.sendServerMessage("[<J>Information</J>] Invalid login url of ip [<J>%s</J>] and name [<V>%s</V>]. Link is [<R>%s</R>] " %(self.client.ipAddress, playerName, url))
                        self.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Acesse pelo site: %s" %(self.server.serverURL[0])])
                        self.client.transport.loseConnection()
                        return


                    elif self.server.checkExistingUser(playerName):
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
                        self.Cursor.execute("insert into users values (%s, %s, %s, 1, 0, 0, 0, 0, %s, %s, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', %s, '', '', '', '', '', '', '', '', '', 0, 0, 0, 32, '', 0, '', '', 0, 0, '', 0, 0, 0, '', '', '0,0,0,0', '0,0,0,0', '0,0,0', '', '', 0, 0, 0, 0, '', 0, 0, '', '', '', %s, '', '24:0', 0, %s, '0.jpg', %s, '', 0, 0, %s)", [playerName, password, self.server.lastPlayerID, self.server.initialCheeses, self.server.initialFraises, Utils.getTime(), self.client.langue, self.client.computerLanguage, email, '{}'])
                        self.client.loginPlayer(playerName, password, "\x03[Tutorial] %s" %(playerName))
                        self.client.sendServerMessage("The ip %s created account <V>%s</V>. (<J>%s</J>)." %(self.client.ipAddress, playerName, self.client.langue))
                        if "?id=" in url:
                            link = url.split("?id=")
                            self.Cursor.execute("select IP from loginlog where Username = %s", [self.server.getPlayerName(int(link[1]))])
                            ipPlayer = self.Cursor.fetchone()[0]
                            self.Cursor.execute("select Password from users where Password = %s", [password])
                            passProtection = self.Cursor.fetchone()[0]
                    return
                else:
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeByte(0).writeByte(0).writeUTF(playerName).toByteArray())

            elif CC == Identifiers.recv.Login.Login:
                playerName, password, url, startRoom, resultKey = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readInt()
                #print(url)
                
                #authKey = self.server.authKey
                #for value in self.server.loginKeys:
                #    authKey ^= value
                #
                #if authKey != resultKey: 
                #    pass # aiotfm

                if not len(self.client.playerName) == 0:
                    self.client.sendServerMessage("[<J>Information</J>] Attempt to login multiple accounts. (IP:%s / Name:%s) " %(self.client.ipAddress, self.client.playerName))
                    self.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Attempt to login multiple accounts."])
                    self.client.transport.loseConnection()
                    return
                elif playerName == "" and not password == "":
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                else:
                    self.client.loginPlayer(playerName, password, startRoom)
                    return

            elif CC == Identifiers.recv.Login.New_Survey:
                if self.client.privLevel != 9:
                    return
                p = ByteArray()
                options = []
                description = packet.readUTF()
                for i in range(0, 6):
                    option = packet.readUTF()
                    if option != "":
                        options.append(option)
                p.writeInt(1).writeUTF("").writeBoolean(False).writeUTF(description)
                for option in options:
                    p.writeUTF(option)
                if len(options) > 0:
                    self.client.sendPacket(Identifiers.send.Survey, p.toByteArray())
                return

            elif CC == Identifiers.recv.Login.Survey_Answer:
                unknown = packet.readInt()
                optionID = packet.readByte()
                self.client.sendPacket([26, 17], ByteArray().writeByte(optionID).toByteArray())
                return
                
            elif CC == 18:
                print(4)
                return
                
            elif CC == Identifiers.recv.Login.Captcha:
                self.client.currentCaptcha = random.choice(list(self.server.captchaList))
                self.client.sendPacket(Identifiers.send.Captcha, self.server.captchaList[self.client.currentCaptcha][0])
                return

            elif CC == Identifiers.recv.Login.Player_MS:
                self.client.sendPacket(Identifiers.send.Player_MS)
                return

            elif CC == Identifiers.recv.Login.Dummy:
                if self.client.awakeTimer != None: self.client.awakeTimer.cancel()
                self.client.awakeTimer = self.server.loop.call_later(120, self.client.transport.close)
                return

            elif CC == Identifiers.recv.Login.Temps_Client:
                temps = packet.readUTF()
                self.client.sendPacket(Identifiers.send.Temps_Client, ByteArray().writeUTF(temps).toByteArray())
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                self.client.lastGameMode = mode
                self.client.sendGameMode(mode)
                return

            elif CC == Identifiers.recv.Login.Player_Info:
                info = packet.readShort()
                self.client.sendPacket([26, 28], ByteArray().writeByte(0).writeShort(info).toByteArray())
                return

            elif CC == Identifiers.recv.Login.Player_FPS:
                info = packet.readShort()
                self.client.sendPacket([26, 13], ByteArray().writeByte(0).writeShort(info).toByteArray())
                return

            elif CC == Identifiers.recv.Login.Undefined:
                self.client.sendPacket([26, 40])
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if (not self.client.isDead and self.client.room.currentMap in self.client.room.transformationMaps) or self.client.room.isFuncorp or self.client.hasLuaTransformations:
                    self.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(self.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readUnsignedByte(), packet.readUnsignedByte(), packet.readUTF()
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
                        print("[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, errorC, errorCC, error))
                        with open("./include/logs/Errors/Debug.log", "a") as f:
                            f.write("[%s] [%s] GameLog Error - C: %s CC: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, errorC, errorCC, error))
                        f.close()
                return
                
            elif CC == Identifiers.recv.Informations.Player_Ping:
                VC = (ord(packet.toByteArray()) + 1)
                if self.client.PInfo[0] == VC:
                    self.client.PInfo[2] = int((_time.time() - self.client.PInfo[1])*1000)
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                self.client.isNoShamanSkills = packet.readByte()
                self.client.shamanType = type
                self.client.sendShamanType(type, (self.client.shamanSaves >= self.server.minimumNormalSaves and self.client.hardModeSaves >= self.server.minimumHardSaves), self.client.isNoShamanSkills)
                return

            elif CC == Identifiers.recv.Informations.Letter: 
                playerName = Utils.parsePlayerName(packet.readUTF())[:-5]
                type = packet.readByte()
                letter = packet.readUTFBytes(packet.getLength())
                player = self.server.players.get(playerName)
                if (player != None): 
                    p = ByteArray()
                    p.writeUTF(self.client.playerName)
                    p.writeUTF(self.client.playerLook)
                    p.writeByte(type)
                    p.writeBytes(letter)
                    player.sendPacket(Identifiers.send.Letter, p.toByteArray())
                    self.client.sendLangueMessage("", "$MessageEnvoye")
                else:
                    self.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                return

            elif CC == Identifiers.recv.Informations.Send_gift:
                self.client.sendPacket(Identifiers.send.Send_gift, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info: # Receive computer's default language.
                self.client.computerLanguage = packet.readUTF()
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                self.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                self.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://localhost/tfm/info.php").toByteArray())
                return
                
        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Lua_Script:
                script = packet.readUTFBytes(int.from_bytes(packet.read(3),'big')).decode()
                if(self.client.privLevel in [9, 4] or self.client.isLuaCrew) or ((self.client.privLevel == 5 or self.client.isFunCorpPlayer) and self.room.isFuncorp) or self.server.isDebug:
                    if not self.client.isLuaAdmin:
                        if self.client.room.luaRuntime == None:
                            self.client.room.luaRuntime = Lua(self.client.room, self.server)
                        self.client.room.luaRuntime.owner = self.client
                        self.client.room.luaRuntime.RunCode(script)
                    else: self.client.runLuaScript(script)
                return

            elif CC == Identifiers.recv.Lua.Key_Board: 
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()
                mars = {87:87,38:87,65:65,37:65,68:68,39:68,83:83,40:83}
                chars = {87:"↑",65:"←",68:"→",83:"↓"}
                if key in mars and self.client.playerName in self.server.sonar:
                    end = _time.time()
                    key = mars[key]
                    if down:
                        self.temps[key] = end
                    else:
                        time = int((end - self.temps[key])*1000) - self.client.PInfo[2] # reduce the delay of ping
                        if time < 0: time = 0
                        time = str(time)
                        while len(time) < 4: 
                            time = " " + time
                        self.server.sonar[self.client.playerName].append(f"<BL>{chars[key]}<G> + <V>{time}</V> ms")
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("Keyboard", (self.client.playerName, key, down, posX, posY))
                return
            
            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()                    
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("Mouse", (self.client.playerName, posX, posY))
                return

            elif CC == Identifiers.recv.Lua.Popup_Answer:
                popupID, answer = packet.readInt(), packet.readUTF()
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("PopupAnswer", (popupID, self.client.playerName, answer))
                return

            elif CC == Identifiers.recv.Lua.Text_Area_Callback:
                textAreaID, event = packet.readInt(), packet.readUTF()

                if event in ["lbileri","lbgeri","lbkapat"]:
                    self.client.lbSayfaDegis(event=="lbileri", event=="lbkapat")
                    return 
                    
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("TextAreaCallback", (textAreaID, self.client.playerName, event))
                return

            elif CC == Identifiers.recv.Lua.Color_Picked: 
                colorPickerId, player, color, title = packet.readInt(), packet.readUTF(), packet.readInt(), packet.readUTF()
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("ColorPicked", (colorPickerId, player, color))
                return
            
        elif C == Identifiers.recv.Cafe.C or C == Identifiers.recv.Moludrome.C:
            if CC == Identifiers.recv.Cafe.Reload_Cafe:
                if not self.client.isReloadCafe:
                    self.client.Cafe.loadCafeMode()
                    self.client.isReloadCafe = True
                    self.server.loop.call_later(2, setattr, self.client, "isReloadCafe", False)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                self.client.Cafe.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                if self.client.privLevel >= 1:
                    message, title = packet.readUTF(), packet.readUTF()
                    self.client.Cafe.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                if self.client.privLevel >= 1:
                    topicID, message = packet.readInt(), packet.readUTF()
                    self.client.Cafe.createNewCafePost(0, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                self.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                if self.client.privLevel >= 1:
                    topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                    self.client.Cafe.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if self.client.privLevel >= 7:
                    postID = packet.readInt()
                    self.client.Cafe.deleteCafePost(postID)
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if self.client.privLevel >= 7:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    self.client.Cafe.deleteAllCafePost(topicID, playerName)
                return

            elif CC == Identifiers.recv.Moludrome.Mulodrome_Close:
                self.client.room.sendAll(Identifiers.send.Mulodrome_End)
                return

            elif CC == Identifiers.recv.Moludrome.Mulodrome_Join:
                team, position = packet.readByte(), packet.readByte()

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
                return

            elif CC == Identifiers.recv.Moludrome.Mulodrome_Leave:
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
                return

            elif CC == Identifiers.recv.Moludrome.Mulodrome_Play:
                if not len(self.client.room.redTeam) == 0 or not len(self.client.room.blueTeam) == 0:
                    self.client.room.isMulodrome = True
                    self.client.room.isRacing = True
                    self.client.room.noShaman = True
                    self.client.room.mulodromeRoundCount = 0
                    self.client.room.never20secTimer = True
                    self.client.room.sendAll(Identifiers.send.Mulodrome_End)
                    self.client.room.mapChange()
                return

        elif C == Identifiers.recv.Inventory.C:
            if CC == Identifiers.recv.Inventory.Open_Inventory:
                self.client.sendInventoryConsumables()
                return

            elif CC == Identifiers.recv.Inventory.Use_Consumable:
                id = packet.readShort()
                self.client.useConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                if id in self.client.equipedConsumables:
                    self.client.equipedConsumables.remove(id)
                else:
                    self.client.equipedConsumables.append(id)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Invite:
                playerName = packet.readUTF()
                self.client.tradeInvite(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Cancel_Trade:
                playerName = packet.readUTF()
                self.client.cancelTrade(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Add_Consusmable:
                id, isAdd = packet.readShort(), packet.readBoolean()
                self.client.tradeAddConsumable(id, isAdd)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Result:
                isAccept = packet.readBoolean()
                self.client.tradeResult(isAccept)
                return

        elif C == Identifiers.recv.Tribulle.C:
            if CC == Identifiers.recv.Tribulle.Tribulle:
                if not self.client.isGuest:
                    code = packet.readShort()
                    self.client.tribulle.parseTribulleCode(code, packet)
                return

        elif C == Identifiers.recv.Transformice.C:
            if CC == Identifiers.recv.Transformice.Invocation:
                objectCode, posX, posY, rotation, position, invocation = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readUTF(), packet.readBoolean()
                if self.client.isShaman:
                    showInvocation = True
                    if self.client.room.isSurvivor:
                        showInvocation = invocation
                    pass
                    if showInvocation:
                        self.client.room.sendAllOthers(self.client, Identifiers.send.Invocation, ByteArray().writeInt(self.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                    
                    if self.client.room.luaRuntime != None:
                        self.client.room.luaRuntime.emit("SummoningStart", (self.client.playerName, objectCode, posX, posY, rotation))
                return

            elif CC == Identifiers.recv.Transformice.Remove_Invocation:
                if self.client.isShaman:
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(self.client.playerCode).toByteArray())
                    if self.client.room.luaRuntime != None:
                        self.client.room.luaRuntime.emit("SummoningCancel", (self.client.playerName))
                return

            elif CC == Identifiers.recv.Transformice.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in self.client.shamanBadges:
                    self.client.equipedShamanBadge = str(badge)
                    self.client.sendProfile(self.client.playerName)
                return
                
            elif CC == Identifiers.recv.Transformice.NPC_Functions: 
                id = packet.readByte()
                if id == 4:
                    self.client.openNpcShop(packet.readUTF())
                else:
                    self.client.buyNPCItem(packet.readByte())
                return

            elif CC == Identifiers.recv.Transformice.Question: 
                pass

            elif CC == Identifiers.recv.Transformice.Map_Info:
                self.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount // 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    self.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1
                
                self.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount // 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    self.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return
                
            elif CC == Identifiers.recv.Transformice.Crazzy_Packet:
                type = packet.readByte()
                if type == 2:
                    posX = int(packet.readShort())
                    posY = int(packet.readShort())
                    lineX = int(packet.readShort())
                    lineY = int(packet.readShort())
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Crazzy_Packet, self.client.getCrazzyPacket(2,[self.client.playerCode, self.client.drawingColor, posX, posY, lineX, lineY]))

            elif CC == Identifiers.recv.Transformice.Full_Look: 
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")
                look = self.server.shopOutfitsCheck[visuID].split(";")
                look[0] = int(look[0])
                lengthCloth = len(self.client.clothes)
                buyCloth = 5 if (lengthCloth == 0) else (50 if lengthCloth == 1 else 100)

                self.client.visuItems = {-1: {"ID": -1, "Buy": buyCloth, "Bonus": True, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}, 22: {"ID": self.client.getFullItemID(22, look[0]), "Buy": self.client.getItemInfo(22, look[0])[6], "Bonus": False, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}}

                count = 0
                for visual in look[1].split(","):
                    if not visual == "0":
                        item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                        item = int(item)
                        itemID = self.client.getFullItemID(count, item)
                        itemInfo = self.client.getItemInfo(count, item)
                        self.client.visuItems[count] = {"ID": itemID, "Buy": itemInfo[6], "Bonus": False, "Customizable": bool(itemInfo[2]), "HasCustom": customID != "", "CustomBuy": itemInfo[7], "Custom": customID, "CustomBonus": False}
                        if self.client.Shop.checkInShop(self.client.visuItems[count]["ID"]):
                            self.client.visuItems[count]["Buy"] -= itemInfo[6]
                        if len(self.client.custom) == 1:
                            if itemID in self.client.custom:
                                self.client.visuItems[count]["HasCustom"] = True
                            else:
                                self.client.visuItems[count]["HasCustom"] = False
                        else:
                            if str(itemID) in self.client.custom:
                                self.client.visuItems[count]["HasCustom"] = True
                            else:
                                self.client.visuItems[count]["HasCustom"] = False
                    count += 1
                hasVisu = map(lambda y: 0 if y in shopItems else 1, map(lambda x: x["ID"], self.client.visuItems.values()))
                visuLength = reduce(lambda x, y: x + y, hasVisu)
                allPriceBefore = 0
                allPriceAfter = 0
                promotion = 70.0 / 100

                p.writeUnsignedShort(visuID)
                p.writeUnsignedByte(20)
                p.writeUTF(self.server.shopOutfitsCheck[visuID])
                p.writeUnsignedByte(visuLength)

                for category in self.client.visuItems.keys():
                    if len(self.client.visuItems.keys()) == category:
                        category = 22
                    itemID = self.client.getSimpleItemID(category, self.client.visuItems[category]["ID"])

                    buy = [self.client.visuItems[category]["Buy"], int(self.client.visuItems[category]["Buy"] * promotion)]
                    customBuy = [self.client.visuItems[category]["CustomBuy"], int(self.client.visuItems[category]["CustomBuy"] * promotion)]

                    p.writeShort(self.client.visuItems[category]["ID"])
                    p.writeUnsignedByte(2 if self.client.visuItems[category]["Bonus"] else (1 if not self.client.Shop.checkInShop(self.client.visuItems[category]["ID"]) else 0))
                    p.writeUnsignedShort(buy[0])
                    p.writeUnsignedShort(buy[1])
                    p.writeUnsignedByte(3 if not self.client.visuItems[category]["Customizable"] else (2 if self.client.visuItems[category]["CustomBonus"] else (1 if self.client.visuItems[category]["HasCustom"] == False else 0)))
                    p.writeUnsignedShort(customBuy[0])
                    p.writeUnsignedShort(customBuy[1])
                    
                    allPriceBefore += buy[0] + customBuy[0]
                    allPriceAfter += (0 if (self.client.visuItems[category]["Bonus"]) else (0 if self.client.Shop.checkInShop(itemID) else buy[1])) + (0 if (not self.client.visuItems[category]["Customizable"]) else (0 if self.client.visuItems[category]["CustomBonus"] else (0 if self.client.visuItems[category]["HasCustom"] else (customBuy[1]))))
                    
                p.writeShort(allPriceBefore)
                p.writeShort(allPriceAfter)
                self.client.priceDoneVisu = allPriceAfter
                self.client.sendPacket(Identifiers.send.Buy_Full_Look, p.toByteArray())
                return
                
        elif C == Identifiers.recv.Language.C:
            if CC == Identifiers.recv.Language.BotProtection:
                packet.decryptIdentification(self.server.packetKeys, str(self.client.verifycoder).encode())
                code = packet.readInt()
                st1 = packet.readUTF()
                code2 = packet.readInt()
                st2 = packet.readUTF()
                code3 = packet.readInt()
                if (code != self.client.verifycoder) or st1 != '--' or (code2 != self.client.verifycoder) or st2 != '---' or (code3 != self.client.verifycoder) or (not packet.bytesAvailable()):
                    self.client.transport.close()
                else: self.client.canlogin2 = True
                return
                
            elif CC == Identifiers.recv.Language.Set_Language:
                langue = packet.readUTF().upper()
                self.client.langue = langue
                if "-" in self.client.langue:
                    self.client.langue = self.client.langue.split("-")[1]
                self.client.langueID = Utils.getLangueID(self.client.langue.upper())
                self.client.sendPacket(Identifiers.send.Set_Language, ByteArray().writeUTF(langue).writeUTF(self.server.langs.get(self.client.langue.lower())[1]).writeShort(0).writeBoolean(False).writeBoolean(True).writeUTF('').toByteArray())
                return
                
            elif CC == Identifiers.recv.Language.Language_List:
                data = ByteArray().writeShort(len(self.server.langs)).writeUTF(self.client.langue.lower())
                for info in self.server.langs.get(self.client.langue.lower()):
                    data.writeUTF(info)

                for info in self.server.languages:
                    if info[0] != self.client.langue.lower():
                        data.writeUTF(info[0])
                        data.writeUTF(info[1])
                        data.writeUTF(info[2])
                self.client.sendPacket(Identifiers.send.Language_List, data.toByteArray())                                              
                return
                
        elif C == Identifiers.recv.Others.C:
            if CC == Identifiers.recv.Others.Open_Missions:
                self.client.missions.sendMissions()
                return

            elif CC == Identifiers.recv.Others.Change_Mission:
                missionID = packet.readShort()
                self.client.missions.changeMission(str(missionID))
                return
            
            elif CC == Identifiers.recv.Others.Cafe:
                topicID, delete = packet.readInt(), packet.readBoolean()
                self.client.Cafe.CheckMessageType(topicID, delete)
                return
            
            elif CC == Identifiers.recv.Others.Report_Cafe_Post:
                PostID = packet.readInt()
                TopicID = packet.readInt()
                self.client.Cafe.ReportCafeTopic(TopicID, PostID)
                return
            
            elif CC == Identifiers.recv.Others.View_Posts:
                playerName = packet.readUTF()
                self.client.Cafe.ViewCafeMessages(playerName)
                return
            
            elif CC == Identifiers.recv.Others.Send_Warnings:
                self.client.Cafe.sendWarnings()
                return
                
            elif CC == Identifiers.recv.Others.Attach_Player:
                self.client.room.sendAll(Identifiers.send.SetPositionToAttach, ByteArray().writeByte(-1).toByteArray())
                self.client.room.sendAll(Identifiers.send.AttachPlayer, ByteArray().writeInt(packet.readInt()).writeInt(1).writeInt(1*1000).toByteArray())
                return
            
            elif CC == Identifiers.recv.Others.NotAttach_Player:
                self.client.room.sendAll(Identifiers.send.SetPositionToAttach, ByteArray().writeByte(-1).toByteArray())
                return

            elif CC == Identifiers.recv.Others.Open_Sales:
                self.client.sendPacket([144, 29], ByteArray().writeUTF("").toByteArray())
                return

            elif CC == Identifiers.recv.Others.Add_Sale:
                return

        if self.server.isDebug:
            print("[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
            with open("./include/logs/Errors/Debug.log", "a") as f:
                f.write("[%s] Packet not implemented - C: %s - CC: %s - packet: %s\n" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
            f.close()
                

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
                    self.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                    rs = self.client.room.CursorMaps.fetchone()
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
                    self.client.room.mapChange()
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
                        self.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [self.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        self.server.lastMapEditeurCode += 1
                        code = self.server.lastMapEditeurCode
                        self.client.room.CursorMaps.execute("insert into Maps (Code, Name, XML, YesVotes, NoVotes, Perma, Del) values (?, ?, ?, ?, ?, ?, ?)", [code, self.client.playerName, self.client.room.EMapXML, 0, 0, 22 if isTribeHouse else 0, 0])
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
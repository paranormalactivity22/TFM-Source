#coding: utf-8
import re, json, random, urllib, traceback, time as _time, struct, asyncio

# Game
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Lua import Lua

# Library
from collections import deque
class Reactor1:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    def callLater(self, *args, **kwargs):
        return self.loop.call_later(*args, **kwargs)
    def callFromThread(self, func):
        return func()
reactor = Reactor1()


class Packets:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor
        self.isOpenedHelpCommand = False

    def parsePacket(self, packetID, C, CC, packet):
        #CC - 26, C - 6
        if C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTF()
                self.client.Packets.parsePacketUTF(data)
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                roundCode = packet.readInt()
                if roundCode == self.client.room.lastRoundCode:
                    packet2 = ByteArray()
                    while packet.bytesAvailable():
                        objectID = packet.readShort()
                        objectCode = packet.readShort()
                        if objectCode == -1:
                            packet2.writeShort(objectID)
                            packet2.writeShort(-1)
                        else:
                            posX = packet.readShort()
                            posY = packet.readShort()
                            velX = packet.readShort()
                            velY = packet.readShort()
                            rotation = packet.readShort()
                            rotationSpeed = packet.readShort()
                            ghost = packet.readBoolean()
                            stationary = packet.readBoolean()
                            packet2.writeShort(objectID).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(velX).writeShort(velY).writeShort(rotation).writeShort(rotationSpeed).writeBoolean(ghost).writeBoolean(stationary).writeBoolean(self.client.room.getAliveCount() > 1)
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Sync, packet2.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                roundCode, droiteEnCours, gaucheEnCours, px, py, vx, vy, jump, jump_img, portal, isAngle = packet.readInt(), packet.readBoolean(), packet.readBoolean(), packet.readUnsignedInt(), packet.readUnsignedInt(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readBoolean(), packet.readByte(), packet.readByte(), packet.bytesAvailable(),
                angle = packet.readUnsignedShort() if isAngle else -1
                vel_angle = packet.readUnsignedShort() if isAngle else -1
                loc_1 = packet.readBoolean() if isAngle else False

                if roundCode == self.client.room.lastRoundCode:
                    if droiteEnCours or gaucheEnCours:
                        self.client.isMovingRight = droiteEnCours
                        self.client.isMovingLeft = gaucheEnCours

                        if self.client.isAfk:
                            self.client.isAfk = False

                    self.client.posX = px * 800 / 2700
                    self.client.posY = py * 800 / 2700
                    self.client.velX = vx
                    self.client.velY = vy
                    self.client.isJumping = jump
                
                    packet2 = ByteArray().writeInt(self.client.playerCode).writeInt(roundCode).writeBoolean(droiteEnCours).writeBoolean(gaucheEnCours).writeUnsignedInt(px).writeUnsignedInt(py).writeUnsignedShort(vx).writeUnsignedShort(vy).writeBoolean(jump).writeByte(jump_img).writeByte(portal)
                    if isAngle:
                        packet2.writeUnsignedShort(angle).writeUnsignedShort(vel_angle).writeBoolean(loc_1)
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Player_Movement, packet2.toByteArray())
                return
            
            elif CC == Identifiers.recv.Sync.Mort:
                roundCode, loc_1 = packet.readInt(), packet.readByte()
                if roundCode == self.client.room.lastRoundCode:
                    self.client.isDead = True
                    if not self.client.room.noAutoScore: self.client.playerScore += 1
                    self.client.sendPlayerDied()

                    if self.client.room.getPlayerCountUnique() >= self.server.needToFirst:
                        if self.client.room.isSurvivor:
                            for playerCode, client in self.client.room.clients.items():
                                if client.isShaman:
                                    client.survivorDeath += 1

                                    if client.survivorDeath == 4:
                                        id = 2261
                                        sum = 10
                                        if not id in self.playerConsumables:
                                            self.playerConsumables[id] = sum
                                        else:
                                            count = self.playerConsumables[id] + sum
                                            self.playerConsumables[id] = count
                                        self.sendAnimZeldaInventory(1, id, sum)

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

        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if self.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()

                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    self.client.room.addPhysicObject(0, posX, posY, bodyDef)
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
                self.client.SkillSkills.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                self.client.Skills.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
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
                roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
                if self.client.room.isTotemEditor:
                    if self.client.tempTotem[0] < 20:
                        self.client.tempTotem[0] = int(self.client.tempTotem[0]) + 1
                        self.client.sendTotemItemCount(self.client.tempTotem[0])
                        self.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, dur]))
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
                        for player in self.client.room.clients.values():
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
                velX, velY = packet.readShort(), packet.readShort()
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
                community, roomName, isSalonAuto = packet.readByte(), packet.readUTF(), packet.readBoolean()
                if isSalonAuto or roomName == "":
                    self.client.startBulle(self.server.recommendRoom(self.client.langue))
                elif not roomName == self.client.roomName or not self.client.room.isEditor or not len(roomName) > 64 or not self.client.roomName == "%s-%s" %(self.client.langue, roomName):
                    if self.client.privLevel < 8: roomName = self.server.checkRoom(roomName, self.client.langue)
                    roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
                    if roomEnter == None or self.client.privLevel >= 7:
                        self.client.startBulle(roomName)
                    else:
                        if not roomEnter.roomPassword == "":
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
                url = packet.readUTF()
                id = Utils.getYoutubeID(url)
                print(id)
                if (id == None):
                    self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                else:
                    myUrl = urllib.urlopen("https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails")
                    data = json.loads(myUrl.read())
                    if data["pageInfo"]["totalResults"] == 0:
                        self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                    else:
                        duration = Utils.Duration(data["items"][0]["contentDetails"]["duration"])
                        duration = 300 if duration > 300 else duration
                        title = data["items"][0]["snippet"]["title"]
                        if (filter(lambda music: music["By"] == (self.client.playerName), self.client.room.musicVideos)):
                            self.client.sendLangueMessage("", "$ModeMusic_VideoEnAttente")
                        elif (filter(lambda music: music["Title"] == (title), self.client.room.musicVideos)):
                            self.client.sendLangueMessage("", "$DejaPlaylist");
                        else:
                            self.client.sendLangueMessage("", "$ModeMusic_AjoutVideo", str(len(self.client.room.musicVideos) + 1))
                            values = {}
                            values["By"] = self.client.playerName
                            values["Title"] = title
                            values["Duration"] = str(duration)
                            values["VideoID"] = id
                            self.client.room.musicVideos.append(values)
                            if (len(self.client.room.musicVideos) == 1):
                                self.client.sendMusicVideo(True)
                                self.client.room.isPlayingMusic = True
                                self.client.room.musicSkipVotes = 0

                    return

            elif CC == Identifiers.recv.Room.Send_PlayList:
                packet = ByteArray().writeShort(len(self.client.room.musicVideos))
                for music in self.client.room.musicVideos:
                    packet.writeUTF(music["Title"]).writeUTF(music["By"])
                self.client.sendPacket(Identifiers.send.Music_PlayList, packet.toByteArray())
                return

            elif CC == Identifiers.recv.Room.Music_Time:
                time = packet.readInt()
                if len(self.client.room.musicVideos) > 0:
                    self.client.room.musicTime = time
                    duration = self.client.room.musicVideos[0]["Duration"]
                    if time >= int(duration) - 5 and self.client.room.canChangeMusic:
                        self.client.room.canChangeMusic = False
                        del self.client.room.musicVideos[0]
                        self.client.room.musicTime = 1
                        if len(self.client.room.musicVideos) >= 1:
                            self.client.sendMusicVideo(True)
                        else:
                            self.client.room.isPlayingMusic = False
                            self.client.room.musicTime = 0
                return
            
        elif C == Identifiers.recv.Chat.C:
            if CC == Identifiers.recv.Chat.Chat_Message:
                #packet = self.descriptPacket(packetID, packet)
                message = packet.readUTF().replace("&amp;#", "&#").replace("<", "&lt;")
                if self.client.isGuest:
                    self.client.sendLangueMessage("", "$Créer_Compte_Parler")
                elif message == "!lb":
                    self.client.sendLeaderBoard()
                elif message == "!lsrec":
                    self.client.sendTotalRec()
                elif message == "!listrec":
                    self.client.sendListRec()
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
                            self.server.removeModMute(self.client.playerName)
                            if self.client.isMumute:
                                self.client.room.sendAllChat(self.client.playerCode, self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.client.langueID, 2)
                            else:
                                self.client.room.sendAllChat(self.client.playerCode, self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.client.langueID, self.server.checkMessage(message))
                        else:
                            self.client.sendModMute(self.client.playerName, timeCalc, muteInfo[0], True)
                            return
                    else:
                        if not self.client.chatdisabled:
                            if not message == self.client.lastMessage:
                                self.client.lastMessage = message
                                if self.client.isMumute:
                                    self.client.room.sendAllChat(self.client.playerCode, self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.client.langueID, 2)
                                else:
                                    self.client.room.sendAllChat(self.client.playerCode, self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.client.langueID, self.server.checkMessage(message))
                                reactor.callLater(0.9, self.client.chatEnable)
                                self.client.chatdisabled = True
                            else:
                                self.client.sendLangueMessage("", "$Message_Identique")
                        else:
                            self.client.sendLangueMessage("", "$Doucement")

                    if not self.client.playerName in self.server.chatMessages:
                        messages = deque([], 60)
                        messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                        self.server.chatMessages[self.client.playerName] = messages
                    else:
                        self.server.chatMessages[self.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                return
                ##else:
##                    self.client.sendMessage("<ROSE>You need 3 cheeses to speak.")

           
            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF()
                priv = self.client.privLevel
                if self.client.isLuaCrew or self.client.isMapCrew or self.client.isFashionSquad or self.client.isFunCorpPlayer:
                    self.client.sendAllModerationChat(type, message)
                    return
                if priv < 2: 
                    return
                self.client.sendAllModerationChat(type, message)
                return
                
                        
        # 2: arbitre,
        # 3: modo,
        # 7: mapcrew,
        # 8: luateam,
        # 9: funcorp,
        # 10: fashionsquad

            elif CC == Identifiers.recv.Chat.Commands:
                command = packet.readUTF()
                try:
                    if _time.time() - self.client.CMDTime > 1:
                        self.client.Commands.parseCommand(command)
                        self.client.CMDTime = _time.time()
                except Exception as e:
                    with open("./logs/Errors/Commands.log", "a") as f:
                        traceback.print_exc(file=f)
                        f.write("\n")
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
                        player = filter(lambda p: p.playerCode == playerCode, self.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(14, flag, False, False)
                            player.sendPlayerEmote(15, flag, False, False)

                    elif emoteID == 18:
                        self.client.sendPlayerEmote(18, flag, False, False)
                        self.client.sendPlayerEmote(19, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, self.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(17, flag, False, False)
                            player.sendPlayerEmote(19, flag, False, False)

                    elif emoteID == 22:
                        self.client.sendPlayerEmote(22, flag, False, False)
                        self.client.sendPlayerEmote(23, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, self.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(22, flag, False, False)
                            player.sendPlayerEmote(23, flag, False, False)

                    elif emoteID == 26:
                        self.client.sendPlayerEmote(26, flag, False, False)
                        self.client.sendPlayerEmote(27, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, self.server.players.values())[0]
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
                langue = Utils.getTFMLangues(self.client.langueID)
                self.client.langue = langue
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
                    self.client.lastping = not self.client.lastping
                    #self.client.sendPacket(Identifiers.send.Ping, self.client.PInfo[0])
                    self.client.sendPacket(Identifiers.send.Ping, ByteArray().writeByte(self.client.PInfo[0]).writeBoolean(self.client.lastping).toByteArray())
                    self.client.PInfo[0] += 1
                    if self.client.PInfo[0] == 31:
                        self.client.PInfo[0] = 0
                return

            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                self.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(self.client.playerCode).toByteArray())
                self.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(self.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if self.client.isShaman else 5).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Bolos:
                #print repr(packet.toByteArray())
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                #print("ID: "+str(id)+ ", ID da aventura: "+str(sla2)+ ", Sla: "+str(sla))
                #.client.winEventMap()
                if not self.client.hasBolo:
                    p = ByteArray()
                    p.writeByte(52)
                    p.writeByte(1)
                    p.writeByte(2)
                    p.writeUTF(str(self.client.playerCode))
                    p.writeUTF(str(id))
                    self.client.room.sendAll([16, 10], p.toByteArray())
                    self.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(self.client.playerCode).writeUTF("x_Sly/x_aventure/x_recoltables/x_"+str((1 if id == 1 else 0))+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    self.client.sendPacket([100, 101], "\x01\x01")
                    #self.client.room.sendAll([5, 53], ByteArray().writeByte(type).writeShort(id).toByteArray())
                    #self.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(self.client.playerCode).writeUTF("x_Sly/x_aventure/x_recoltables/x_"+1 if self.server.adventureID == 52 else 0+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    #self.client.sendPacket([100, 101], "\x01\x00")
                    self.client.hasBolo = True
                    if not self.client.isGuest:
                        if id == 1:
                            self.client.selfGet = True
                return

            elif CC == Identifiers.recv.Player.Vampire:
                if self.client.room.isSurvivor:
                    self.client.sendVampireMode(True)
                return

        elif CC == Identifiers.recv.Player.Calendar:
                pass
                return

        elif C == Identifiers.recv.Buy_Fraises.C:
            if CC == Identifiers.recv.Buy_Fraises.Buy_Fraises:
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

            elif CC == Identifiers.recv.Tribe.Bot_Bolo:
                pass
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
                look = self.server.newVisuList[visuID].split(";")
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
                    self.client.visuDone.append(lookBuy)
                else:
                    self.sendMessage("yarrak")
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

            elif CC == Identifiers.recv.Shop.Send_self:
                self.client.Shop.sendself(packet)
                return

            elif CC == Identifiers.recv.Shop.self_Result:
                self.client.Shop.selfResult(packet)
                return

        elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if self.client.privLevel >= 7:
                    isOpen = packet.readBoolean()
                    if isOpen:
                        self.client.modoPwet.openModoPwet(True)
                    else:
                        self.client.modoPwet.openModoPwet(False)
                        
                    self.client.isModoPwet = isOpen    
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if self.client.privLevel >= 7:
                    playerName, closeType = packet.readUTF(), packet.readByte()
                    self.client.modoPwet.deleteReport(playerName,int(closeType))
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if self.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    if not self.client.playerName == playerName:
                        roomName = self.server.players[playerName].roomName if playerName in self.server.players else ""
                        if not roomName == "" and not roomName == self.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            self.client.isHidden = True
                            self.client.sendPlayerDisconnect()
                            self.client.startBulle(roomName)
                            self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(playerName).writeBoolean(True).toByteArray())
                            self.server.players[playerName].followed = self.client
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if self.client.privLevel >= 7:
                    playerName, iban = packet.readUTF(), packet.readBoolean()
                    self.client.modoPwet.banHack(playerName,iban)
                return

            elif CC == Identifiers.recv.Modopwet.Change_Langue:
                if self.client.privLevel >= 7:
                    langue,modopwetOnlyPlayerReports,sortBy = packet.readUTF(),packet.readBoolean(),packet.readBoolean()
                    self.client.modoPwetLangue = langue.upper()
                    self.client.modoPwet.openModoPwet(self.client.isModoPwet,modopwetOnlyPlayerReports,sortBy)
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


        elif C == Identifiers.recv.Login.C:
            if CC == Identifiers.recv.Login.Create_Account:
                #packet = self.descriptPacket(packetID, packet)
                playerName, password, email, captcha, url, test = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF()
                if self.client.checkTimeAccount():
                    createTime = _time.time() - self.client.CRTTime
                    if createTime < 5.2:
                        self.server.sendStaffMessage(7, "[<V>#</V>] The ip <J>"+self.client.ipAddress+"</J> is creating so fast accounts <FC><a href='banip:"+str(self.client.ipAddress)+"'>Suspect</a></FC>'")
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
                        tag = "0000"
                        tag = "".join([str(random.choice(range(9))) for x in range(4)])
                        playerName += "#" + tag
                        self.client.sendAccountTime()
                        self.server.lastPlayerID += 1
                        self.Cursor.execute("insert into users values (%s, %s, %s, 1, 0, 0, 0, 0, %s, %s, 0, 0, 0, 0, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', %s, '{}', '', '', '', '', '', '', '', '', 0, 70, 0, 0, '', 0, '', '', 0, 0, '', 0, 0, 0, '', '', '0,0,0,0', '0,0,0,0', '23:20', '23', 0, 0, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, %s, '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', 0, 0, 0, '', 0, 1, %s, '', 0, 0, 'Little Mouse', 0, 0, %s)", [playerName, password, self.server.lastPlayerID, self.server.initialCheeses, self.server.initialFraises, Utils.getTime(), self.client.langue, email, '{}'])
                        #self.Cursor.execute("insert into DailyQuest values (%s, '237129', '0', '20', '0', '20', '1')", [self.server.lastPlayerID])
                        self.client.loginPlayer(playerName, password, "\x03[Tutorial] %s" %(playerName))
                        self.client.sendServerMessage("The ip %s created account <V>%s</V>. (<J>%s</J>)." %(self.client.ipAddress, playerName, self.client.langue))
                        self.server.updateConfig()
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
                #packet = self.descriptPacket(packetID, packet)
                playerName, password, url, startRoom, resultKey, byte = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readInt(), packet.readByte()
                #authKey = self.client.authKey
                #print(url)

                if not len(self.client.playerName) == 0:
                    self.client.sendServerMessage("[<J>Information</J>] Attempt to login multiple accounts. (IP:%s / Name:%s) " %(self.client.ipAddress, self.client.playerName))
                    self.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Attempt to login multiple accounts."])
                    self.client.transport.loseConnection()
                    return
                elif playerName == "" and not password == "":
                    self.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                else:
                    self.client.loginPlayer(playerName, password, startRoom)
                #else:
                    #self.client.sendServerMessage("[<J>Information</J>] Invalid login auth key. (IP:%s / Name:%s) " %(self.client.ipAddress, playerName))
                    #self.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Invalid login auth key."])
                    #self.client.transport.loseConnection()
                    return

            elif CC == Identifiers.recv.Login.Player_FPS:
                return
            
            
            #elif CC == Identifiers.recv.Login.Survey:
                

            elif CC == Identifiers.recv.Login.Captcha:
                captchas = {
                    "IELR": b'\x00\x00\x02$x\x9c\xed\x951H#Q\x10\x86\x17\xddhTP\xc4\x10ml4M\n\xaf\xb10\x07\x82\x10\xad$\xa6\xd5\xc6B\x85\xc3F\x90\xa4\xf0\xe0\n\x13\xbd\xf6b\xb9\x16\xa6P\x11!(\xd8\x19HL\xa1wVZX\xe8\xa9UPA\x04\xe5\n\x89\x1c\x87\xfa\xfc\x9f\x99\x07{\xcbK\\\xa2\xae\x88;\xf0\xb1;\xf3\xdeL\xe6\xcf\xbe\x9dU\x94N\xc5\xa5\xae)\xb6\xd9\xf6\x01\xac\x8a1\xf6\xd6=Xe\\\xeb\x19hz\xc7\x9a\x1d&{\xaf\x05|\xe3E<\x1e\x8f!G\xf8\x85\xd0\xe7\x9cJ\xea}\x96\xe4\xdc\x82\x1b\xb0\x01\x9aK\xd4\xa3\xb7r\xf4\xd9\x06F\xc0,\xd8\x05\x7f\x80\x19\xcd\x01\xea)\xe1\xf1x\xae\xb0\x7f\xd0\xef\xf7?\xa5W\xe4,I\xea\r\x15\xc9\xe5\xfc*A_+\xfa\x1a\x00?\xc0\x16\xb8\x06\xbf\xc1\x02\x18\x03\x1d\xa0\xd2\xe4\xf3\xfdF}\x8c\x80\x19\xe4l\xa7R)\xee\x0f\x9a\xc8\x19\x95\xac\xcd\xd3\x9a1\xdfC\xf1\xbfO\xf4\xc3\xdf\xa9>0\r\x92\xe0\x12\x9c\x80U0\x01\xfc\xfc\x0c>\xe3\xbd[\xa1>\xba@3\xea\xdc\xc3X&\x93\x99K\xa7\xd3\xde\x02uEN\xbbdm\x87\xd6zu\xb1z\x10\xa5\xf8\xb1.^\x87\xfa\xdd\xe0+\xe99%}\xeb`\x8at7\xbe\xf0L9W\xf2\xef\x97J\xfe\x85\xdb\xedf\xc1`\x90i\x9a\xc6\xb2\xd9\xec#\xfc\x1e\xb1\x1a\xfam\x9es#\xa9UF\xb5\xa4g\xd9\xe9t\xde\xf9|>-\x99L.\xa2\xce!\x9d\xcbM:\xa7\xfd\xa0\xe5\x95\xe7\xa5\x98;\xc7\x06\xff?\xbc^/\x0b\x85B\x8c\x9f\xf3g\xda~.\x97\xd3p\x1d\xa6ySn\xf1\xf7@\xcc\x9d\xe5\x02\xbe\xd1*\xd0\x9f\xd83)Y\x17\xb3*A>\xff\xff6(\xd6\xe5r\xb9^\xa8\xed\x92M\xcc\x9d\t\x83\xff\xc5DN@\xb2&f\xd5\xb8.\xd6\xa2\xe4\xcf\xf8\x9e\xaa\xaa\x92\x14KM\xcc\x9d\xc7g\x16\x89D^\x9b\xa3p8\xfc\x1d\xd7\x1eP\r\xac\xd6{Nz\x1b\x0c~\xb1oo\xb1=\xfc9\xfeS\xf2sKo\x9f\xf8\xba\xc3\xe18\xc0,\x98\x86\xce-p\r~\x82\xb7\xd4o\xa5U\xc5b\xb1\xeeh4j\xeb\xb7\xf5\xdb\xfam\xfdW\xa0B\xa2\xf9\x01\x99eX\xd9',
                    "TCQC": b'\x00\x00\x03ux\x9c\xed\x96\x7fHSQ\x14\xc7/2\xb5$\x16\x99\x93\x122\x02\x83\xd5\x04\xdb\x04\x15T\x86D\x12#h\xd4\x1f1\xe6\x1f\x8ac\x7fH\xea\x1f\x13\xa2\x10t\xfe*J"\xa9\x7f4K\xa2\x02\x19aj\x85\x89F\x90\xa6E\x7f,\n\xcc\xa4Y\x16Y&\xc6\x9an\xc5\xe6v\xfb^\xde\x1d=\xc66\xcb\x1f[R\x07>\xbc\xb7\xfb\xce=;\xdf{\xde=\xf7\x11\x92G\x92$\xddd\x9d\x9b\xac\xa9\xa9)\xaf\xb6\xb6\xd6\x00\xce\x81;`\x02\xcc\x03\t\x88v~\xcb\xb1\xd8\xd6\xd6\xd6=\xf5\xf5\xf5Z\xe4\x7f\xc2l6w\xe0:\x02\xbe\x829~\x7f\x95?;\x0c\xe4\xb8gs\xa2\x9d\xf7R\x16\xaaV\xdf\xc1k\xd0\xcb\xc7K\xa1\x89\xf9%\xad\x83\xfa\xfd\xafU\xf4kE\xc5\xc4\xc6\xc6\xd2\x801f\xfb@\x97D"YHNN^\x94\xcb\xe5\xdf\xd4j\xf5\xcb\x92\x92\x92\xd1\x9a\x9a\x1a\x7f\xad\x9eUWW\xbf(..\x9e+((`>\x0b2\x99\xac\x1bs\xd2E\xff\xc5\xe2\xdc\x02\x0e\xe0\x06\x1f\xc1Y \x89\x90V"\xd6\x96\x98\x98H\x91wX\xca\xcb\xcb\xa9N\xa7\xa3\x85\x85\x85T\xa5R\xdd\xc8\xc8\xc8`\xb5\xca\xc4\xfc\x19\x12\xb0v\x1c\x17`\xcf\x8f\x81\xc5\x10>g"\xa8\x97Y\x0cr~e2\x99h~~~Ovv\xb6\x86RZ\t\xae\xcd\xcc\xccx\xfb\xfb\xfb\xe9\xe4\xe4$\xf5z\xbd\xa3n\xb7\xbb\x0e\xd7:\xd4\xd2\x1d\x1f\x1fo\xc3\xdc\x04"\xd4\x89\xe5\xfd\x00\xec\xe51w\x82\xfb||\x04\xfc\x10i\xdb\xc2\xfe\x13\xe8\x88Pg[D\xd5\x12R\x89}\xf5\xa9\xa2\xa2\x82\xfa|\xbeY\xbb\xdd\xde\x07\xad\x17\xc1\xa3\x96\x96\x16\xaa\xd1h\xba\xb3\xb2\xb26\xe3\xf7\x01p\x1a<\x01\x0e0\x08\xfa,\x16\x0b\xcd\xc9\xc9\x19\xc1^\x08\x8c+#\x82F\x0f\xbf^\x8f\xb0\xae`\x96\x80\xda\xbe\x03\xe3z\xbd\x9e\x0e\x0f\x0f\xe7\x8a\x9e\xbd%B\x9e\x99A\xe6I\xa1\xf5\x10\x98noo\xa7V\xabu\xc1\xe3\xf1\xdc\xc3o\x13P\x81\x18\x06\x9f\xef\x0b\x13\'\x1a\xb6\xa9\xac\xac\xcc\xdb\xd8\xd8\xe8mhh\x88\x11\x8d\xfb\xf7[8\xf3\xbf\xa7I\xd3\xd3\xd3G\xa0\xf1\x12\x18\x03s\xe0\xf1\xd4\xd4\x14\xdb\xf3>\x85B\xb1T\x9cH\x1a[wV\xdb1\xadV+\x1e\xf7k\x91\x05\xf8g\x13\xa1\xc7Z\x82\xf8\xb0\xfdi\x06\xbb\xb0\xef\xdf\x1b\x0c\x06\xda\xd6\xd6\xe6\xb3\xd9l\x14\xbd\xe0\xb6\xd3\xe94b\x1dv\x83\xc08\x91\xb4\xd2\x94\x94\x14:??\xdf!\x95J\xc5\xe3\xac\xff\xb0\xc4\xee\x82\xedD\xe81\x07\xc9\xaf\xfetA\xe4\xc3z\xd3\x0e`$\xc2{1\xcb\xc7\x1f\xfa}RSS\x9fWUUY\x1c\x0e\xc7\x07\xe8\x9du\xb9\\\xce\xce\xceN\x8a3\xec\x8aR\xa9\x8c\x88Pn\x83EEEthhH\x170\x9eK\x82\x9f\x1f\x8c\t\xb0\x95\x08g\xaa+\x84\xcf\x18\x90\x86\x8a\x93\x96\x96F\x8dF\xa3\xa3\xa7\xa7\xe7\x0bz\xfe\x1b\xac\xc1e\xa0\x03\xdbx\xfd\xd7\xca>\xb3>\x8c\xef\xbe\xf4 \xcfX\xae\xac>\xec\xbdeu\x1b\x07\xcdD8S\xfc\xc6\xe6\xf5r\x1fV\xd7\x93`\x80\x08\xba\x9a\x7f3\x8e\x02\x1a\x8f\x83.\xbe\xf7\xc7x/8\n\xb6\xae\xb2\xfea\xc4\xdb\xbf\xca17\x80\x9b@\xbf\x8c\xb9\xac\xb7+y\xafg=\xdf\x0e\xac\xe0<?\x13\xa4+\xc85\x8e\xaf\xe7\xc65~\x87Vb\x12\xe4\x96\x03N\x81\x01~\xf6?\xe5\xdf\x02\xec\x9b \xe1\x0fs\x8f\xfb\x8b\xb5\x063\x96\xaf\x1a\xd4\xb2o"^\xaf\xf5\xa6a%\xf6/i\rg?\x01\xdd\x8b\xa0\x91',
                    "EYSH": b'\x00\x00\x036x\x9c\xed\x95_HSa\x18\xc6\xcf\xdc\xc2\x90%\x14\x1b\x81\x82\x18\x88\x19B\x82\xa1\x10\x8e\xc0.Db\xe0\xd8\x85%.\x89\x16A\x0b\x9b\xa0lA\xea\x94\xd9.\xb6\x0b\xa3\rBhV\x90\xa4\x15\xae\xdaM7N\x82\x16h\xe1\xc5\x88\xc0lhH\xb9\xf0O\x92C\xd7\xd8\xfaz>\xfdN[\x87\xcdMB#\xdb\x03?\xf6\x9d\xf7|\xe7\xbc\xe7\xd9\xfb\x9e\xf7p\x9c\x82\x93I\x9ep\x19e\x94QF\xff\xa8r\x01\xd9\x04\xaa\x17l\xad\x14\\{\x9a\xc5\xef\xc5\xdd\xcb\x01\x96A\x18\xcc\x02\x93 \xcf\xac\xe0\x1e\x07Y\xfc\xd3\x1f\xfa\x90tuu\xa5\xb3O\xc9\xf2\x11\x89D\x92\xcco-[\xbf\x03Y,\x96\x0f\x96\xc04\x90\xb2\xd8\xe3\x04\xd7S\xae\xc7\xe5\x19\x10\xe4W\xb3\xf8\x834}\xc9-\x16\x8b\x02\xde.\x00\x1bp\x83\xf7`\x05\xa4\xe3\xf9\x1a\xf3\xba\xdc\xde\xde~`\x93\xfd>\xf6\\W\xd8\xf1(;>\x1e\xb7\'\xc2b\xc7\xd8q5\xb7Q\xe79>\x0f\xd0\t\xee\xebH\x10\xdf\xd3\xd7\xd7w\xc4l6\xab\xf0<\xc6\xee\xee\xee;\xf8}\x05\x96\xc0"[\xf7\xb3su\xa0\x04kzM*\xafT\xeb5\xc9\xc9\xc9Y\x1b\x1c\x1c\xec\xb1\xdb\xed\xc9\xf6\x9de\xcf\xf5\x05t\xb0\xb5Y\xb0\xc7\xcf\xe2U\xc9\xf2\x80\x8a\xb8\x18\xad\xd5\xdb\xa2\xa2"R^^~\xbf\xb9\xb9\x99\xaf\xd5\x1a\x98\x04\xcfX\r\xb5\xf0Dk*K\xb3g7\xd3\x1c{\x0e\xd2\xda\xdaJ\xacV+\x11\x89D\xf1\xbd\xcc\x8b\xf6\xf1G.\xd6\xa3o\xb8Xo\xf3\xa2\xf5\x9c\xe7b\xfdY\xc2\xc5j\xf5\xb5\xb4\xb4\x94(\x14\n\xa2R\xa9\x88V\xab%F\xa3q\x1d\xac\xa3\x88]\x85\x97\xad\xd6j\xab\xfamVQ\x9f\xd4o[[["\xbfT-,\x1e\x04\xc5\x82s\xfc{u\x19\x1e^666\x865\x1a\rA\xcd\xc2\x9d\x9d\x9dS&\x93\x89444\x90\x9a\x9a\x1aZKRPP@{\x8a\xcf3\xb2\x1d\xe6\x12\x88\x9f!\xfc\xac\xb08\x1c\x0e2<<\xec\'\x84<\x07v\xa0\x07\xa7@18SXXH\xe4r\xf9Heee\xaa\xf7\xea\x9cN\xa7#2\x99l^,\x16\xf3y\x1e\n\xf2\xabX\xdc\xbaC~\xf9\x19r\x91\x1d\xd3yER\xd1\xdb\xdb\xbb\xeat:?\xb8\\\xaeQ\x8f\xc7s{bbB\x1f\x08\x04\x82J\xa5\xf2{YY\xd9\t\xb5Z-\xc2\x7fS\xcd\xc5z\x81\xcf\xd3"\xc8\xcf\xcf\x01\xd5\x0e\xf9M\xf8\xfd\x88\xfb.\t\xe5\x92J\xa5$//O\x8f\x9e\xad\x83\xa7K\xc0\x0c\x9c 0>>N|>\x1fYXX \xa1P\x88\xcc\xcc\xcc\x10\xaf\xd7;9666544D\xdfU\xb3\xdb\xed>\x89\xbd% \x17\xf0\xf9\xf7\xef\x90\xdf_\xb3*\t\xc9\xf6K\x13\x9c\xa3\xcf|\x93\xdb\x98\xdf\x91\xec\xec\xec\x00\xe6\xee\xdd\xa6\xa6\xa6\xfaH$\xf2\xcd`0Dm6\xdb@4\x1a\xf5\xc0\xe7$X\x01?\x82\xc1`\xd8\xef\xf7\x8fb=\x00\xac\xa0\x05\xd4\x83*p\x08\xec\x05\xdb\xe1\xfdoh\x1f\xbc\x1c\x06\xb4\xe6\x1a`\x007\xc0#\xe0\x05\xd3 \x04\x16\x81\x8f\xcd\x94~\xd0\xc3z\x8b\xf6X\x05\xc8\x07\xe2]\xf4\xbf\xc8\xe0\xe5(\xa8\x05\xe7A\x07\xb8\x05\x9e\x82\xd7\xe03X\x05Y\xbb\xc8s*\xfdO^3\x8a\xe9\'biP)',
                    "IPVF": b'\x00\x00\x03\x06x\x9c\xed\x95_H\x93Q\x18\xc6\xbfm\xbaj#\x11\xdc\xf0\xa2u\x11\x8d\xb2\x9b\xba\xd9\xbc\xd1\x0c\xba2\x11\xd6\xc56\x89\xf0b\xb4\x8bM#R\xc41[9p\x8ej\x04e7\xc1\x98\x12D\x1b6dE\xc1\xba\n"CA\x90,\x92\xba\xd1\x04\xb3\x02\xe9\xa2Z+\x9co\xcf\xd1\xf3\xb1\xcf\xb9\xe5\x04\xf7\x87\xe8\x81\x1f\xdb{v\xde\xf7;\xcf\xf9\xdes&\x08\x8d\x82\xa6"&\xfc\xa3R\x10Q\xa9\xd7\xb0\x93\x92\xc1\xcf>\xd0\x08\xda\xc1\x150\x0c\x9e\x81y\xf0\x03l\xc7\xb3\xba\x0c\xf6G\x8b5\x18\x81\x15\xb8\xc0\x1d\xf0\x14\xbc\x03?\xc1G0\x0e\xee\x01\x1f8\x07N\x82\x03\xa0b\x9b^\xe7\xc0\x89\x02{\xaeB\xfdc\xe04\xb8\x08n\x81G\xe05\xf8\x06\x96\xc1\x14x\x00\xae\x03\'h\x06u`\xf7\x0e\xaf\x8dy\xfd\xc2\xf7+\xd7\x1c\x95\xd7\xeb\xfd[\x8d=|m\xa7@\x07\x08\x80(\xf7\xb0\xcc=\xcd\x80\x87\xdc+\xf3l\x02G\xc1\xde"\xf5W\x15`\x0f\x9a\x02\xcc\xebj2\x99\xa4\xe9\xe9i\x8aD"\x14\x08\x04\xc8\xedv\xa7\xba\xbb\xbb\x93.\x97k\x15~\'\x07\x07\x07\x87\x83\xc1\xe0Jgg\'\xf9|\xbe\xfb\xa9T\xea%\xf2\x96x\xcf}H$\x12\x14\x8f\xc7\x17Y~oo/Y\xadV2\x1a\x8d\xa4\xd1h\x88?\xab\x94\x07\xa7\x95?\xff.8\xec\xf1x\x98\'\xea\xe9\xe9\xa1\xae\xae.\xe6u\xcds8\x1c^\xdb\x03\xec\xc5\xa7\xd9\xd9\xd9\x85X,\x96\xf2\xfb\xfd\xd4\xdf\xdf\xff\xe6\x06422r\x1cc\xecN\x19\xe7\xf5\xceK\xbce\xa3T\xba\xc4\x9foW(\x14\xcf\xe1\xf5\x89\xc9dbq\xbbd\xce~>\xe7\xb7R\xa9\x14\xc7\x1e\xb31\xb5Z}\xcdl6\x87\x90\xb7\x00>c\xbf\x08\xf9/\x1a\x1a\x1a\xfcZ\xad6\xb3N9(*\xac{\xb9m\xb3\xd9\x98\xdf\xa8L&cq\x0b\xff\xbd\x02\x9c\xe5sf$ya>\xd6&\x19{U[[\xbbR__\x1fG_\xfc\xea\xeb\xeb#\xa7\xd39\xe6p8\x9aQ\xb7\x06\xfdP\x04;[j\t\xacTVV\xcecM\x07\x07\x06\x06X\x9c\xab\x07\xcfH\xf2\x82|\xcc\xcdc\xf1\\\xdc\x14\xeb\xca\xe5r\xd2\xe9t\xd4\xd4\xd4D\xd8K\xd6\xfbd\xb1XH\xaf\xd7+FGG\x8b`m\x93\xc4\xbb\xea\xbd\xb0~\xf7\x8a\xb1\x94\x04\x98\x146\xf7e\x07\xff=\xc4c\xf6\xee\xbf\x83\x1aI\xdd\r\xa0\xf7\xc9`0\x90\xddn_\xc4\xb3\xae\x82#\xd8\xdfB\xfa\xcb\x94\xf8N\xc2\x19q(gFZm|\xee\x18\xb0\xf0\xef\x97\xf3\xacS\xc7\xfd2\xdf\x13\xc0\x01\xaa\xb7\xf8\xaf\xdb\t\x89w\x95+#\xb6\xe5\x91\xdb"\xa4\xff\xc7\xde\n\xeb\xe7B\xb5\xcd:\xac\xaf\xd9\xd9\x8e\x80\xaf\xfc\x93\xc5\x85\xeaw\xf1\xaej\xcd\x88[rf\xa4uH\xd8\xd8\xaf\x17\xb2\xd4\xcd\xa7\x8e\xa8j\xfe\x9e\'\xf8{/D\xbf\x8bwSMF\xac\xca\x99\x91\x96RH{e\xe7_\x9e\xa5n>u\xb2\xa9T\xfd^j\x15\xbb\xdf\xcbI\xc5\xe8\xf7r\xd5\xff~\xf7z\x97\xc0\xae\xa1\xa1\xa1R\xaf\xa9X\xca\xe5\xf5\x0f3V_\xd0',
                    "IKSJ": b'\x00\x00\x03Qx\x9c\xed\x96_HSQ\x1c\xc7/\xe2\x1aD\xf4\x07\xdd\xd6|)\x82\xc0\xf9\xb2\x81\xf4\xe0\x12\x96\x0fE\x84\xd4\x1e\x1aQ\x04\x0e4\x1f\xf6\x92\x04\xa1$\xe1\xe6T$\x1f6\xa4\x02K\xe6|0A\xa4,\x08#\x88\xad\x87\xf6\xb0\x97\x82Jh\xe1\x1cN\x13\x93\xd5\xa2lb\x9b\xa7\xef\xaf\xfd.\xca\xd8\xc4\xe120\x7f\xf0\xe1\x9e\xdf=\xe7\xdc\xf3\xfb\xfe~\xe7\x9e{%\xa9Z*-\x1e\x93v\xec\xbf4\xa5\x10\xe2_\xc7\xb0UFZ\xe7A\xc9\xcc\xcc\xccn\xbb\xdd\xbe\x1f\xa8\xba\xba\xba\xcap=\x0c\x8e:\x9d\xce\n\\\r\xe0X{{\xbb\x11\xd7\x13\xe0\xa4\xc3\xe18\x83\xab\x19X\xd0\xbe\x84\xab\x15\\A\xdb\x86k\x13\xb8\x8e\xf6\r{\xda:\xc1-\xe0\x06w\xc0=\xe0\x05C`\x04\x8c\x81\xa7\xe09\xf0\x83W \x08\xde\x80\xf7 \x04"`\x16|\x06q\xb0\x08\x96A\n\xe4\xa3Y`|\x12\xb1\xd1\xfc\xaf\xfc<z\xee\x14\xafC\xeb\xbd\xe6\xf5)\x0e\x1f\xc7E\xf1=\xe2x)\xee\x01\xd6Az\\\xac\x8ft\xb6\xb1n\xd2\x7f\x95\xf3Ay\xa9\xe3<Q\xbe\xceq\xfe(\x8f&\xce+\xe5W\x0f*8\xef\x87:::\xca\xb8\x1e\xfb\xba\xbb\xbb\xa9>\x8a\xbe\xbe\xbe\x8d\xea\xdcKZA\xd8f\xb3=F\x8d\x8b\xd0^\x02\x0bk\xc6\\\xe31t\xffT\xc6\xdc\xdb \x0e\x96A\x14\xb4\xe5XG\xc3\xcf\x98\xddh`\x7f\xc9j9\x8e\x07j\xb5\xfa\x1b\xf4V\x99L&\xf2G\xb9\xbf\x9e\xfbI\xcf\xe9\x8c\xb9\xa3\xdc\x97Ig\x96u\xcc\xdc7Rp\x05\xf9Y+\xc7A\xba\xa8\xbew\xfb\xfb\xfb\xc9w\x82\x0b\xd2\xaa\x86\xb3Y\xe6&\xb9\xaf\x92\xfd\x1a)\x9d\x97\xb9,c\x1d<\xb6\xb5\xa0\xd1\xe7or\x8dL\xe02\xf4F\x83\xc1 \xf9\xf7\xa5U\xad\x96\x1cs\'\xb9\xff\xf8\x06\xd6y\xc8ck7\x1d\xf1\xe6\x8cjAu*\x06j\xe8\x15\xa9TJx\xbd^a0\x18(\xbe\x1fR\xfa\xdd\xcbfTOz\xcfi\xdc0(_g\x9d/<nO\xc1"\xcf\xdf\xe4\xb3*\xc4>iNj\xb5Z\xd1\xd2\xd2\x92\xc2\xb7)\x14\x8dFS\x16\x8b\xa5W\xa9T\xe6z\x06\xc5\x7fSJ\xeb\xa1\xbc\xd5e\x19#\x9fU\xd1\x82F\x9f\xbf\xc9g\xd50\xfb5\xd2\xaa\xfe#\x1a\x8d\xe6<\xca\xfdibbBLOO\xf7\x84\xc3\xe1\x83\xeb\xfc\x93hy\xeeB\x96>\xf9\x1c\x18*h\xf4\xf9\x9b|V5\xb3\xdf\xc4\xfe\xdao\n\xedQ\xa1\xd7\xeb\'\xc7\xc7\xc7W\xa0\xf7#x\x02\x96\\.\xd7\xaf\xc6\xc6\xc6\xba\xc1\xc1A\x15|9W\xb4\xffI\xf3O)]\xd7]\xe0%\xf7]\xdc\x1aY9M>\xab\xe43dD\xca~\x16\x8f\xf1\xfd*\xa3\xd1X\x0emf\xf0\xd6\xedv\x0b\x8f\xc7#\x02\x81\x80\x88\xc5b\x7f@\xfb\x9d\xcf\xe7\x9b\xc7\xff\x810\x9b\xcdB\xa7\xd3\t\x85BAs\xa7@\xd1V\t\xcbatVQ,%\xecG\xd9We\x8c\xab\xe4\xfb\xcf\xd6\xdc;\x00z\xc1\xbc\x94~o\xe7\xf0\xfd\xf6Z\xad\xd6\x86d2\xe9\x89D"1\xbf\xdf\xbf\x12\n\x85D"\x91X\xc49\xf0"\x1e\x8f\xf7 O\r\xa0\x1a\xa8\xb6\xe9\xff\xba\x02\xba\xe4=\xd1\x0c< \x00b\x0c\xb5\x07\xb8\x8f\xc6\xe8\x80b\x9b\xe6\xa2\x94k]\x0fz\xf8\\\xf8\x00\x12 \xc4\xfe\xce\x9e\xd8\xd9\x13\xb4\'\xbe\x83\xe2m\xaa9\x9b\xe5\xd2\xfa\x1b\x83\x12\x85\xe8',
                    "LWFF": b'\x00\x00\x03^x\x9c\xed\x96]H\x93Q\x1c\xc6_\xe6\\Pm\x11e\x03!P\xbb\x91E\x10\xb4\x0b\x85.\xb6\x8bp\x0c\xaf$\x85\xd9"\x83P\xd9@1\xc5\x06\x06N\x1d\xeaPJ\xc3\x0c\xf4FI\xa1\xe6\x84\xb6\xa2"f\r5\x1a\x997\xc2\xd0\x84f\x94\x11\xbaAn\x82E\xc5N\xcf\xd1\xf3\xb2i\xbes\x96\xd3>|\xe0\xc7\xfbq\xfe\xef{\xces>\xfe\xe7p\xdci\xee\xb0\xf8\x1e\xb7\xab\xffRI6\x9bm\xa7\xdb\xb0]\xa2^\x97\xccf\xf3,\xf0\x80\x01p\x1d\\\x06\x05 \xbb\xbe\xbe\xfe\xa8\xc5b\xd9\xd7\xd2\xd2\xb2\xd3m\xdd*Q\xcf\xd4\x13\xf5\x96_WWG\xbd^c\xde_\x80\x0f \x0c\x1e\xa3\xac\x14\xd7T\xb0\xd3m\xfe\x15\xc9\x00\x01\xef\x05\xca\x97X9\xd5\x81\xe6\xe6\xe6\xb3\xf09b4\x1aIuu5)..\xbe\x8a\xe7\x13\xe8\xa3\x93,n\x84]\x85\x88\xae3VL\xa2\x94\xcb\xea\xe8\x17(\x9fZ\xd3\x061xC\xdf\x89D"\x92\x96\x96F\xe7\xbd\x0f,VUU\x11\x8dFs+++k\xb9\x8c\x13\xf6\x92+P\xb6\x1d~kX\x1d\xa5\x02\xe5\xce5m\xb8\x02\xber\xab\xdb\x96\x02\xbe\xc9\xe5r_NN\xcelEE\x05\x1d\xfb\xe7\x06\x83\x81\xce\x05\xa9\xd5j\x15\xaa\xf3\xfcV\x99\xd8\x84\xec\xac\xeeS\x02\xe5\xfd\\\xc4\xd7!\x10\x02\xdd\xdcj\xbf\xb5\xec>\x9b\xff\x9fT*\xed(,,|\x08\xbfA\xf0\x08D\xafy\xbeNm\x02\xfcl\xa4\x8f\xdc\xca\x1a\x15R\x07\x17\xf1u\x83\xdd+\xb8\x88_\x11\x98\x03\xcf\xa2\xfe\xb7j~J$\x12\xa2P(H^^^\x00~\xc7\xe8\xdcW\xab\xd5\x04\xf3a\xbb\xe72\x9f7\x1e\xc4\x88\xb9\xc8b2\xc1w0\xc4\xde\xf3\xed\xbb\xc0E\xc66f\x1eJNN\x16\xc3\xab\xb6\xac\xac\x8c\xaesR^^\xbe\x0c\xbdOOO\xe7\xd7|"\xc5\xe7\x8d\xda\x181\xf9,\x86_\xc7\x1a\xf6\x9e\xf7\xf1\x8a\x8b\x8c\xadN\xa9T\x12\xf0\xb4\xb2\xb2\xd2D\x08\xe9\x06C`\x86\xac\xc8\x0f\xde\x05\x83A\xe2v\xbbgFGG\xef\xfa|\xbe\xa1\xc1\xc1\xc1\xb7\xad\xad\xad\xa1\x86\x86\x86\'mmm\x15===\x19\x13\x13\x13I\x88\xddj\xbf|\xde\xc8\x8d\x11\xa3\x89\xf26-\x93\xc9\x8e\xa1\x1dgh\xe3KJJ\x08r\x11\xb1\xdb\xed\xafC\xa1\xd0\x02^}\x86\xc8\xf8\xf8\xf8\xd8\xe4\xe4\xa4\x95\x86\xb0\xd8\x0c \x01)\xa0]\xab\xd5\x12\x95J\xd5\xd9\xde\xden\xc0\xb3\x19\xdc\x04\xf7\x03\x81\xc0\xf4\xf0\xf0\xf0"\xfc\x86\x9b\x9a\x9a\xc2}}}\x8b\x1e\x8fgzaa\xc1\x8d\xf2\x01\xd0\xc9\xe2\x8d\xa0\x00\xa8\xc0qp\x04\xc4\xd3?|\xdeX\x0f>\x97d\xeat:\xa2\xd7\xeb\x89\xd3\xe9\x0c\xb3\xb1rQ\xbf]]]\xc4d2y\xe1[\x89\xc7\x83 \x9e<\x14O\xcc~\xcc{z\xe6\x19hll\xfc\x84\xeb\x14\xf6\xfd;\xbd\xbd\xbd\x16\xaf\xd7\xcb\xf7\x8f\r\xd0~\xf0\x82y\xf0\x05\x886\xf0\xfcSn\xe1\xc18^\xf2\xfb\xfd\x0e|\x1f\xa4\xde\x1c\x0eG\xa8\xa8\xa8H\xeer\xb9\xf8o\xf9\xd8\xecu\xfe\xb77\x8e:c\xc5D\x8b\xaey\x15;\xdf\xfa\x18\xf4^\x8d~\x10G\x9d\xf16\xf2\xbaV2\xc4\xeb\xa95\xe6\x91^\xcf\x01Y\x02\xd6\xd1\xef\x88\x9e\xe5j\xe0\xf5%\xbc\xd2|\x7f\x1b\x08\xed\xf3B\xda\x03Os\x7f\xb0G!\xa5\xb2}\x9d\xee\xf3\xf3@\xb2\x893\xfd\x9e\xbf\xc4\xa3\x906\xe3uW\xff\x8e~\x00\x0e6qN',
                    "DNIC": b'\x00\x00\x03\x10x\x9c\xed\x95_HSQ\x1c\xc7/\x9b\x0e\x86c0\xcae\xe6\x83\x0c\xdcC\x85\x0cz\x08b\xb8\x1eF\xa6F \x94\xb3\x17\x1f\x12\x12J\xdc\x93\x13\x9d\xb1\xcd\x07\xa5\x82\xe9\x83\x05\x05>D\x0f\xc2\xdc@"$\x88$\x89\xc0\x07_\xa74\xc5\x1c\xb6\x82D\x92\x05e:\xfb\xf5=\xf8\xbbu\xbbl\x13\x9c\xb7D\xfb\xc1\x87s\xcf\xef\x9c\xf3;\xbf\xef\xf9w%\xc9)\x1d-\x1a\x97r\x98\x91\x88r\xb5\x1d4\x13Z\xdf\x83\xb2C\xa4y\x10Z\xc3\x87H\xaf\xd8\xdb\xd5C\xb8\xc7C\x07\\\xaf\x19\x90LEE\x05\xfd\x80-..\xaeLOO\x8f\xcd\xcf\xcf{\xa1\xffJ2\x99$\xbb\xddN\xc5\xc5\xc5\xd5\x8a\xb1&\x1e\xb7\xa2\x8a5\xa3\x9a\xc3\x01b\x06\x83!\x8dr\x03\xa4\xc0]P\xa4\xa1\xae\\vIR\xe8\x15\x98\xcdf\xaa\xaa\xaa\xa2\xfa\xfa\xfa\x8c\xd7\xeb\x1d]ZZ\x9aI\xa5R\xb4\xb0\xb0@\x85\xda\xdc\xdc\x1cE\xa3Q\n\x85B\xe4\xf1xFjkk\r\x7f\xf9<\xf9Y\xe75\x85\xef\x18\x18e\xff\x84\xa2\x0f\xe9\xf5z\xb1\x97:\xee\xd7\xc5\xfe\x80*V+\xd7m`\x9d}\xf7JJJ\xceMMMy2\x99Llrrr+\x16\x8bm$\x12\x89ob\x19@\x14\x84\x80\x07\x9c\x06Z\xadC\x94\xf3q\xa8\xfc\xf2\xd9\xfc\xaa\xe83\xc1\xe5e\xee\x13Q\xd5\xe5~.\xae\x0fs\xfdI\x9e\xf9\r\xac\xaf\x89\xf5\n\xdd\xb3@\xabu\xf8(m\xdf)\x9d\xca\xaf\xe3\\7\xb8\x8f\xf8>\xce\xf5\xa7\xdc\'\xc9\xfeRE\xac\x8c\xf4\xfb^\xbe\xe3\xf63\xbb\xc8K\x8bu\x90\xf7\xf0u\x96\xb63\xdc&\xe7\x9cb\x7f\x845\x9d\x90\xb2\xbfU\tE\x8c\x0c\xfb\xf6\xd2r\xadC\x1a\x14\xed\xa0Y~\xabF\xb2\xb4=\xe3\xb6\x18\x97\x11\xf6_\xe4\xfas.\xa3\xaaX\xa3\x8a\x18\xf2\xdd-\x95\xfe\xb4\xb3 \xad\x88\xb9\x17f\x88\xc7\xe3;\xf5\xc9\xf6VU\xe3\x9f$\xdf\xc35p\x87\xbfo\x03]0\x18\x14\xe7\\>\xdf\xd9\xde\xaa.E\xac\x97\xec\x13k\'\xee\x82\x18+\xd6+\xc5\xfe\xa1<\xb9\xe9#\x91\x88\x15\xf3\x9d\xea\xeb\xeb;\x8f\xb2\t\xdc\xc2\xbb\x8e"\xf8\x00\x8c\x81W`\x16\xac\x80u\x91\x1b\xc8\xa7W\xd6\xf5\x0b\x93\xc9D\x18\x93\x8f\xcf`\xcd\xe7\xf3Q[[\x1b\xb5\xb4\xb4\xbc\xc1?\xeb\x11|o\x1b\x1b\x1b\xc9\xe9t\x0e777_E^n\xf8\xae\xbb\xddn\xb2X,d4\x1a\xc5\xdbNx\xa3\xc9j\xb5Ree\xe5\x07\x87\xc3\xe1\xeb\xec\xec\xcc\x95\xff&\xf8\x04\xe2\xec\x8f\x80\xfb\xc1m\xbb\t\xc4\x1cb\x1dN\x82\xd2\xfe\xfe\xfe\x9d\xb4J\xaa}\x12l\xd5\xd5\xd5}ihhx\x88o\xbb\xaa\xcf\x11\xde_\xcb\xc0\xc0\xc0\x85\x9a\x9a\x1a*//\'\x9b\xcd\xd6\n\xbd7\xe0O\xbb\\.\x82\xbe\xc7==="\xb7\x17`\x06\xa4z{{7\xbb\xbb\xbb)\x10\x08\x10\xf4}\xef\xe8\xe8Xnoo\x1f\xf7\xfb\xfd\x85\xe6_\x88\x95!\xfe*(\xd3h\x1eq>\xb5\x88\xbb[\x1b\x84\xce\xb0\xc6k\xba_\xcc\x18\x0e\x87\x975\xdc\xdb\xfdhB\xf3\xbf\xce\xe1\xbf\x15n?\x01\xd6\x9cux'
                }
                self.client.currentCaptcha = random.choice(list(captchas))
                self.client.sendPacket(Identifiers.send.Captcha, captchas[self.client.currentCaptcha])
                return

            #elif CC == Identifiers.recv.Login.Player_MS:
                #print('g')
                #self.client.sendPacket(Identifiers.send.Player_MS)
                #return

            elif CC == Identifiers.recv.Login.Dummy:
                if self.client.awakeTimer != None: self.client.awakeTimer.cancel()
                self.client.awakeTimer = reactor.callLater(120, self.client.transport.close)
                return

            elif CC == Identifiers.recv.Login.Player_Info or CC == Identifiers.recv.Login.Player_Info2 or CC == Identifiers.recv.Login.Temps_Client:
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                self.client.lastGameMode = mode
                self.client.sendGameMode(mode)
                return

            elif CC == Identifiers.recv.Login.Undefined:
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if (not self.client.isDead and self.client.room.currentMap in range(200, 211)) or self.client.room.isFuncorp or self.client.hasLuaTransformations:
                    self.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(self.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readUnsignedByte(), packet.readUnsignedByte(), packet.readUTF()
                if self.server.isDebug:
                    if errorC == 1 and errorCC == 1:
                        print("[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, oldCC, error))
                        with open("./logs/Errors/Debug.log", "a") as f:
                            f.write("[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, oldCC, error))
                        f.close()
                    elif errorC == 60 and errorCC == 1:
                        if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                        print("[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, error))
                        with open("./logs/Errors/Debug.log", "a") as f:
                            f.write("[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, error))
                        f.close()
                    else:
                        print("[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, errorC, errorCC, error))
                        with open("./logs/Errors/Debug.log", "a") as f:
                            f.write("[%s] [%s] GameLog Error - C: %s CC: %s error: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, errorC, errorCC, error))
                        f.close()
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                self.client.shamanType = type
                self.client.sendShamanType(type, (self.client.shamanSaves >= 100 and self.client.hardModeSaves >= 150))
                return

            elif CC == Identifiers.recv.Informations.Letter:
                playerName = Utils.parsePlayerName(packet.readUTF())[:-5]
                type = packet.readByte()
                letter = packet.readUTFBytes(packet.getLength())
                idler = {0:29,1:30,2:2241,3:2330,4:2351}
                
                if self.server.checkExistingUser(playerName):
                    id = idler[type]
                    count = self.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        self.client.playerConsumables[id] -= 1
                        if count == 0:
                            del self.client.playerConsumables[id]
                            if self.client.equipedConsumables:
                                for id in self.client.equipedConsumables:
                                    if not id:
                                        self.client.equipedConsumables.remove(id)
                                None
                                if id in self.client.equipedConsumables:
                                    self.client.equipedConsumables.remove(id)

                    self.client.updateInventoryConsumable(id, count)
                    self.client.useInventoryConsumable(id)
                    
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
                else: 
                    self.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                
                return

            elif CC == Identifiers.recv.Informations.Letter:
                return

            elif CC == Identifiers.recv.Informations.Send_self:
                self.client.sendPacket(Identifiers.send.Send_self, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info:
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                self.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                self.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://195.154.124.74/outils/info.php").toByteArray())
                return

        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Lua_Script:
                #script = packet.readUTFBytes(((packet.readByte() << 24) & 0xFF) | packet.readShort()).decode()
                script = packet.readUTFBytes(int.from_bytes(packet.read(3),'big')).decode()
                if self.client.privLevel >= 9 or self.client.isLuaCrew:
                    if not self.client.isLuaAdmin:
                        if self.client.room.luaRuntime == None:
                            self.client.room.luaRuntime = Lua(self.client.room, self.server)
                        self.client.room.luaRuntime.owner = self.client
                        self.client.room.luaRuntime.RunCode(script)
                    else: self.client.runLuaScript(script)
                return

            elif CC == Identifiers.recv.Lua.Key_Board:
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()
                
                if key == 9 and self.client.privLevel >= 7:
                    if self.isOpenedHelpCommand == False:
                        self.client.sendLogMessage(self.client.sendModerationCommands())
                        self.isOpenedHelpCommand = True
                    else:
                        self.isOpenedHelpCommand = False
                
                if self.client.isFlyMod and key == 32:
                    self.room.bindKeyBoard(self.playerName, 32, False, self.room.isFly)
                
                if self.client.isFFA and key == 40:
                    if self.client.canSpawnCN == True:
                        if self.client.isMovingRight == True and self.client.isMovingLeft == False:
                            reactor.callLater(0.2, self.client.Utility.spawnObj, 17, posX - 10, posY +15, 90)
                        if self.client.isMovingRight == False and self.client.isMovingLeft == True:
                            reactor.callLater(0.2, self.client.Utility.spawnObj, 17, posX + 10, posY +25, 270)
                        reactor.callLater(2.5, self.client.Utility.removeObj)
                        self.client.canSpawnCN = False
                        reactor.callLater(1.3, self.client.enableSpawnCN)

                #elif self.client.room.mapCode == 2002 and self.client.room.isHuggingEvent:
                    #if self.client.posX >= 789 and self.client.posX <= 911 and self.client.posY >= 354 and self.client.posY <= 356:

                if self.client.isSpeed and key == 32:
                    self.client.room.movePlayer(self.client.playerName, 0, 0, True, 50 if self.client.isMovingRight else -50, 0, True)
                if self.client.room.isFlyMod and key == 32:
                    self.client.room.movePlayer(self.client.playerName, 0, 0, True, 0, -50, True)
                if self.client.isFly and key == 32:
                    self.client.room.movePlayer(self.client.playerName, 0, 0, True, 0, -50, True)

                if self.client.room.isDeathmatch and key == 3:
                    if self.client.room.canCannon:
                        if not self.client.canCN:
                            self.client.room.objectID += 1
                            idCannon = {15: "149aeaa271c.png", 16: "149af112d8f.png", 17: "149af12c2d6.png", 18: "149af130a30.png", 19: "149af0fdbf7.png", 20: "149af0ef041.png", 21: "149af13e210.png", 22: "149af129a4c.png", 23: "149aeaa06d1.png"}
                            #idCannon = "149aeaa271c.png" if self.client.deathStats[4] == 15 else "149af112d8f.png" if self.client.deathStats[4] == 16 else "149af12c2d6.png"
                            if self.client.isMovingRight:
                                x = int(self.client.posX+self.client.deathStats[0]) if self.client.deathStats[0] < 0 else int(self.client.posX+self.client.deathStats[0])
                                y = int(self.client.posY+self.client.deathStats[1]) if self.client.deathStats[1] < 0 else int(self.client.posY+self.client.deathStats[1])
                                self.client.sendPlaceObject(self.client.room.objectID, 17, x, y, 90, 0, 0, True, True)
                                if self.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not self.client.deathStats[3] == 1:
                                        self.client.room.sendAll([29, 19], ByteArray().writeInt(self.client.playerCode).writeUTF(idCannon[self.client.deathStats[4]]).writeByte(1).writeInt(self.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            else:
                                x = int(self.client.posX-self.client.deathStats[0]) if self.client.deathStats[0] < 0 else int(self.client.posX-self.client.deathStats[0])
                                y = int(self.client.posY+self.client.deathStats[1]) if self.client.deathStats[1] < 0 else int(self.client.posY+self.client.deathStats[1])
                                self.client.sendPlaceObject(self.client.room.objectID, 17, x, y, -90, 0, 0, True, True)
                                if self.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not self.client.deathStats[3] == 1:
                                        self.client.room.sendAll([29, 19], ByteArray().writeInt(self.client.playerCode).writeUTF(idCannon[self.client.deathStats[4]]).writeByte(1).writeInt(self.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            self.client.canCN = True       
                            self.canCCN = reactor.callLater(0.8, self.client.cnTrueOrFalse)        
                if self.client.room.isDeathmatch and key == 79:
                    self.client.sendDeathInventory()
                if self.client.room.isDeathmatch and key == 80:
                    self.client.sendDeathProfile()
                    
                if self.client.room.isFFARace and key == 3:
                    if self.client.canCannon:
                        itemID = random.randint(100, 999)
                        if self.client.isMovingRight:
                            reactor.callLater(0.2, lambda: self.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX + -5).writeShort(posY + 15).writeShort(90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        else:
                            reactor.callLater(0.2, lambda: self.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX - -5).writeShort(posY + 15).writeShort(-90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        reactor.callLater(2.5, lambda: self.client.sendPacket(Identifiers.send.Remove_Object, ByteArray().writeInt(itemID).writeBoolean(True).toByteArray()))
                        self.client.canCannon = False
                        reactor.callLater(1.3, setattr, self.client, "canCannon", True)
                        
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("Keyboard", (self.client.playerName, key, down, posX, posY))
                return
            
            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()
                if self.client.isTeleport:
                    self.client.room.movePlayer(self.client.playerName, posX, posY, False, 0, 0, False)
                    
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
                #self.client.modoPwet.textAreaCallback(textAreaID, event) # Modopwet Events
                ## Menself Menu System ##
                
                if event in ["lbileri","lbgeri","lbkapat"]:
                    self.client.lbSayfaDegis(event=="lbileri",event=="lbkapat")
                    return 

                if event == "closed":
                    self.client.sendPacket([29, 22], struct.pack("!l", 7999))
                    self.client.sendPacket([29, 22], struct.pack("!l", 8249))
                    
                    
                if event == "fechar":
                    self.client.sendPacket([29, 22], struct.pack("!l", 10050))
                    self.client.sendPacket([29, 22], struct.pack("!l", 10051))
                    self.client.sendPacket([29, 22], struct.pack("!l", 10052))
                    self.client.sendPacket([29, 22], struct.pack("!l", 10053))


                elif event == "fecharPop":
                    self.client.sendPacket([29, 22], struct.pack("!l", 10056))
                    self.client.sendPacket([29, 22], struct.pack("!l", 10057))
                    self.client.sendPacket([29, 22], struct.pack("!l", 10058))

                        

                
                ## End Duxo Menu System ##
                    
                if event.startswith("fechadin"):
                    for x in range(0, 100):                                 
                        self.client.sendPacket([29, 22], ByteArray().writeInt(x).toByteArray())
                        
                if textAreaID in [8983, 8984, 8985]:
                    if event.startswith("inventory"):
                        event = event.split("#")
                        if event[1] == "use":
                            self.client.deathStats[4] = int(event[2])
                        else:
                            self.client.deathStats[4] = 0
                        self.client.sendDeathInventory(self.client.page)

                if textAreaID == 123480 or textAreaID == 123479:
                    if event == "next":
                        if not self.client.page >= 3:
                            self.client.page += 1
                            self.client.sendDeathInventory(self.client.page)
                    else:
                        if not self.client.page <= 1:
                            self.client.page -= 1
                            self.client.sendDeathInventory(self.client.page)

                if textAreaID == 9012:
                    if event == "close":
                        ids = 131458, 123479, 130449, 131459, 123480, 6992, 8002, 23, 9012, 9013, 9893, 8983, 9014, 9894, 8984, 9015, 9895, 8985, 504, 505, 506, 507
                        for id in ids:
                            if id <= 507 and not id == 23:
                                self.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                self.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 9009:
                    if event == "close":
                        ids = 39, 40, 41, 7999, 20, 9009, 7239, 8249, 270
                        for id in ids:
                            if id <= 41 and not id == 20:
                                self.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                self.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 20:
                    if event.startswith("offset"):
                        event = event.split("#")
                        if event[1] == "offsetX":
                            if event[2] == "1":
                                if not self.client.deathStats[0] >= 25:
                                    self.client.deathStats[5] += 1
                                    self.client.deathStats[0] += 1
                            else:
                                if not self.client.deathStats[0] <= -25:
                                    self.client.deathStats[5] -= 1
                                    self.client.deathStats[0] -= 1
                        else:
                            if event[2] == "1":
                                if not self.client.deathStats[1] >= 25:
                                    self.client.deathStats[6] += 1
                                    self.client.deathStats[1] += 1
                            else:
                                if not self.client.deathStats[1] <= -25:
                                    self.client.deathStats[6] -= 1
                                    self.client.deathStats[1] -= 1
                    elif event == "show":
                        if self.client.deathStats[3] == 1:
                            self.client.deathStats[3] = 0
                        else:
                            self.client.deathStats[3] = 1
                    self.client.sendDeathProfile()

                    
                if event == "closeRanking":
                        i = 30000
                        while i <= 30010:
                            self.client.room.removeTextArea(i, self.client.playerName)
                            i += 1
                            
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("TextAreaCallback", (textAreaID, self.client.playerName, event))
                return

            elif CC == Identifiers.recv.Lua.Color_Picked:
                colorPickerId, color = packet.readInt(), packet.readInt()
                #try:
                    #if colorPickerId == 10000:
                        #if color != -1:
                            #self.client.nameColor = "%06X" %(0xFFFFFF & color)
                            #self.client.room.setNameColor(self.client.playerName, color)
                            #self.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengi başarıyla değiştirildi." if self.client.langue.lower() == "tr" else "You've changed color of your nickname successfully." + "</font>")
                    #elif colorPickerId == 10001:
                        #if color != -1:
                            #self.client.mouseColor = "%06X" %(0xFFFFFF & color)
                            #self.client.playerLook = "1;%s" %(self.client.playerLook.split(";")[1])
                            #self.client.sendMessage("<font color='"+color+"'>" + "Farenizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if self.client.langue.lower() == "tr" else "You've changed color of your mouse successfully.\nWait next round for your new mouse color." + "</font>")
                    #elif colorPickerId == 10002:
                        #if color != -1:
                            #self.client.nickColor = "%06X" %(0xFFFFFF & color)
                            #self.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if self.client.langue.lower() == "tr" else "You've changed color of your nickname successfully.\nWait next round for your new nickname color." + "</font>")
                #except: self.client.sendMessage("<ROSE>" + "Renginizi Başarıyla Değiştiniz." if self.client.langue.lower() == "tr" else "Incorrect color, select other one.")
                return
            
        elif C == Identifiers.recv.Cafe.C or C == Identifiers.recv.Moludrome.C:
            if CC == Identifiers.recv.Cafe.Reload_Cafe:
                if not self.client.isReloadCafe:
                    self.client.loadCafeMode()
                    self.client.isReloadCafe = True
                    reactor.callLater(3, setattr, self.client, "isReloadCafe", False)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                self.client.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                if self.client.privLevel >= 1:
                    message, title = packet.readUTF(), packet.readUTF()
                    self.client.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                if self.client.privLevel >= 1:
                    topicID, message = packet.readInt(), packet.readUTF()
                    self.client.createNewCafePost(0, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                self.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                if self.client.privLevel >= 1:
                    topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                    self.client.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if self.client.privLevel >= 7:
                    topicID, postID = packet.readInt(), packet.readInt()
                    self.client.deleteCafePost(topicID, postID)
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if self.client.privLevel >= 7:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    self.client.deleteAllCafePost(topicID, playerName)
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
                if id in self.client.playerConsumables and not self.client.isDead and not self.client.room.isRacing and not self.client.room.isBootcamp and not self.client.room.isDefilante and not self.client.room.isSpeedRace and not self.client.room.isMeepRace:
                    # if not id in [31, 34, 2240, 2247, 2262, 2332, 2340] or self.client.pet == 0:
                    count = self.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        self.client.playerConsumables[id] -= 1
                        if count == 0:
                            del self.client.playerConsumables[id]
                            if self.client.equipedConsumables:
                                for id in self.client.equipedConsumables:
                                    if not id:
                                        self.client.equipedConsumables.remove(id)
                                None
                                if id in self.client.equipedConsumables:
                                    self.client.equipedConsumables.remove(id)

                        if id in [1, 5, 6, 8, 11, 20, 24, 25, 26, 2250]:
                            if id == 11:
                                self.client.room.objectID += 2
                            ids={1:65, 5:6, 6:34, 8:89, 11:90, 20:33, 24:63, 25:80, 26:95, 2250:97}   
                            self.client.sendPlaceObject(self.client.room.objectID if id == 11 else 0, ids[id], self.client.posX + 28 if self.client.isMovingRight else self.client.posX - 28, self.client.posY, 0, 0 if id == 11 or id == 24 else 10 if self.client.isMovingRight else -10, -3, True, True)
                            
##                        if id == 1 or id == 5 or id == 6 or id == 8 or id == 11 or id == 20 or id == 24 or id == 25 or id == 26 or id == 2250:
##                                if id == 11:
##                                    self.client.room.objectID += 2
##                                self.client.sendPlaceObject(self.client.room.objectID if id == 11 else 0, 65 if id == 1 else 6 if id == 5 else 34 if id == 6 else 89 if id == 8 else 90 if id == 11 else 33 if id == 20 else 63 if id == 24 else 80 if id == 25 else 95 if id == 26 else 114 if id == 2250 else 0, self.client.posX + 28 if self.client.isMovingRight else self.client.posX - 28, self.client.posY, 0, 0 if id == 11 or id == 24 else 10 if self.client.isMovingRight else -10, -3, True, True)
                        if id == 10:
                            x = 0
                            for player in self.client.room.clients.values():
                                if x < 5 and player != self.client:
                                    if player.posX >= self.client.posX - 400 and player.posX <= self.client.posX + 400:
                                        if player.posY >= self.client.posY - 300 and player.posY <= self.client.posY + 300:
                                            player.sendPlayerEmote(3, "", False, False)
                                            x += 1

                        if id == 11:
                            self.client.room.newConsumableTimer(self.client.room.objectID)
                            self.client.isDead = True
                            if not self.client.room.noAutoScore: self.client.playerScore += 1
                            self.client.sendPlayerDied()
                            self.client.room.checkChangeMap()
                    
                        if id == 28:
                            self.client.Skills.sendBonfireSkill(self.client.posX, self.client.posY, 15)

                        if id in [31, 34, 2240, 2247, 2262, 2332, 2340,2437]:
                            self.client.pet = {31:2, 34:3, 2240:4, 2247:5, 2262:6, 2332:7, 2340:8,2437:9}[id]
                            self.client.petEnd = Utils.getTime() + (1200 if self.client.pet == 8 else 3600)
                            self.client.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(self.client.playerCode).writeUnsignedByte(self.client.pet).toByteArray())

                        if id == 33:
                            self.client.sendPlayerEmote(16, "", False, False)
                        
                        if id == 21:
                            self.client.sendPlayerEmote(12, "", False, False)        

                        if id == 35:
                            if len(self.client.shopBadges) > 0:
                                self.client.room.sendAll(Identifiers.send.Balloon_Badge, ByteArray().writeInt(self.client.playerCode).writeShort(random.choice(self.client.shopBadges.keys())).toByteArray())

                        if id == 800:
                            self.client.shopCheeses += 5
                            self.client.sendAnimZelda(2, 0)
                            self.client.sendGiveCurrency(0, 5)

                        if id == 801:
                            self.client.shopFraises += 5
                            self.client.sendAnimZelda(2, 2)

                        if id == 2234:
                            x = 0
                            self.client.sendPlayerEmote(20, "", False, False)
                            for player in self.client.room.clients.values():
                                if x < 5 and player != self.client:
                                    if player.posX >= self.client.posX - 400 and player.posX <= self.client.posX + 400:
                                        if player.posY >= self.client.posY - 300 and player.posY <= self.client.posY + 300:
                                            player.sendPlayerEmote(6, "", False, False)
                                            x += 1

                        if id == 2239:
                            self.client.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(self.client.playerCode).writeInt(self.client.shopCheeses).toByteArray())
                        
                        if id in [2252,2256,2349,2379]:
                            renkler = {2252:"56C93E",2256:"C93E4A",2349:"52BBFB",2379:"FF8400"}
                            renk = int(renkler[id],16)
                            self.client.drawingColor = renk
                            self.client.sendPacket(Identifiers.send.Crazzy_Packet, ByteArray().writeUnsignedByte(1).writeUnsignedShort(650).writeInt(renk).toByteArray())

                        if id in [9,12,13,17,18,19,22,27,407,2251,2258,2308,2439]: # kurkler
                            ids={9:"10",12:"33",13:"35",17:"37",18:"16",19:"42",22:"45",27:"51",407:"7",2251:"61",2258:"66",2308:"75",2439:"118"}[id]
                            look = self.client.playerLook
                            index = look.index(";")
                            self.client.fur = ids + look[index:]
                            
                        if id == 2246:
                            self.client.sendPlayerEmote(24, "", False, False)

                        if id == 2100:
                            idlist = ["1", "5", "6", "8", "11", "20", "24", "25", "26", "31", "34", "2240", "2247", "2262", "2332", "2340", "33", "35", "800", "801", "2234", "2239", "2255", "10", "28"]
                            ids = int(random.choice(idlist))
                            if not ids in self.client.playerConsumables:
                                self.client.playerConsumables[ids] = 1
                            else:
                               counts = self.client.playerConsumables[ids] + 1
                               self.client.playerConsumables[ids] = counts
                            self.client.sendAnimZeldaInventory(4, ids, 1)

                        if id == 2255:
                            self.client.sendAnimZelda2(7, case="$De6", id=random.randint(0, 6))
                            
                        if id == 2259:
                            self.client.room.sendAll(Identifiers.send.Crazzy_Packet, self.client.getCrazzyPacket(5, [self.client.playerCode, (self.client.playerTime / 86400),(self.client.playerTime / 3600) % 24]));
                                
                        self.client.updateInventoryConsumable(id, count)
                        self.client.useInventoryConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                try:
                    if equip:
                        self.client.equipedConsumables.append(id)
                    else:
                        self.client.equipedConsumables.remove(str(id))
                except: pass
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
                try:
                    self.client.tradeAddConsumable(id, isAdd)
                except: pass
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

        elif C == Identifiers.recv.Sly.C:
            if CC == Identifiers.recv.Sly.Invocation:
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

            elif CC == Identifiers.recv.Sly.Remove_Invocation:
                if self.client.isShaman:
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(self.client.playerCode).toByteArray())
                    if self.client.room.luaRuntime != None:
                        self.client.room.luaRuntime.emit("SummoningCancel", (self.client.playerName))
                return

            elif CC == Identifiers.recv.Sly.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in self.client.shamanBadges:
                    self.client.equipedShamanBadge = str(badge)
                    self.client.sendProfile(self.client.playerName)
                return
                
            elif CC == Identifiers.recv.Sly.Crazzy_Packet:
                type = packet.readByte()
                if type == 2:
                    posX = int(packet.readShort())
                    posY = int(packet.readShort())
                    lineX = int(packet.readShort())
                    lineY = int(packet.readShort())
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Crazzy_Packet, self.client.getCrazzyPacket(2,[self.client.playerCode, self.client.drawingColor, posX, posY, lineX, lineY]))
                       

            elif CC == Identifiers.recv.Sly.NPC_Functions:
                id = packet.readByte()
                if id == 4:
                    self.client.openNpcShop(packet.readUTF())
                else:
                    self.client.buyNPCItem(packet.readByte())
                return

            
            elif CC == Identifiers.recv.Sly.Full_Look:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()

                shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")
                look = self.server.newVisuList[visuID].split(";")
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
                p.writeUTF(self.server.newVisuList[visuID])
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

            elif CC == Identifiers.recv.Sly.Map_Info:
                self.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount / 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    self.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1
                
                self.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount / 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    self.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return

        elif C == Identifiers.recv.Others.C:
            if CC == Identifiers.recv.Others.Open_Missions:
                self.client.missions.sendMissions()

            elif CC == Identifiers.recv.Others.Change_Mission:
                missionID = packet.readShort()
                self.client.missions.changeMission(str(missionID))
            
            elif CC == Identifiers.recv.Others.Cafe:
                topicID, delete = packet.readInt(), packet.readBoolean()
                self.client.MessageType(topicID, delete)
            
            elif CC == Identifiers.recv.Others.Warn:
                self.client.warns()

        if self.server.isDebug:
            print("[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
            with open("./logs/Errors/Debug.log", "a") as f:
                f.write("[%s] Packet not implemented - C: %s - CC: %s - packet: %s\n" %(self.client.playerName, C, CC, repr(packet.toByteArray())))
            f.close()
                

    def parsePacketUTF(self, packet):
        values = packet.split(chr(1))
        C = ord(values[0][0])
        CC = ord(values[0][1])
        values = values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                self.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                self.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                reactor.callLater(10, self.client.sendConjurationDestroy, int(values[0]), int(values[1]))
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
                if self.client.cheeseCount < 40 and self.client.privLevel < 6 and not isTribeHouse:
                    self.client.sendMessage("<ROSE>You need 40 cheese to transfer the map.", False)
                elif self.client.shopCheeses < (5 if isTribeHouse else 40) and self.client.privLevel < 6:
                    self.client.sendPacket(Identifiers.old.send.Editor_Message, ["", ""])
                elif self.client.room.EMapValidated or isTribeHouse:
                    if self.client.privLevel < 6:
                        self.client.shopCheeses -= 5 if isTribeHouse else 40

                    code = 0
                    if self.client.room.EMapLoaded != 0:
                        code = self.client.room.EMapLoaded
                        self.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [self.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        self.server.lastMapEditeurCode += 1
                        self.server.configs("game.lastmapcodeid", str(self.server.lastMapEditeurCode))
                        self.server.updateConfig()
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
                        self.client.room.sendAllOthers(self.client, Identifiers.old.send.Drawing, values)
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
            with open("./logs/Errors/Debug.log", "a") as f:
                f.write("[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s\n" %(self.client.playerName, C, CC, repr(values)))
            f.close()

    def descriptPacket(self, packetID, packet):
        data = ByteArray()
        while packet.bytesAvailable():
            packetID = (packetID + 1) % len(self.server.packetKeys)
            data.writeByte(packet.readByte() ^ self.server.packetKeys[packetID])
        return data

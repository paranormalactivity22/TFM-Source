from Identifiers import Identifiers
from ByteArray import ByteArray
from Utils import *

class Cafe:
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.chec = 0

    async def loadCafeMode(self):
        # self.client.cheeseCount < 1000 and self.client.playerTime < 108000
        if self.client.isGuest or (True):
            self.client.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
            # not self.client.isGuest and not (self.client.cheeseCount < 1000 and self.client.playerTime < 108000)
        self.client.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(True).toByteArray())

        packet = ByteArray().writeBoolean(True).writeBoolean(not self.client.privLevel < 7)
        await self.client.CursorCafe.execute("select * from cafetopics order by Date desc limit 0, 20")
        rss = await self.client.CursorCafe.fetchall()
        for rs in rss:
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(self.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        self.client.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())
        await self.sendWarnings()

    async def openCafeTopic(self, topicID):
        packet = ByteArray().writeBoolean(True).writeInt(topicID).writeBoolean(0).writeBoolean(True)
        await self.client.CursorCafe.execute("select * from cafeposts where TopicID = ? order by PostID asc", [topicID])
        rss = await self.client.CursorCafe.fetchall()
        cafe = False
        for rs in rss:
            cafe = True
            if self.client.privLevel >= 7 and rs["Status"] in [0, 2]:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
                self.chec = rs["PostID"]
            elif rs["Status"] < 2:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF("").writeByte(rs["Status"])
        self.server.lastCafeTopicID = topicID
        if not cafe:
            await self.client.CursorCafe.execute("delete from cafetopics where TopicID = ?", [topicID])
            return await self.loadCafeMode()
        self.client.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())
        
    async def createNewCafePost(self, topicID, message):
        commentsCount = 0
        if topicID == 0:
            topicID = self.server.lastCafeTopicID
        if not self.server.checkMessage(message):
            await self.client.CursorCafe.execute("insert into cafeposts values (null, ?, ?, ?, ?, 0, ?, '', 0)", [topicID, self.client.playerName, message, Utils.getTime(), self.client.playerCode])
            await self.client.CursorCafe.execute("update cafetopics set LastPostName = ?, Posts = Posts + 1, Date = ? where TopicID = ?", [self.client.playerName, Utils.getTime(), topicID])
            await self.client.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ?", [topicID])
            rs = await self.client.CursorCafe.fetchone()
            commentsCount = rs["count"]
            await self.openCafeTopic(topicID)
            for player in self.server.players.copy().values():
                if player.isCafe:
                    player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(self.client.playerName).writeInt(commentsCount).toByteArray())
        
    async def createNewCafeTopic(self, title, message):
        if not self.server.checkMessage(title):
            await self.client.CursorCafe.execute("insert into cafetopics values (null, ?, ?, '', 0, ?, ?)", [title, self.client.playerName, Utils.getTime(), self.client.langue])
            await self.createNewCafePost(self.client.CursorCafe.lastrowid, message)
        await self.loadCafeMode()
        
    async def voteCafePost(self, topicID, postID, mode):
        points = 0
        votes = ""
        if self.client.isGuest or self.client.cheeseCount < 1000 and self.client.playerTime < 108000: return

        await self.client.CursorCafe.execute("select Points, Votes from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = await self.client.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]
            
        if not str(self.client.playerID) in votes:
            votes += str(self.client.playerID) if votes == "" else "," + str(self.client.playerID)
            if mode:
                points += 1
            else:
                points -= 1

            await self.client.CursorCafe.execute("update cafeposts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
            self.client.updateDatabase()
            await self.openCafeTopic(topicID)
        
    async def getTopicID(self, postID):
        await self.client.CursorCafe.execute("select TopicID from cafeposts where postID = ?", [postID])
        rs = await self.client.CursorCafe.fetchone()
        return rs[0] if rs else -1
        
    async def getPlayerPosts(self, playerName, topicID):
        await self.client.CursorCafe.execute("select PostID from cafeposts where Name = ? and TopicID = ?", [playerName, topicID])
        r = await self.client.CursorCafe.fetchall()
        return len(r)
        
    async def deleteCafePost(self, postID):
        topicID = await self.getTopicID(postID)
        if topicID != -1:
            await self.client.CursorCafe.execute("delete from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
            await self.client.CursorCafe.execute("update cafetopics set Posts = Posts - 1 where TopicID = ?", [topicID])
            self.client.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
            await self.openCafeTopic(topicID)

    async def deleteAllCafePost(self, topicID, playerName):
        n = await self.getPlayerPosts(playerName, topicID)
        await self.client.CursorCafe.execute("delete from cafeposts where TopicID = ? and Name = ?", [topicID, playerName])
        await self.client.CursorCafe.execute("update cafetopics set Posts = Posts - ? where TopicID = ?", [n, topicID])
        await self.loadCafeMode()
        await self.openCafeTopic(topicID)
        
    async def ReportCafeTopic(self, topicID, postID):
        return
        
    async def ViewCafeMessages(self, playerName):
        return
        
    async def checkTopic(self, topicID):
        if self.client.privLevel < 7:
            return 0
        else:
            await self.client.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ? and Status = 0", [topicID])
            return int((await self.client.CursorCafe.fetchone())["count"])
    
    async def CheckMessageType(self, topicID, status):
        if status:
            await self.client.CursorCafe.execute("update cafeposts set Status = 2, ModeratedBY = ? where PostID = ?", [self.client.playerName, self.chec])
            await self.openCafeTopic(topicID)
        else:
            await self.client.CursorCafe.execute("update cafeposts set Status = 1, ModeratedBY = ? where PostID = ?", [self.client.playerName, self.chec])
            await self.openCafeTopic(topicID)
        self.chec = 0
        
    async def sendWarnings(self):
        await self.client.CursorCafe.execute("select * from cafeposts where status = 2 and name = ? order by postid asc", [self.client.playerName])
        self.client.sendPacket(Identifiers.send.Send_Cafe_Warnings, ByteArray().writeShort(len(await self.client.CursorCafe.fetchall())).toByteArray())
        
    async def deletePlayerMessages(self, playerName):
        await self.client.CursorCafe.execute("delete from cafeposts where Name = ?", [playerName])
        await self.client.CursorCafe.execute("delete from cafetopics where Author = ?", [playerName])
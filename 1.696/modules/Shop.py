#coding: utf-8
import binascii

from ByteArray import ByteArray
from Identifiers import Identifiers

class Shop:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor

    def getShopLength(self):
        return 0 if self.client.shopItems == "" else len(self.client.shopItems.split(","))

    def checkUnlockShopTitle(self):
        if self.getShopLength() in self.server.shopTitleList:
            title = self.server.shopTitleList[self.getShopLength()]
            self.client.checkAndRebuildTitleList("shop")
            self.client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
            self.client.sendCompleteTitleList()
            self.client.sendTitleList()

    def checkAndRebuildBadges(self):
        rebuild = False
        for badge in self.server.shopBadges.items():
            if not badge[0] in self.client.shopBadges and self.checkInShop(badge[0]):
                self.client.shopBadges[str(badge[1])] = 0
                rebuild = True

        if rebuild:
            badges = self.client.shopBadges
            self.client.shopBadges = {}
            for badge, count in badges.items():
                if not badge in self.client.shopBadges:
                    self.client.shopBadges[badge] = count

##    def checkAndRebuildBadges(self):
##        rebuild = False
##        for badge in self.server.shopBadges.items():
##            if not badge[1] in self.client.shopBadges and self.checkInShop(badge[0]):
##                self.client.shopBadges.append(str(badge[1]))
##                rebuild = True
##
##        if rebuild:
##            tempBadges = []
##            tempBadges.extend(self.client.shopBadges)
##            self.client.shopBadges = []
##            self.client.shopBadgesCounts = {}
##            for badge in tempBadges:
##                if not badge in self.client.shopBadges:
##                    self.client.shopBadges.append(badge)
##
    def checkUnlockShopBadge(self, itemID):
        if not self.client.isGuest:
            if itemID in self.server.shopBadges:
                unlockedBadge = self.server.shopBadges[itemID]
                self.sendUnlockedBadge(unlockedBadge)
                self.checkAndRebuildBadges()

    def checkInShop(self, checkItem):
        if not self.client.shopItems == "":
            for shopItem in self.client.shopItems.split(","):
                if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                    return True
        else:
            return False

    def checkInShamanShop(self, checkItem):
        if not self.client.shamanItems == "":
            for shamanItems in self.client.shamanItems.split(","):
                if checkItem == int(shamanItems.split("_")[0] if "_" in shamanItems else shamanItems):
                    return True
        else:
            return False

    def checkInPlayerShop(self, type, playerName, checkItem):
        self.Cursor.execute("select %s from Users where Username = %s" %(type), [playerName])
        for rs in self.Cursor.fetchall():
            items = rs[type]
            if not items == "":
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
            else:
                return False

    def getItemCustomization(self, checkItem, isShamanShop):
        items = self.client.shamanItems if isShamanShop else self.client.shopItems
        if not items == "":
            for shopItem in items.split(","):
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        else:
            return ""

    def getShamanItemCustom(self, code):
        item = self.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                packet = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
                return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(self, fullItem):
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        return self.getItemPromotion(itemCat, item, self.server.shopListCheck[str(itemCat) + "|" + str(item)][1])
                
    def getShamanShopItemPrice(self, fullItem):
        return self.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(self, itemCat, item, price):
        for promotion in self.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] / 100.0 * price)
        return price

    def sendShopList(self):
        self.sendShopList(True)

    def sendShopList(self, sendItems=True):
        shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")

        packet = ByteArray().writeInt(self.client.shopCheeses).writeInt(self.client.shopFraises).writeUTF(self.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = self.server.shopList if sendItems else []
        packet.writeInt(len(shop))

        for item in shop:
            value = item.split(",")
            packet.writeShort(int(value[0])).writeShort(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeByte(int(value[4])).writeInt(int(value[5])).writeInt(int(value[6])).writeByte(0)
                
        visuais = self.server.newVisuList
        packet.writeByte(len(visuais))
        i = len(visuais)
        for visual in visuais.items():
            packet.writeShort(visual[0])
            a = visual[1]
            packet.writeUTF("".join(a))
            packet.writeByte(visual[2])
            i -= 1

        packet.writeShort(len(self.client.clothes))

        for clothe in self.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])    

        shamanItems = [] if self.client.shamanItems == "" else self.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))

                packet.writeBoolean(item in self.client.shamanLook.split(",")).writeByte(len(realCustom)+1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(0)

        shamanShop = self.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))

        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(int(value[0])).writeByte(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeInt(int(value[4])).writeShort(int(value[5]))

        self.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray())
             
    def sendShamanItems(self):
        shamanItems = [] if self.client.shamanItems == "" else self.client.shamanItems.split(",")

        packet = ByteArray().writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(item.split("_")[0])).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(0)
        self.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray())

    def sendLookChange(self):
        try:
            p = ByteArray()
            look = self.client.playerLook.split(";")
            p.writeShort(int(look[0]))

            for item in look[1].split(","):
                if "_" in item:
                    itemSplited = item.split("_")
                    realItem = itemSplited[0]
                    custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                    realCustom = [] if custom == "" else custom.split("+")
                    p.writeInt(int(realItem)).writeByte(len(realCustom))
                    x = 0
                    while x < len(realCustom):
                        p.writeInt(int(realCustom[x], 16))
                        x += 1
                else:
                    p.writeInt(int(item)).writeByte(0)

            p.writeInt(int(self.client.mouseColor, 16))
            self.client.sendPacket(Identifiers.send.Look_Change, p.toByteArray())
        except: pass

    def sendShamanLook(self):
        items = ByteArray()

        count = 0        
        for item in self.client.shamanLook.split(","):
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1
        self.client.sendPacket(Identifiers.send.Shaman_Look, ByteArray().writeShort(count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(self, fullItem):
        self.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeInt(fullItem).writeByte(1).toByteArray())

    def sendUnlockedBadge(self, badge):
        self.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(self.client.playerCode).writeShort(badge).toByteArray())

    def sendselfResult(self, type, playerName):
        self.client.sendPacket(Identifiers.send.self_Result, ByteArray().writeByte(type).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def equipClothe(self, packet):
        clotheID = packet.readByte()
        for clothe in self.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                self.client.playerLook = values[1]
                self.client.mouseColor = values[2]
                self.client.shamanColor = values[3]
                break
                
        self.sendLookChange()
        self.sendShopList(False)

    def saveClothe(self, packet):
        clotheID = packet.readByte()
        for clothe in self.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = self.client.playerLook
                values[2] = self.client.mouseColor
                values[3] = self.client.shamanColor
                self.client.clothes[self.client.clothes.index(clothe)] = "/".join(values)
                break

        self.sendShopList(False)

    def sendShopInfo(self):            
        self.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(self.client.shopCheeses).writeInt(self.client.shopFraises).toByteArray())

    def equipItem(self, packet):
        if self.client.isBlockAttack:
            fullItem = packet.readInt()
            itemStr = str(fullItem)
            itemCat = int((0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100)
            item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
            itemStr = str(item)

            equip = str(item) + self.getItemCustomization(fullItem, False)

            lookList = self.client.playerLook.split(";")
            lookItems = lookList[1].split(",")
            lookCheckList = lookItems[:]
            idx = 0
            while idx < len(lookCheckList):
                lookCheckList[idx] = lookCheckList[idx].split("_")[0] if "_" in lookCheckList[idx] else lookCheckList[idx]
                idx += 1

            if itemCat <= 10:
                if lookCheckList[itemCat] == itemStr:
                    lookItems[itemCat] = "0"
                else:
                    lookItems[itemCat] = str(equip)

            elif itemCat == 21:
                lookList[0] = "1"
                color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
                self.client.mouseColor = "78583a" if self.client.mouseColor == color else color
            else:
                if lookList[0] == itemStr:
                    lookList[0] = "1"
                else:
                    lookList[0] = itemStr

            self.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
            self.sendLookChange()
            self.client.isBlockAttack = False
            self.client.blockAttack()
		
    def buyItem(self, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()
        itemCat = int(((fullItem - 10000) / 10000) if fullItem > 9999 else fullItem / 100)
        item = int(fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem)
        self.client.shopItems += str(fullItem) if self.client.shopItems == "" else "," + str(fullItem)
        price = self.getItemPromotion(itemCat, item, self.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        if withFraises:
            self.client.shopFraises -= price
        else:
            self.client.shopCheeses -= price

        self.sendItemBuy(fullItem)
        self.sendShopList(False)
        self.client.sendAnimZelda(0, fullItem)
        self.checkUnlockShopTitle()
        self.checkUnlockShopBadge(fullItem)
        self.client.missions.upMission('6')

    def customItemBuy(self, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()

        items = self.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        self.client.shopItems = ",".join(items)
        if withFraises:
            self.client.shopFraises -= 20
        else:
            self.client.shopCheeses -= 2000

        if len(self.client.custom) == 1:
            if not fullItem in self.client.custom:
                self.client.custom.append(fullItem)
        else:
            if not str(fullItem) in self.client.custom:
                self.client.custom.append(str(fullItem))
                
        self.sendShopList(False)

    def customItem(self, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = self.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                self.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + self.getItemCustomization(fullItem, False)
                lookList = self.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(item):
                        lookItems[itemCat] = equip
                                
                elif lookItems[itemCat] == str(item):
                    lookItems[itemCat] = equip
                self.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                self.sendShopList(False)
                self.sendLookChange()
                break

    def buyShamanItem(self, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        price = self.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        self.client.shamanItems += str(fullItem) if self.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            self.client.shopFraises -= price
        else:
            self.client.shopCheeses -= price

        self.sendShopList(False)
        self.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(self, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + self.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = self.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        self.client.shamanLook = ",".join(lookItems)
        self.sendShamanLook()

    def customShamanItemBuy(self, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()

        items = self.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        self.client.shamanItems = ",".join(items)
        if withFraises:
            self.client.shopFraises -= 150
        else:
            self.client.shopCheeses -= 4000
                
        self.sendShopList(False)

    def customShamanItem(self, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = self.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                self.client.shamanItems = ",".join(items)

                item = str(fullItem) + self.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = self.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item
                                
                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                self.client.shamanLook = ",".join(lookItems)
                self.sendShopList()
                self.sendShamanLook()
                break

    def buyClothe(self, packet):
        clotheID, withFraises = packet.readByte(), packet.readBoolean()
        self.client.clothes.append("%02d/%s/%s/%s" %(clotheID, "1;0,0,0,0,0,0,0,0,0,0,0", "78583a", "fade55" if self.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            self.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            self.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        self.sendShopList(False)

    def sendself(self, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(), packet.readBoolean(), packet.readShort(), packet.readUTF()
        if not self.server.checkExistingUser(playerName):
            self.sendselfResult(1, playerName)
        else:
            player = self.server.players.get(playerName)
            if player != None:
                if (player.Shop.checkInShamanShop(fullItem) if isShamanItem else player.Shop.checkInShop(fullItem)):
                    self.sendselfResult(2, playerName)
                else:
                    self.server.lastselfID += 1
                    player.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(self.server.lastselfID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(isShamanItem).writeShort(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    self.sendselfResult(0, playerName)
                    self.server.shopselfs[self.server.lastselfID] = [self.client.playerName, isShamanItem, fullItem]
                    self.client.shopFraises -= self.getShamanShopItemPrice(fullItem) if isShamanItem else self.getShopItemPrice(fullItem)
                    self.sendShopList()
            else:
                selfs = ""
                if (self.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    self.sendselfResult(2, playerName)
                else:
                    self.Cursor.execute("select selfs from Users where Username = %s", [playerName])
                    rs = self.Cursor.fetchone()
                    selfs = rs[0]

                selfs += ("" if selfs == "" else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, isShamanItem, fullItem, message])))
                self.Cursor.execute("update Users set selfs = %s where Username = %s", [selfs, playerName])
                self.sendselfResult(0, playerName)

    def selfResult(self, packet):
        selfID, isOpen, message, isMessage = packet.readInt(), packet.readBoolean(), packet.readUTF(), packet.readBoolean()
        if isOpen:
            values = self.server.shopselfs[int(selfID)]
            player = self.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("$DonItemRecu", self.client.playerName)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                self.client.shamanItems += str(fullItem) if self.client.shamanItems == "" else ",%s" %(fullItem)
                self.sendShopList(False)
                self.client.sendAnimZelda(1, fullItem)
            else:
                self.client.shopItems += str(fullItem) if self.client.shopItems == "" else ",%s" %(fullItem)
                self.client.sendAnimZelda(0, fullItem)
                self.checkUnlockShopTitle()
                self.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = self.server.shopselfs[int(selfID)]
            player = self.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(selfID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                messages = ""
                self.Cursor.execute("select Messages from Users where Username = %s", [str(values[0])])
                rs = self.Cursor.fetchone()
                messages = rs[0]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, values[1], values[2], message])))
                self.Cursor.execute("update Users set Messages = %s where Username = %s", [messages, str(values[0])])

    def checkselfsAndMessages(self, lastReceivedselfs, lastReceivedMessages):
        needUpdate = False
        selfs = lastReceivedselfs.split("/")
        for self in selfs:
            if not self == "":
                values = binascii.unhexlify(self).split("|", 4)
                self.server.lastselfID += 1
                self.client.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(self.server.lastselfID).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBoolean(False).toByteArray())
                self.server.shopselfs[self.server.lastselfID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                self.client.sendPacket(Identifiers.send.Shop_self_Message, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBoolean(True).toByteArray())
                needUpdate = True

        if needUpdate:
            self.Cursor.execute("update Users set selfs = '', Messages = '' where Username = %s", [self.client.playerName])

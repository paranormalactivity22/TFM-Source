#coding: utf-8
import binascii, time

from ByteArray import ByteArray
from Identifiers import Identifiers
from functools import reduce

class Shop:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor
        self.presents = ""
        self.messages = ""

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
                self.client.shopBadges.append(str(badge[1]))
                rebuild = True

        if rebuild:
            badges = map(int, self.client.shopBadges)
            self.client.shopBadges = []
            for badge in badges:
                if not badge in self.client.shopBadges:
                    self.client.shopBadges.append(badge)

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
        for rs in self.Cursor['users'].find({'Username':playerName}):
            items = list(rs[type].split(','))
            if not len(items) == 1:
                for shopItem in items:
                    if shopItem != type and checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
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
        itemCat = (0 if fullItem // 10000 == 1 else fullItem // 10000) if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        item_idx = str(itemCat) + "|" + str(item)
        if item_idx in self.server.shopListCheck:
            return self.getItemPromotion(itemCat, item, self.server.shopListCheck[item_idx][1])
        else:
            if self.server.isDebug:
                print(f"[INVALID] The item id {itemCat} in category {item} does not exist in the shop.")
            return 0
                
    def getShamanShopItemPrice(self, fullItem):
        return self.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(self, itemCat, item, price):
        for promotion in self.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return price - int(promotion[2] / 100.0 * price)
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
            packet.writeShort(item["category"]).writeShort(item["id"]).writeByte(item["customs"]).writeBoolean(item["new"]).writeBoolean("purchasable" in item).writeInt(item["cheese"]).writeInt(item["fraise"]).writeBoolean(item["collector"] if 'collector' in item else False)
            if (item["collector"] if 'collector' in item else False):
                packet.writeInt(22)

        looks = {}
        if sendItems:
            for id in self.server.shopOutfitsCheck:
                if self.server.shopOutfitsCheck[id][4] <= int(time.time()):
                    looks[id] = self.server.shopOutfitsCheck[id]
        packet.writeByte(len(looks))
        for id in looks:
            packet.writeShort(id)
            packet.writeUTF(looks[id][0])
            packet.writeByte(looks[id][1])
            
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
            packet.writeInt(item["id"]).writeByte(item["customs"]).writeBoolean(item.get("new")).writeByte(item.get("flag")).writeInt(item["cheese"]).writeShort(item["fraise"])
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
        look = self.client.playerLook.split(";")
        p = ByteArray().writeShort(int(look[0]))

        for item in look[1].split(","):
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                p.writeInt(int(item.split("_")[0])).writeByte(len(realCustom))

                x = 0
                while x < len(realCustom):
                    p.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                p.writeInt(int(item)).writeByte(0)
        p.writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0).writeByte(0)

        try:
            p.writeInt(int(self.client.mouseColor, 16))
        except:
            p.writeInt(int("78583A", 16))
        self.client.sendPacket(Identifiers.send.Look_Change, p.toByteArray())

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
        self.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeInt(fullItem).writeByte(0).toByteArray())

    def sendUnlockedBadge(self, badge):
        self.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(self.client.playerCode).writeShort(badge).toByteArray())

    def sendShopGiftPacket(self, type, playerName):
        self.client.sendPacket(Identifiers.send.Gift_result, ByteArray().writeByte(type).writeUTF(playerName).writeByte(0).writeInt(0).toByteArray())

    def equipClothe(self, clotheID):
        for clothe in self.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                self.client.playerLook = values[1]
                self.client.mouseColor = values[2]
                self.client.shamanColor = values[3]
                break
        self.sendLookChange()
        self.sendShopList(False)

    def saveClothe(self, clotheID):
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

    def equipItem(self, fullItem):
        itemCat = (fullItem - 10000) // 10000 if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        lookList = self.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        i = 0
        while i < len(lookCheckList):
            lookCheckList[i] = lookCheckList[i].split("_")[0] if "_" in lookCheckList[i] else lookCheckList[i]
            i += 1

        if itemCat <= 10:
            lookItems[itemCat] = "0" if lookCheckList[itemCat] == str(item) else str(item) + self.getItemCustomization(fullItem, False)
        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            self.client.mouseColor = "78583a" if self.client.mouseColor == color else color
        else:
            lookList[0] = "1" if lookList[0] == str(item) else str(item)
            self.client.mouseColor = "78583a"

        self.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
        self.sendLookChange()
		
    def buyItem(self, fullItem, withFraises):
        itemCat = (fullItem - 10000) // 10000 if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
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

    def customItemBuy(self, fullItem, withFraises):
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

    def customItem(self, fullItem, customs):
        items = self.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                self.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem // 10000 == 1 else fullItem // 10000) if fullItem > 9999 else fullItem // 100
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

    def buyShamanItem(self, fullItem, withFraises):
        price = self.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        self.client.shamanItems += str(fullItem) if self.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            self.client.shopFraises -= price
        else:
            self.client.shopCheeses -= price

        self.sendShopList(False)
        self.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(self, fullItem):
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

    def customShamanItemBuy(self, fullItem, withFraises):
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

    def customShamanItem(self, fullItem, customs):
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

    def buyClothe(self, clotheID, withFraises):
        self.client.clothes.append("%02d/1;0,0,0,0,0,0,0,0,0/78583a/%s" %(clotheID, "fade55" if self.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            self.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            self.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        self.sendShopList(False)

    def sendShopGift(self, playerName, isShamanItem, fullItem, message):
        if not self.server.checkExistingUser(playerName) or playerName == self.client.playerName:
            self.sendShopGiftPacket(1, playerName)
        else:
            player = self.server.players.get(playerName)
            if player != None:
                if (player.Shop.checkInShamanShop(fullItem) if isShamanItem else player.Shop.checkInShop(fullItem)):
                    self.sendShopGiftPacket(2, playerName)
                else:
                    self.server.lastShopGiftID += 1
                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(self.server.lastShopGiftID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(isShamanItem).writeInt(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    self.sendShopGiftPacket(0, playerName)
                    self.server.shopGifts[self.server.lastShopGiftID] = [self.client.playerName, isShamanItem, fullItem]
                    self.client.shopFraises -= self.getShamanShopItemPrice(fullItem) if isShamanItem else self.getShopItemPrice(fullItem)
                    self.sendShopList()
            else:
                if (self.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    self.sendShopGiftPacket(2, playerName)
                else:
                    rs = self.Cursor['users'].find_one({'Username':playerName})
                    self.presents = rs['Gifts']
                    self.sendShopGiftPacket(0, playerName)
                self.presents += ("" if len(self.presents) == 0 else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, isShamanItem, fullItem, message])).encode()).decode()
                self.Cursor['users'].update_one({'Username':playerName},{'$set':{'Gifts':self.presents}})
                self.presents = ""
        
    def giftResult(self, giftID, isOpen, message, isMessage):
        if isOpen:
            values = self.server.shopGifts[int(giftID)]
            player = self.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("", "$DonItemRecu", self.client.playerName)

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

        elif message:
            values = self.server.shopGifts[int(giftID)]
            player = self.server.players.get(values[0])
            if player != None:
                player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(giftID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(bool(values[1])).writeInt(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                self.messages = ""
                rs = self.Cursor['users'].find_one({'Username':values[0]})
                self.messages = rs['Messages']
                self.messages += ("" if self.messages == "" else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, values[1], values[2], message])).encode()).decode()
                self.Cursor['users'].update_one({'Username':values[0]},{'$set':{'Messages':self.messages}})

    def checkGiftsAndMessages(self):
        for gift in self.client.shopGifts.split("/"):
            if not gift == "":
                values = binascii.unhexlify(gift.encode()).decode().split("|", 4)
                self.server.lastShopGiftID += 1
                self.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(self.server.lastShopGiftID).writeUTF(self.client.playerName).writeUTF(values[1]).writeBoolean(bool(values[1])).writeInt(int(values[3])).writeUTF(values[4] if len(values) > 4 or values[4] != '' else "").writeBoolean(False).toByteArray())
                self.server.shopGifts[self.server.lastShopGiftID] = [values[0], bool(values[2]), int(values[3])]

        for message in self.client.shopMessages.split("/"):
            if not message == "":
                values = binascii.unhexlify(message.encode()).decode().split("|", 4)
                self.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(0).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeInt(int(values[3])).writeUTF(values[4]).writeBoolean(True).toByteArray())

        self.client.shopGifts = ""
        self.client.shopMessages = ""
        
    def buyFullLook(self, visuID):
        p = ByteArray()
        shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")
        look = self.server.shopOutfitsCheck[visuID][0].split(";")
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
        promotion = float((100 - int(self.server.shopOutfitsCheck[visuID][2]))) / 100

        p.writeShort(int(visuID))
        p.writeByte(0)
        p.writeUTF(self.server.shopOutfitsCheck[visuID][0])

        p.writeByte(visuLength)

        for category in self.client.visuItems.keys():
            if len(self.client.visuItems.keys()) == category:
                category = 22
            itemID = self.client.getSimpleItemID(category, self.client.visuItems[category]["ID"])

            buy = [self.client.visuItems[category]["Buy"], int(self.client.visuItems[category]["Buy"] * promotion)]
            customBuy = [self.client.visuItems[category]["CustomBuy"], int(self.client.visuItems[category]["CustomBuy"] * promotion)]

            p.writeInt(self.client.visuItems[category]["ID"])
            p.writeByte(2 if self.client.visuItems[category]["Bonus"] else (1 if not self.client.Shop.checkInShop(self.client.visuItems[category]["ID"]) else 0))
            p.writeShort(buy[0])
            p.writeShort(buy[1])
            p.writeByte(3 if not self.client.visuItems[category]["Customizable"] else (2 if self.client.visuItems[category]["CustomBonus"] else (1 if self.client.visuItems[category]["HasCustom"] == False else 0)))
            p.writeShort(customBuy[0])
            p.writeShort(customBuy[1])
            
            allPriceBefore += buy[0] + customBuy[0]
            allPriceAfter += (0 if (self.client.visuItems[category]["Bonus"]) else (0 if self.client.Shop.checkInShop(itemID) else buy[1])) + (0 if (not self.client.visuItems[category]["Customizable"]) else (0 if self.client.visuItems[category]["CustomBonus"] else (0 if self.client.visuItems[category]["HasCustom"] else (customBuy[1]))))

        p.writeShort(allPriceBefore)
        p.writeShort(allPriceAfter)
        self.client.priceDoneVisu = allPriceAfter
        self.client.sendPacket(Identifiers.send.Buy_Full_Look, p.toByteArray())
        
    def buyFullLookConfirm(self, visuID, lookBuy):
        look = self.server.shopOutfitsCheck[str(visuID)][0].split(";")
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
                        if not self.checkInShop(itemID):
                            self.client.shopItems += str(itemID)+"_" if self.client.shopItems == "" else "," + str(itemID)+"_"
                            if not itemID in self.client.custom:
                                self.client.custom.append(itemID)
                            else:
                                if not str(itemID) in self.client.custom:
                                    self.client.custom.append(str(itemID))
                    else:
                        if not self.checkInShop(str(itemID)):
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
        self.sendShopList(False)
        
    def sendPromotions(self):
        for promotion in self.server.shopPromotions:
            self.client.sendPacket(Identifiers.send.Promotion, ByteArray().writeBoolean(True).writeBoolean(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBoolean(True).writeInt(promotion[3]).writeByte(promotion[2]).toByteArray())

        if len(self.server.shopPromotions) > 0:
            promotion = self.server.shopPromotions[0]
            item = promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)
            self.client.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeInt(promotion[0]).writeInt(promotion[1]).writeInt(promotion[2]).writeShort(self.server.shopBadges.get(item, 0)).toByteArray())
            



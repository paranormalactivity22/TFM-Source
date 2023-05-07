math.randomseed(os.time())
do
	local timer = 0
	local newGame = tfm.exec.newGame
	tfm.exec.newGame = function(map, flip)
		if not map then
			newGame(map, flip)
		else
			if os.time() > timer then
				timer = os.time() + 3000
				newGame(map, flip)
			end
		end
	end
end

local isTribeHouse = string.byte(tfm.get.room.name, 2) == 3

local fastMode, noShamanMode, noCollisionMode = false, false, false
local hasMode, hasModeRunning = false, true
if not isTribeHouse then
	local mode
	if string.find(tfm.get.room.name, "vanilla") then
		mode = "vanilla"
	elseif string.find(tfm.get.room.name, "village") then
		mode = "village"
	else
		if string.find(tfm.get.room.name, "fast") then
			fastMode = true
		end
		if string.find(tfm.get.room.name, "noshaman") then
			noShamanMode = true
		end
		if string.find(tfm.get.room.name, "nocollision") then
			noCollisionMode = true
		end

		hasMode = fastMode or noShamanMode or noCollisionMode
	end

	if mode then
		tfm.exec.chatMessage("<ROSE>You can't play <N>#crowdsurf</N> in " .. mode .. " rooms.")
		return
	end
end

local getParam
do
	local categories = { 1, 4, 5, 6, 7, 8, 9 }
	getParam = function()
		local out
		if isTribeHouse then
			out = "#" .. categories[math.random(#categories)]
		end
		return out
	end
end

local players = 0
eventNewPlayer = function(playerName)
	players = players + 1
	tfm.exec.chatMessage("<N>Welcome to <ROSE>#crowdsurf<N>. Survive or win to become the next shaman! Type <ROSE>!help</ROSE> for more info.", playerName)
end
table.foreach(tfm.get.room.playerList, eventNewPlayer)

eventPlayerLeft = function()
	players = players - 1
end

local toReload, map, shaman
local skip = false

local skipMap = function()
	toReload = nil

	tfm.exec.setGameTime(5, false)
	map = getParam()
end

eventNewGame = function()
	if not string.find(tfm.get.room.currentMap, '@') then
		skipMap()
		return
	end

	if not toReload then
		local xml = tfm.get.room.xmlMapInfo.xml

		if string.find(xml, "T=\"9\"") or string.find(xml, "T=\"15\"") then -- water or web doesn't disappear with the attribute v
			skipMap()
			return
		end

		if not hasMode then
			if hasModeRunning then
				fastMode = false
				noShamanMode = false
				noCollisionMode = false
			end

			if math.random(1, 8) == math.random(1, 8) then
				hasModeRunning = true
				local number = math.random(1, 3)

				local message = "<ROSE>The <N>%s</N> has been activated in this round. You can play more of it at <N>/room #crowdsurf0%s"
				if number == 1 then
					fastMode = true
					tfm.exec.chatMessage(string.format(message, "Fast Mode", "fast"))
				elseif number == 2 and not shaman then
					noShamanMode = true
					tfm.exec.chatMessage(string.format(message, "No Shaman Mode", "noshaman"))
				elseif number == 3 then
					noCollisionMode = true
					tfm.exec.chatMessage(string.format(message, "No Mice Collision Mode", "nocollision"))
				end
			end
		end

		local counter = 0
		xml = (string.gsub(xml, "<S ", function()
			counter = counter + 1
			return "<S v=\"" .. (5000 + counter * (fastMode and 500 or 2000)) .. "\" "
		end))

		xml = (string.gsub(xml, "defilante=\".-\"", ""))
		xml = (string.gsub(xml, "mgoc=\".-\"", ""))

		for i = 11, 16 do
			xml = (string.gsub(xml, "<O .-C=\"" .. i .. "\".->", ""))
		end
		xml = (string.gsub(xml, "<O .-C=\"22\".->", ""))

		if not noCollisionMode then
			xml = (string.gsub(xml, "<P ", function()
				return "<P C=\"\" "
			end))
		end
		
		if isTribeHouse then
			map = xml
		else
			tfm.exec.newGame(xml)
		end
		toReload = tfm.get.room.currentMap
		
		skip = true
	else
		if tfm.get.room.currentMap ~= "@0" then
			tfm.exec.setGameTime(6, false)
			skip = true
			return
		end
		skip = false

		map = nil

		tfm.exec.setGameTime(63)
		ui.setMapName("<N>" .. toReload)
		
		for playerName in next, tfm.get.room.playerList do
			if playerName ~= shaman then
				tfm.exec.giveMeep(playerName)
			end
		end
		
		if shaman then
			if not noShamanMode and tfm.get.room.playerList[shaman] then
				tfm.exec.setShaman(shaman)
			end
			shaman = nil
		end

		toReload = nil
	end
end

eventLoop = function(currentTime, remainingTime)
	if map and currentTime >= 3000 then
		tfm.exec.newGame(map)
	end
end

eventPlayerDied = function(playerName)
	if not skip then
		if shaman then
			if shaman == playerName then
				tfm.exec.setPlayerScore(shaman, -1, true)
				
				if not noShamanMode then
					tfm.exec.chatMessage("<ROSE>Just kidding, <N>" .. shaman .. "</N> will not be the next shaman :p")
				else
					tfm.exec.chatMessage("<ROSE>Ehhh, that was luck. <N>" .. shaman .. "</N> did not survive.")
				end
				shaman = nil
			end
			return
		end

		local survivor
		for playerName, playerData in next, tfm.get.room.playerList do
			if not playerData.isDead then
				if survivor then
					return
				end
				survivor = playerName
			end
		end
		
		tfm.exec.setGameTime(5, false)
		if survivor and players > 1 then
			shaman = survivor
			tfm.exec.setPlayerScore(shaman, 1, true)

			tfm.exec.addShamanObject(30, tfm.get.room.playerList[shaman].x, tfm.get.room.playerList[shaman].y + 30)

			if not noShamanMode then
				tfm.exec.chatMessage("<ROSE>The next shaman will be <N>" .. shaman)
			else
				tfm.exec.chatMessage("<N>" .. shaman .. " <ROSE>is the survivor!")
			end
		end
	end
end

eventPlayerWon = function(playerName)
	if not skip and not shaman then
		tfm.exec.setGameTime(15, false)

		shaman = playerName
		tfm.exec.setPlayerScore(shaman, 1, true)
		
		if not noShamanMode then
			tfm.exec.chatMessage("<ROSE>The next shaman will be <N>" .. shaman)
		else
			tfm.exec.chatMessage("<N>" .. shaman .. " <ROSE>won!")
		end
	end
end

eventChatCommand = function(playerName, command)
	if command == "help" then
		tfm.exec.chatMessage("<ROSE>Module rewritten by <N>Bolodefchoco</N> and initially released by <N>Baasbase#0095</N>.\nGame modes: <N>#crowdsurf0fast</N>, <N>#crowdsurf0noshaman</N>, <N>#crowdsurf0nocollision</N>\n<ROSE>Discord: https://discord.gg/quch83R", playerName)
	elseif command == "mort" then
		tfm.exec.killPlayer(playerName)
	end
end
system.disableChatCommandDisplay("help", true)

tfm.exec.disableAutoShaman()
tfm.exec.disableAutoScore()
tfm.exec.disableMortCommand()
tfm.exec.disableAllShamanSkills()

tfm.exec.newGame(getParam())
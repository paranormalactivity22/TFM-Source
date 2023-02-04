local module = {
	owner = "Bolodefchoco#0000",
	map_file = 1
}

-- Translations
local translations = {
	en = {
		-- Init
		welcome = "Welcome to <PS>#Signal<S>! Follow the traffic lights and join the hole! Use !help to read more informations and send maps in https://atelier801.com/topic?f=6&t=859064.\n\tReport any issue to Bolodefchoco#0000",
		
		-- Info
		info = {
			[1] = {"Run", "Run as fast as you can. Do not stop!"},
			[2] = {"Attention", "Pay attention! You can die in the next few seconds!"},
			[3] = {"Stop", "Stop or die!"},
		},
		
		-- Simple words
		close = "Close",
	},
	br = {
		welcome = "Bem-vindo ao <PS>#Signal<S>! Siga o semáforo e entre na toca!  Use !help para ler mais informações e envie mapas em https://atelier801.com/topic?f=6&t=859064.\n\tReporte qualquer problema para Bolodefchoco#0000",

		info = {
			[1] = {"Corra", "Corra o mais rápido que puder. Não pare!"},
			[2] = {"Atenção", "Preste atenção! Você poderá morrer a qualquer momento!"},
			[3] = {"Pare", "Pare ou morra!"},
		},

		close = "Fechar",
	},
	pl = {
		welcome = "Witaj w <PS>#Signal<S>! Patrz na tabliczke i wejdź do norki! Użyj komendy !help, aby przeczytać więcej informacji and send maps in https://atelier801.com/topic?f=6&t=859064.\n\tZgłoś wszystkie błędy jakie znajdziesz do Bolodefchoco#0000",
		
		info = {
			[1] = {"Biegnij", "Biegnij jak najszybciej do norki. Nie zatrzymuj się!"},
			[2] = {"Uważaj", "Uważaj! Możesz zginąć za kilka sekund!"},
			[3] = {"Stój", "Stój albo zgiń!"},
		},
		
		close = "Zamknij",
	},
	hu = {
		welcome = "Üdv a <PS>#Signal<S> modulban! Kövesd a jelzőlámpákat, és érj be a lyukba! Használd a !help parancsot, hogy több információt tudj meg, és küldj be pályákat az https://atelier801.com/topic?f=6&t=859064 oldalon.\n\tA hibákat Bolodefchoco#0000 játékosnak jelentheted.",
		
		info = {
			[1] = {"Futás", "Fuss olyan gyorsan, ahogyan csak tudsz. Ne állj meg!"},
			[2] = {"Vigyázat", "Figyelj oda! Meghalhatsz pár másodpercen belül!"},
			[3] = {"Állj", "Állj meg vagy meghalsz!"},
		},
		
		close = "Bezár",
	},
}
local translation = translations[tfm.get.room.community] or translations.en

--[[ Data ]]--
local info = {}
local mapEvaluators = {
	["Bolodefchoco#0000"] = true,
	["Grapeup#0000"] = true
}
local review = false

--[[ Maps ]]--
local maps = { "#17" }
local mapHashes = { }
local mapsToAdd = { }

local loading_maps = system.loadFile(module.map_file)
local reloader
reloader = system.newTimer(function()
	if not loading_maps then
		loading_maps = system.loadFile(module.map_file)
	end
end, 1000, true)

--[[ API ]]--
math.clamp = function(value, min, max)
	return value < min and min or value > max and max or value
end

string.split = function(value, pattern, f)
	local out = {}
	for v in string.gmatch(value, pattern) do
		out[#out + 1] = (not f and v or f(v))
	end
	return out
end
system.isPlayer = function(n)
	--[[
		The player must not be a souris;
		The player must have played Transformice for at least 5 days
	]]
	return not not (string.sub(n, 1, 1) ~= "*" and tfm.get.room.playerList[n] and (os.time() - (tfm.get.room.playerList[n].registrationDate or os.time())) >= 432e6)
end
system.players = function(alivePlayers)
	local alive, total = 0, 0
	if alivePlayers then
		alive = {}
	end

	for k, v in next, tfm.get.room.playerList do
		if system.isPlayer(k) then
			total = total + 1
			if not (v.isDead or v.isVampire) then
				if alivePlayers then
					alive[#alive + 1] = k
				else
					alive = alive + 1
				end
			end
		end
	end

	return alive, total
end

table.find = function(list, value, index, f)
	for k, v in next, list do
		local i = (type(v) == "table" and index) and v[index] or v
		if (not f and i or f(i)) == value then
			return true, k
		end
	end
	return false, 0
end
table.random = function(t)
	return t[math.random(#t)]
end
table.shuffle = function(t)
	local len = #t
	for i = len, 1, -1 do
		local rand = math.random(i)
		t[i], t[rand] = t[rand], t[i]
	end
	return t
end

ui.banner = function(image, aX, aY, n, time)
	time = time or 5
	aX = aX or 100
	aY = aY or 100

	local img = tfm.exec.addImage(image .. ".png", "&0", aX, aY, n)
	system.newTimer(function()
		tfm.exec.removeImage(img)
	end, time * 1000, false)
end

local xml = {}
xml.parseParameters = function(currentXml)
	currentXml = string.match(currentXml, "<P (.-)/>") or ""
	local out = {}
	for tag, _, value in string.gmatch(currentXml, "([%-%w]+)=([\"'])(.-)%2") do
		out[tag] = value
	end
	return out, currentXml
end
xml.attribFunc = function(currentXml, funcs)
	local attributes, properties = xml.parseParameters(currentXml)
	for k, v in next, funcs do
		if attributes[v.attribute] then
			v.func(attributes[v.attribute])
		end
	end
	return properties
end

--[[ Settings ]]--
-- New Game
local sys = {0, 1}
local discrepancy = 0
local lights = {"15b52f8717d", "15b52f8583a", "15b52f88765"}
local lightId = -1
local lightTime = {{3, 5}, {2, 3}, {7, 13}}
local rounds = 0

--[[ System ]]--
-- UpdateLight
local update = function(id)
	tfm.exec.removeImage(lightId)
	lightId = tfm.exec.addImage(lights[sys[2]] .. ".png", "&0", 375, 30)
	local color = ({0x1CB70C, 0xF4D400, 0xEC0000})[sys[2]]
	for k, v in next, info do
		if id == 1 then
			if not v.afk and v.canRev then
				tfm.exec.respawnPlayer(k)
			end
		end
		tfm.exec.setNameColor(k, color)
	end
end
-- Load new map
local loadMap = function()
	rounds = rounds + 1
	if rounds > #maps then
		maps = table.shuffle(maps)
		rounds = 1
	end
	
	tfm.exec.newGame(maps[rounds])
end
-- Valid map code
local mapCode = function(x)
	if string.sub(x, 1, 1) == "@" then
		x = string.sub(x, 2)
	end

	local str = x
	x = tonumber(x)
	return x, not not x and #str > 3
end

--[[ UI ]]--
local displayInfo = function(n, id)
	local color = ({"<VP>", "<J>", "<R>"})[id]
	ui.addTextArea(1, "<p align='center'><font size='25'>" .. color .. translation.info[id][1] .. "\n</font></p><p align='left'><font size='14'>" .. translation.info[id][2], n, 250, 110, 300, 181, 0x324650, 0x27343A, 1, true)
	ui.addTextArea(2, "<font size='2'>\n</font><p align='center'><font size='16'><a href='event:close'>" .. translation.close, n, 250, 300, 300, 30, 0x27343A, 0x27343A, 1, true)
	ui.addTextArea(3, "<p align='center'><font size='20'><a href='event:info.1'><VP>•</a> <a href='event:info.2'><J>•</a> <a href='event:info.3'><R>•</a>", n, 250, 145, 300, 30, 1, 1, 0, true)
	tfm.exec.removeImage(info[n].imageId)
	info[n].imageId = tfm.exec.addImage(lights[id] .. ".png", "&1", 375, 200, n)
end

--[[ Events ]]--
-- NewPlayer
eventNewPlayer = function(n)
	if not info[n] then
		info[n] = {
			isMoving = {false, false, false, false},
			imageId = -1,
			afk = true,
			skipped = false,
			canRev = true,
		}
	end
	for i = 0, 3 do
		system.bindKeyboard(n, i, true, true)
		system.bindKeyboard(n, i, false, true)
	end
	tfm.exec.chatMessage("<S>" .. translation.welcome .. "\n\t<ROSE>Discord: https://discord.gg/quch83R", n)
	tfm.exec.lowerSyncDelay(n)
	--ui.banner("15d60d9212c", 220, 130, n)
end
-- NewGame
eventNewGame = function()
	ui.setMapName(tfm.get.room.xmlMapInfo.author .. " <BL>- " .. tfm.get.room.currentMap .. "   <G>|   <N>Round : <V>" .. rounds)
	
	for k, v in next, info do
		v.isMoving = {false, false, false, false}
		v.afk = true
		v.skipped = false
		v.canRev = true
	end
	
	sys = {0, 1}
	update(sys[2])
	
	lightTime = {{7, 13}, {2, 3}, {3, 5}}
	xml.attribFunc((tfm.get.room.xmlMapInfo or {}).xml or "", {
		[1] = {
			attribute = "light",
			func = function(value)
				value = string.lower(value)
				
				local normalizator = function(v)
					return math.clamp(tonumber(v), 1, 13)
				end
				
				local axis, interval = string.match(value, "^([gyr]);(%d+ ?, ?%d+)")
				if axis and interval then
					local _, index = table.find({'g', 'y', 'r'}, axis)
					interval = string.split(interval, "[^ ?, ?]+", normalizator)
					table.sort(interval)
					lightTime[tonumber(index)] = interval
				else
					axis = string.split(value, "[^;]+")
					if #axis > 0 then
						for i = 1, #axis do
							interval = string.split(axis[i], "[^ ?, ?]+", normalizator)
							table.sort(interval)
							lightTime[i] = interval
						end
					end
				end
			end
		}
	})

	if review then
		for k in next, mapEvaluators do
			tfm.exec.chatMessage(string.format("<PS>" .. tfm.get.room.currentMap .. " : <PT>|%s:%s| <J>|%s:%s| <R>|%s:%s|", lightTime[1][1], lightTime[1][2], lightTime[2][1], lightTime[2][2], lightTime[3][1], lightTime[3][2]), k)
		end
	end
end
-- Keyboard
eventKeyboard = function(n, k, d)
	if sys[2] == 3 and d and os.time() > discrepancy then
		tfm.exec.killPlayer(n)
	else
		info[n].isMoving[k + 1] = d
	end
	info[n].afk = false
end
-- Loop
eventLoop = function(currentTime, leftTime)
	if currentTime > 8000 then
		if os.time() > sys[1] then
			sys[2] = (sys[2] % 3) + 1
			sys[1] = os.time() + ({math.random(lightTime[1][1], lightTime[1][2]), math.random(lightTime[2][1], lightTime[2][2]), math.random(lightTime[3][1], lightTime[3][2])})[sys[2]] * 1000
			update(sys[2])
			discrepancy = os.time() + 520
		end
	end

	if leftTime > 2000 and system.players() > 0 then
		if sys[2] == 3 and os.time() > discrepancy then
			for k, v in next, info do
				for i, j in next, v.isMoving do
					if j then
						tfm.exec.killPlayer(k)
						break
					end
				end
			end
		end
	else
		if not review then
			loadMap()
		end
	end
end
-- TextAreaCallback
eventTextAreaCallback = function(i, n, c)
	local p = string.split(c, "[^%.]+")
	if p[1] == "info" then
		displayInfo(n, tonumber(p[2]))
	elseif p[1] == "close" then
		tfm.exec.removeImage(info[n].imageId)
		for i = 1, 3 do
			ui.removeTextArea(i, n)
		end
	end
end
-- ChatCommand
eventChatCommand = function(n, c)
	local p = string.split(c, "%S+", string.lower)

	if p[1] == "info" or p[1] == "help" or p[1] == "?" then
		eventTextAreaCallback(nil, n, "info." .. sys[2])
	elseif p[1] == "speak" and n == module.owner then
		tfm.exec.chatMessage("<S><B>[#signal] " .. table.concat(p, " ", 2) .. "</B>")
	else
		if mapEvaluators[n] then
			if p[1] == "review" then
				review = not review
				tfm.exec.chatMessage("<S>REVIEW : " .. string.upper(tostring(review)))
				tfm.exec.disableAfkDeath(review)
			elseif p[1] == "ls" then
				local m = { }
				for k, v in next, maps do
					m[k] = (mapsToAdd[v] and "<R>@" or "@") .. v
				end

				tfm.exec.chatMessage("Total maps: <J>" .. #maps .. " <BL>: " .. table.concat(m, ", "), n)
			elseif p[1] == "data" and n == module.owner then
				if #maps == 0 then
					tfm.exec.chatMessage("<R>You can not save an empty queue.", n)
				else
					mapsToAdd = { }

					local data = table.concat(maps, '@')
					system.saveFile(data, module.map_file)

					for name in next, mapEvaluators do
						tfm.exec.chatMessage("[database] Total maps: <J>" .. #maps .. " <BL>: @" .. table.concat(maps, ", @"), name)
					end
				end
			elseif p[2] then
				if (p[1] == "np" or p[1] == "map") and review then
					tfm.exec.newGame(p[2])
				elseif not reloader then
					local data = table.concat(p, " ", 2)
					if p[1] == "add" then
						local entries = string.split(data, "[^, ]+")

						if entries then
							for map = 1, #entries do
								local code, isCode = mapCode(entries[map])
								if isCode and not mapHashes[code] then
									maps[#maps + 1] = code
									mapHashes[code] = true
									mapsToAdd[code] = true
									tfm.exec.chatMessage("<BL>The map <J>@" .. code .. "</J> is now in the map queue.")
								end
							end
						end
					elseif p[1] == "del" then
						local entries = string.split(data, "[^, ]+")

						if entries then
							for map = 1, #entries do
								local code, isCode = mapCode(entries[map])
								if isCode and mapHashes[code] then
									for o_map = 1, #maps do
										if maps[o_map] == code then
											table.remove(maps, o_map)
											break
										end
									end
									mapHashes[code] = nil
									tfm.exec.chatMessage("<BL>The map <J>@" .. code .. "</J> was removed from the map queue.")
								end
							end
						end
					end
				end
			end

			if not string.find(tfm.get.room.name, "^*?#signal%d*$") then
				if p[1] == "next" then
					loadMap()
				elseif p[1] == "again" then
					tfm.exec.newGame(tfm.get.room.currentMap)
				end
			end
		end
	end
end
-- PlayerWon
eventPlayerWon = function(n)
	info[n].canRev = review
	tfm.exec.setGameTime(40, false)
	
	if review then
		tfm.exec.respawnPlayer(n)
	end
end
-- FileLoaded
eventFileLoaded = function(id, data)
	system.removeTimer(reloader)
	reloader = nil

	local counter = 0
	maps, mapHashes = { }, { }
	string.gsub(data, "[^@]+", function(code)
		counter = counter + 1

		code = tonumber(code) or code
		maps[counter] = code
		mapHashes[code] = true
	end)
	maps = table.shuffle(maps)
end

table.turnTable = function(x)
	return (type(x)=="table" and x or { x })
end
table.merge = function(this,src)
	for k, v in next, src do
		if this[k] then
			if type(v) == "table" then
				this[k] = table.turnTable(this[k])
				table.merge(this[k], v)
			else
				this[k] = this[k] or v
			end
		else
			this[k] = v
		end
	end
end

for k, v in next, translations do
	if k ~= "en" then
		table.merge(v, translations.en)
	end
end

for _, f in next, {"AutoShaman", "AutoNewGame", "AutoTimeLeft", "PhysicalConsumables"} do
	tfm.exec["disable"..f]()
end
table.foreach(tfm.get.room.playerList, eventNewPlayer)

system.disableChatCommandDisplay(nil, true)

maps = table.shuffle(maps)

loadMap()
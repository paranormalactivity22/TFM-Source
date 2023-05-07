local module = {
	owner = "Bolodefchoco#0015",
	id = "cn",
	min_mice = 4,
	map_file = 0,
	xp_per_30_sec = 5,
	xp_per_victory = 15
}

--[[ Translations ]]--
local translations = {
	en = {
		-- Init
		welcome = "Welcome to #cannonup. Your aim is to be the survivor!\n<VP>Press <B>P</B> to open your profile or <B>!p nickname</B> to see someone's profile!\n<J>Submit maps in <S>https://atelier801.com/topic?f=6&t=859067\n\t<J>Report any issue to Bolodefchoco#0015.",

		-- Info
		nowinner = "No one won!",

		-- Simple words
		soon = "Soon!",
		won = "won!",

		-- Profile
		profile = { "Rounds", "Victories", "Badges" },

		-- Titles
		unlock = "%s just unlocked the title «%s»",
		titlecmd = "Type !title to change your title.",
		titlemsg = "Type !title X to choose a title in the list below :",
		usetitle = "Your new title is <CH>«%s»",
		titles = {
			[1] = {
				[1] = "Survivor",
				[2] = "Veteran",
				[3] = "Blessed",
				[4] = "Anti Robot",
				[5] = "Addicted",
				[6] = "King of the Hill",
				[7] = "Psychedelic Mouse"
			},
			[2] = {
				[1] = "Leve Mouse",
				[2] = "Cannon Boy",
				[3] = "Unkillable Mouse",
				[4] = "Undetectable Mouse",
				[5] = "Warrior",
				[6] = "Explosion",
				[7] = "F = Mouse * A",
				[8] = "Matrix",
				[9] = "Survivor Master",
			},
			[3] = {
				[1] = "Watermelon",
				[2] = "Mapmaker", -- at least 5 maps in the module
				[3] = "Dodger", -- desviar de x cn
				[4] = "Parkour Mouse", -- jump 120x
			}
		}
	},
	br = {
		welcome = "Bem-vindo ao #cannonup. Seu objetivo é ser o sobrevivente!\n<VP>Aperte <B>P</B> para abrir seu perfil ou <B>!p nickname</B> para ver o perfil de alguém!\n<J>Envie mapas em <S>https://atelier801.com/topic?f=6&t=859067\n\t<J>Reporte qualquer problema para Bolodefchoco#0015.",

		nowinner = "Ninguém ganhou!",

		soon = "Em breve!",
		won = "venceu!",

		profile = { "Partidas", "Vitórias", "Medalhas" },

		unlock = "%s desbloqueou o título «%s»",
		titlecmd = "Digite !title para mudar seu título.",
		titlemsg = "Digite !title X para escolher um título na lista abaixo :",
		usetitle = "Seu novo título é <CH>«%s»",
		titles = {
			[1] = {
				[1] = "Survivor",
				[2] = "Veterano",
				[3] = "Abençoado",
				[4] = "Anti Robô",
				[5] = "Viciado",
				[6] = "Rei da Colina",
				[7] = "Rato Psicodélico"
			},
			[2] = {
				[1] = "Rato Leve",
				[2] = "Cannon Boy",
				[3] = "Rato Imortal",
				[4] = "Rato Indetectável",
				[5] = "Guerreiro",
				[6] = "Explosão",
				[7] = "F = Mouse * A",
				[8] = "Matrix",
				[9] = "Mestre Survivor",
			},
			[3] = {
				[1] = "Melancia",
				[2] = "Mapper", -- at least 5 maps in the module
				[3] = "Dodger", -- desviar de x cn
				[4] = "Rato do Parkour", -- jump 120x
			}
		}
	},
}
local translation = translations[tfm.get.room.community] or translations.en

--[[ Data ]]--
local mapEvaluators = {
	["Bolodefchoco#0015"] = true,
	["Acer#0010"] = true,
	["Jota#0676"] = true,
	["Grapeup#0020"] = true
}
local artist = {
	["Flindix#0095"] = true
}
local keys = {
	P = string.byte('P')
}
local badges = {
	{ 2^0, "1660271f4c6.png" }, -- Map Reviewer
	{ 2^1, "165df979c2f.png" }, -- Artist
	{ 2^2, "165df891e2a.png" }, -- Mapper (more than 5)
}
local titles = {
	-- Rounds, Victories, Challenges
	[1] = {
		[1] = 0,
		[2] = 50,
		[3] = 150,
		[4] = 250,
		[5] = 450,
		[6] = 750,
		[7] = 1000
	},
	[2] = {
		[1] = 10,
		[2] = 50,
		[3] = 70,
		[4] = 150,
		[5] = 250,
		[6] = 320,
		[7] = 450,
		[8] = 500,
		[9] = 1000
	},
	[3] = {
		[1] = { 2^0, true },
		[2] = { 2^1, true },
		[3] = { 2^2, true },
		[4] = { 2^3, true }
	}
}

--[[ Data Handler ]]--
local DataHandler = {}
DataHandler.VERSION = '1.3.3'
DataHandler.__index = DataHandler

function DataHandler.new(moduleID, skeleton, otherOptions)
	local self = setmetatable({}, DataHandler)

	assert(moduleID, 'Invalid module ID (nil)')
	assert(moduleID ~= '', 'Invalid module ID (empty text)')
	assert(skeleton, 'Invalid skeleton (nil)')

	for k, v in next, skeleton do
		v.type = v.type or type(v.default)
	end

	self.players = {}
	self.moduleID = moduleID
	self.moduleSkeleton = skeleton
	self.moduleIndexes = {}
	self.otherOptions = otherOptions
	self.otherData = {}
	self.originalStuff = {}

	for k,v in pairs(skeleton) do
		self.moduleIndexes[v.index] = k
	end

	if self.otherOptions then
		self.otherModuleIndexes = {}
		for k,v in pairs(self.otherOptions) do
			self.otherModuleIndexes[k] = {}
			for k2,v2 in pairs(v) do
				self.otherModuleIndexes[k][v2.index] = k2
			end
		end
	end

	return self
end

function DataHandler.newPlayer(self, name, dataString)
	assert(name, 'Invalid player name (nil)')
	assert(name ~= '', 'Invalid player name (empty text)')

	self.players[name] = {}
	self.otherData[name] = {}

	dataString = dataString or ''
	self.originalStuff[name] = dataString

	-- turns a simple table into a string
	local function turnStringToTable(str)
		local output = {}
		for data in string.gsub(str, '%b{}', function(b) return b:gsub(',', '\0') end):gmatch('[^,]+') do
		-- for data in string.gsub(str, '({.*()})', function(b) return b:gsub(',', '\0') end):gmatch('[^,]+') do
			data = data:gsub('%z', ',')

			if string.match(data, '^{.-}$') then
				table.insert(output, turnStringToTable(string.match(data, '^{(.-)}$')))
			else
				table.insert(output, tonumber(data) or data)
			end
		end
		return output
	end

	-- get the field index
	local function getDataIndexName(skeleton, index)
		for k,v in pairs(skeleton) do
			if v.index == index then
				return k
			end
		end
		return 0
	end

	-- gets the higher index
	local function getHigherIndex(skeleton)
		local higher = 0
		for k,v in pairs(skeleton) do
			if v.index > higher then
				higher = v.index
			end
		end
		return higher
	end

	-- creates the fields in the player's table
	-- loads the other modules' data too
	local function handleModuleData(moduleID, skeleton, moduleData, makeTable)
		local dataIndex = 1
		local higherIndex = getHigherIndex(skeleton)

		if makeTable then
			self.players[name]['__'..moduleID] = {}
		end

		local setPlayerData = function(data, dataType, dataName, dataDefault)

			if dataType == 'number' then
				if makeTable then
					self.players[name]['__'..moduleID][dataName] = tonumber(data) or dataDefault
				else
					self.players[name][dataName] = tonumber(data) or dataDefault
				end
			elseif dataType == 'string' then
				if makeTable then
					if string.match(data or '', '^".-"$') then
						self.players[name]['__'..moduleID][dataName] = string.match(data, '^"(.-)"$')
					else
						self.players[name]['__'..moduleID][dataName] = dataDefault
					end
				else
					if string.match(data or '', '^".-"$') then
						self.players[name][dataName] = string.match(data, '^"(.-)"$')
					else
						self.players[name][dataName] = dataDefault
					end
				end
			elseif dataType == 'table' then
				if makeTable then
					if string.match(data or '', '^{.-}$') then
						self.players[name]['__'..moduleID][dataName] = turnStringToTable(string.match(data, '^{(.-)}$'))
					else
						self.players[name]['__'..moduleID][dataName] = dataDefault
					end
				else
					if string.match(data or '', '^{.-}$') then
						self.players[name][dataName] = turnStringToTable(string.match(data, '^{(.-)}$'))
					else
						self.players[name][dataName] = dataDefault
					end
				end
			elseif dataType == 'boolean' then
				if makeTable then
					self.players[name]['__'..moduleID][dataName] = data and (tonumber(data) == 1) or dataDefault
				else
					self.players[name][dataName] = data and (tonumber(data) == 1) or dataDefault
				end
			end
		end

		if #moduleData > 0 then
			for data in string.gsub(moduleData, '%b{}', function(b) return b:gsub(',', '\0') end):gmatch('[^,]+') do
			-- for data in string.gsub(moduleData, '({.*()})', function(b) return b:gsub(',', '\0') end):gmatch('[^,]+') do
				data = data:gsub('%z', ',')

				-- pega info a respeito do esqueleto
				local dataName = getDataIndexName(skeleton, dataIndex)
				local dataType = skeleton[dataName].type
				local dataDefault = skeleton[dataName].default

				setPlayerData(data, dataType, dataName, dataDefault)

				dataIndex = dataIndex + 1
			end
		end

		-- fields are missing, will set them to default
		if dataIndex <= higherIndex then
			for i = dataIndex, higherIndex do
				local dataName = getDataIndexName(skeleton, i)
				local dataType = skeleton[dataName].type
				local dataDefault = skeleton[dataName].default

				setPlayerData(nil, dataType, dataName, dataDefault)
			end
		end
	end

	local modules, originalStuff = self:getModuleData(dataString)

	-- keeps other unrelated stuff
	self.originalStuff[name] = originalStuff

	if not modules[self.moduleID] then
		modules[self.moduleID] = '{}'
	end

	handleModuleData(self.moduleID, self.moduleSkeleton, modules[self.moduleID]:sub(2,-2), false)

	if self.otherOptions then
		-- if the player does not have the other modules' data and we need them
		-- then creates the data using the default values provided
		for moduleID, skeleton in pairs(self.otherOptions) do
			if not modules[moduleID] then
				local strBuilder = {}
				for k,v in pairs(skeleton) do
					if v.type == 'string' then
						strBuilder[v.index] = '"'..tostring(v.default)..'"'
					elseif v.type == 'table' then
						strBuilder[v.index] = '{}'
					elseif v.type == 'number' then
						strBuilder[v.index] = v.default
					end
				end
				modules[moduleID] = '{'..table.concat(strBuilder, ',')..'}'
			end
		end
	end

	-- loads the player's data from other modules
	for moduleID, moduleData in pairs(modules) do
		if moduleID ~= self.moduleID then
			if self.otherOptions and self.otherOptions[moduleID] then
				handleModuleData(moduleID, self.otherOptions[moduleID], moduleData:sub(2,-2), true)
			else
				self.otherData[name][moduleID] = moduleData
			end
		end
	end
end

function DataHandler.dumpPlayer(self, name)
	-- dumps player data to string
	local output = {}

	-- turns a simple table into a string
	local function turnTableToString(tbl)
		local output = {}
		for k,v in pairs(tbl) do
			if type(v) == 'table' then
				output[#output+1] = '{'
				output[#output+1] = turnTableToString(v)

				if output[#output]:sub(-1) == ',' then
					output[#output] = output[#output]:sub(1, -2)
				end
				output[#output+1] = '}'
				output[#output+1] = ','
			else
				if type(v) == 'string' then
					output[#output+1] = '"'
					output[#output+1] = v
					output[#output+1] = '"'
				elseif type(v) == 'boolean' then
					output[#output+1] = v and '1' or '0'
				else
					output[#output+1] = v
				end
				output[#output+1] = ','
			end
		end
		if output[#output] == ',' then
			output[#output] = ''
		end
		return table.concat(output)
	end

	-- returns a module's data in string
	local function getPlayerDataFrom(name, moduleID)
		local output = {moduleID, '=', '{'}
		local player = self.players[name]
		local moduleIndexes = self.moduleIndexes
		local moduleSkeleton = self.moduleSkeleton

		if self.moduleID ~= moduleID then
			moduleIndexes = self.otherModuleIndexes[moduleID]
			moduleSkeleton = self.otherOptions[moduleID]
			moduleID = '__'..moduleID
			player = self.players[name][moduleID]
		end

		for i = 1, #moduleIndexes do
			local dataName = moduleIndexes[i]

			if moduleSkeleton[dataName].type == 'string' then
				-- inserts "string"
				output[#output+1] = '"'
				output[#output+1] = player[dataName]
				output[#output+1] = '"'

			elseif moduleSkeleton[dataName].type == 'number' then
				-- inserts number
				output[#output+1] = player[dataName]

			elseif moduleSkeleton[dataName].type == 'boolean' then
				output[#output+1] = player[dataName] and '1' or '0'

			elseif moduleSkeleton[dataName].type == 'table' then
				-- inserts table
				output[#output+1] = '{'
				output[#output+1] = turnTableToString(player[dataName])
				output[#output+1] = '}'
			end

			output[#output+1] = ','
		end

		if output[#output] == ',' then
			output[#output] = '}'
		else
			output[#output+1] = '}'
		end

		return table.concat(output)
	end

	output[#output+1] = getPlayerDataFrom(name, self.moduleID)

	-- builds the output
	if self.otherOptions then
		for k,v in pairs(self.otherOptions) do
			output[#output+1] = ','
			output[#output+1] = getPlayerDataFrom(name, k)
		end
	end

	for k,v in pairs(self.otherData[name]) do
		output[#output+1] = ','
		output[#output+1] = k
		output[#output+1] = '='
		output[#output+1] = v
	end

	return table.concat(output)..self.originalStuff[name]
end

function DataHandler.get(self, name, dataName, moduleName)
	-- returns some player data
	if not moduleName then
		return self.players[name][dataName]
	else
		assert(self.players[name]['__'..moduleName], 'Module data not available ('..moduleName..')')
		return self.players[name]['__'..moduleName][dataName]
	end
end

function DataHandler.set(self, name, dataName, value, moduleName)
	-- sets some player data

	if moduleName then
		self.players[name]['__'..moduleName][dataName] = value
	else
		self.players[name][dataName] = value
	end

	return self
end

function DataHandler.save(self, name)
	-- tbl:set():save("Smth")
	system.savePlayerData(name, self:dumpPlayer(name))
end

function DataHandler.getModuleData(self, str)
	local output = {}

	for moduleID, moduleData in string.gmatch(str, '([0-9A-Za-z_]+)=(%b{})') do
		output[moduleID] = moduleData
	end

	local strCopy = str
	for k,v in pairs(output) do
		strCopy = strCopy:gsub(k..'='..v:gsub("[%(%)%.%%%+%-%*%?%[%]%^%$]", "%%%0")..',?', '')
	end
	return output, strCopy
end

local playerData = DataHandler.new(module.id, {
	rounds = {
		index = 1,
		default = 0
	},
	victories = {
		index = 2,
		default = 0
	},
	xp = {
		index = 3,
		default = 21
	},
	badges = {
		index = 4,
		default = 0
	},
	titles = {
		index = 5,
		default = { 11, 1, 0, 0 } -- Wearing title ((cat - 1) .. id), Round, Victory, Challenge
	},
})
local playerCache = { }

local xpToLvl = function(xp)
	local last, total, level, remain, need = 20, 0, 0, 0, 0
	for i = 1, 100 do
		local nlast = last + (i - ((i < 26 and 1 or i < 46 and 20 or 30)))
		local ntotal = total + nlast

		if ntotal >= xp then
			level, remain, need = i - 1, xp - total, ntotal - xp
			return level, remain, need
		else
			last, total = nlast, ntotal
		end
	end
end

local lvlToXp = function(lvl)
	local last, total = 20, 0
	for i = 1, lvl do
		last = last + (i - ((i < 26 and 1 or i < 46 and 20 or 30)))
		total = total + last
	end

	return last, total
end

--[[ Maps ]]--
local maps = { 6001536, 6001536, 4591929, "#10" }
local mapHashes = { }
local mapsToAdd = { }

local loading_maps = system.loadFile(module.map_file)
local reloader
reloader = system.newTimer(function()
	if not loading_maps then
		loading_maps = system.loadFile(module.map_file)
	end
end, 1000, true)

--[[ Settings ]]--
-- Status
local players = {
	room = { _count = 0 },
	alive = { _count = 0 },
	currentRound = { _count = 0 }
}
local soloGame = false
local review = false
-- New Game
local cannon = {
	x = 0,
	y = 0,
	time = 2.5,
	quantity = 1,
	speed = 25,
	mul = 1,
}
local toSpawn = {}
local toDespawn = {}
local currentRound = 1
local announceWinner = true
local wasReview = false
local cannonID = {}
local mapSettingsReview = false
-- Hard mode
local hardMode = string.find(tfm.get.room.name, "*?#cannonup%d+hard$") and 2 or 0
-- Data
local canSave
do
	local isRoom = string.byte(tfm.get.room.name, 2) ~= 3
	canSave = function()
		return isRoom and tfm.get.room.uniquePlayers >= module.min_mice and not review and not wasReview
	end
end

--[[ API ]]--
math.clamp = function(value, min, max)
	return value < min and min or value > max and max or value
end

string.nick = function(player, ignoreCheck)
	if not ignoreCheck and not player:find("#") then
		player = player .. "#0000"
	end

	return string.gsub(string.lower(player), "%a", string.upper, 1)
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

table.copy = function(list)
	local out = {}
	for k, v in next, list do
		out[k] = (type(v) == "table" and table.copy(v) or v)
	end
	return out
end
table.merge = function(this, src)
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
table.random = function(t, q)
	return t[math.random(q or #t)]
end
table.shuffle = function(t)
	local len = #t
	for i = len, 1, -1 do
		local rand = math.random(i)
		t[i], t[rand] = t[rand], t[i]
	end
	return t
end
table.turnTable = function(x)
	return (type(x)=="table" and x or {x})
end
local insert = function(where, playerName)
	if not where[playerName] and system.isPlayer(playerName) then
		where._count = where._count + 1
		where[where._count] = playerName
		where[playerName] = where._count
	end
end
local remove = function(where, playerName)
	if where[playerName] then
		where._count = where._count - 1
		table.remove(where, where[playerName])
		for i = where[playerName], where._count do
			where[where[i]] = where[where[i]] - 1
		end
		where[playerName] = nil
	end
end

local timer
do
	timer = {
		_timers = {
			_count = 0
		}
	}

	timer.start = function(callback, ms, times, ...)
		local t = timer._timers
		t._count = t._count + 1

		t[t._count] = {
			id = t._count,
			callback = callback,
			args = { ... },
			defaultMilliseconds = ms,
			milliseconds = ms,
			times = times
		}
		t[t._count].args[#t[t._count].args + 1] = t[t._count]

		return t._count
	end

	timer.delete = function(id)
		timer._timers[id] = nil
	end

	timer.loop = function()
		local t
		for i = 1, timer._timers._count do
			t = timer._timers[i]
			if t then
				t.milliseconds = t.milliseconds - 500
				if t.milliseconds <= 0 then
					t.milliseconds = t.defaultMilliseconds
					t.times = t.times - 1

					t.callback(table.unpack(t.args))
					if t.times == 0 then
						timer.delete(i)
					end
				end
			end
		end
	end
end

ui.banner = function(image, aX, aY, n, time)
	time = time or 5
	aX = aX or 100
	aY = aY or 100

	local img = tfm.exec.addImage(image .. ".png", "&0", aX, aY, n)
	timer.start(tfm.exec.removeImage, time * 1000, 1, img)
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
	for k,v in next, funcs do
		if attributes[v.attribute] then
			v.func(attributes[v.attribute])
		end
	end
	return properties
end
xml.getCoordinates = function(s)
	if string.find(s, ";") then
		local x, y
		local axis, value = string.match(s, "(%a);(%-?%d+)")
		value = tonumber(value)
		if value then
			if axis == "x" then
				x = value
			elseif axis == "y" then
				y = value
			end
		end
		return x or 0, y or 0
	else
		local pos = {}
		for x, y in string.gmatch(s, "(%-?%d+) ?, ?(%-?%d+)") do
			pos[#pos + 1] = { x = x, y = y }
		end
		return pos
	end
end

--[[ System ]]--
-- Translations
for k, v in next, translations do
	if k ~= "en" then
		table.merge(v, translations.en, true)
	end
end

-- Cannon
local getCannon
do
	local currentMonth = tonumber(os.date("%m"))
	local cannons = { 17, 17, 17, 1706 }
	if currentMonth == 1 or currentMonth == 12 then
		cannons[#cannons + 1] = 1703 -- Christmas decoration
		cannons[#cannons + 1] = 1703
		cannons[#cannons + 1] = 1705 -- Apple
	elseif currentMonth == 2 then
		cannons[#cannons + 1] = 1701 -- Glass
		cannons[#cannons + 1] = 1705
		cannons[#cannons + 1] = 1706 -- Watermelon
		cannons[#cannons + 1] = 1706
	elseif currentMonth > 2 and currentMonth < 10 then
		if currentMonth == 5 then
			cannons[#cannons + 1] = 1704 -- Shaman
			cannons[#cannons + 1] = 1704
			cannons[#cannons + 1] = 1704
			cannons[#cannons + 1] = 1709 -- Light
		elseif currentMonth > 5 and currentMonth < 9 then
			cannons[#cannons + 1] = 1705
			cannons[#cannons + 1] = 1705
			cannons[#cannons + 1] = 1710 -- Nut
		elseif currentMonth == 9 then
			cannons[#cannons + 1] = 1711 -- Flower
		end
		cannons[#cannons + 1] = 1706
		cannons[#cannons + 1] = 1706
	elseif currentMonth == 10 then
		cannons[#cannons + 1] = 1701
		cannons[#cannons + 1] = 1702 -- Lollipop
		cannons[#cannons + 1] = 1702
		cannons[#cannons + 1] = 1702
		cannons[#cannons + 1] = 1707 -- Purple
		cannons[#cannons + 1] = 1708 -- Spike
	end

	getCannon = function()
		if #cannonID > 0 then
			return table.random(cannonID)
		end
		return table.random(cannons)
	end
end

-- Shoot
local newCannon = function()
	if players.alive._count > 0 then
		local player
		repeat
			player = tfm.get.room.playerList[table.random(players.alive, players.alive._count)]
		until not player or not player.isDead
		if not player then return end

		local coordinates = {
			{ player.x, math.random() * 700 },
			{ player.y, math.random() * 300 },
			{ false, false }
		}

		local id
		if type(cannon.x) == "table" then
			id = math.random(#cannon.x)
			coordinates[1][2] = cannon.x[id]
			coordinates[3][1] = true
		else
			if cannon.x ~= 0 then
				coordinates[1][2] = cannon.x
				coordinates[3][1] = true
			end
		end

		if type(cannon.y) == "table" then
			coordinates[2][2] = cannon.y[id]
			coordinates[3][2] = true
		else
			if cannon.y ~= 0 then
				coordinates[2][2] = cannon.y
				coordinates[3][2] = true
			end
		end

		if not coordinates[3][2] and coordinates[2][2] > coordinates[2][1] then
			coordinates[2][2] = coordinates[2][1] - math.random(100) - 35
		end
		if not coordinates[3][1] and math.abs(coordinates[1][2] - coordinates[1][1]) > 350 then
			coordinates[1][2] = coordinates[1][1] + math.random(-100,100)
		end

		local ang = math.deg(math.atan2(coordinates[2][2] - coordinates[2][1],coordinates[1][2] - coordinates[1][1]))
		tfm.exec.addShamanObject(0, coordinates[1][2] - (coordinates[3][1] and 0 or 10), coordinates[2][2] - (coordinates[3][2] and 0 or 10), ang + 90)

		toSpawn[#toSpawn + 1] = { os.time() + 150, getCannon(), coordinates[1][2], coordinates[2][2], ang - 90, cannon.speed }
	end
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

-- Unlock title
local unlockTitle = function(playerName, category, id)
	tfm.exec.chatMessage("<CH>" .. string.format(translation.unlock, playerName, translation.titles[category][id]))
	tfm.exec.chatMessage("<BV>" .. translation.titlecmd, playerName)
end

-- Check title (for round and victory only)
local checkTitle = function(playerName, category)
	local titleData = playerData:get(playerName, "titles")

	local id = category + 1
	local newTitle = titles[category][titleData[id] + 1]

	if newTitle and newTitle <= playerData:get(playerName, (category == 1 and "rounds" or "victories")) then
		titleData[id] = titleData[id] + 1

		playerData:set(playerName, "titles", titleData)

		unlockTitle(playerName, category, titleData[id])
		save = true
	end

	playerCache[playerName].titles[id] = titleData[id]

	return save
end

--[[ UI ]]--
ui.removeProfile = function(n)
	playerCache[n].profile.target = nil
	for i = 0, 7 do
		ui.removeTextArea(i, n)
	end
	for i = 1, #playerCache[n].profile do
		tfm.exec.removeImage(playerCache[n].profile[i])
	end
	playerCache[n].profile = { }
end
do
	local colors = { owner = "AB5BC2", map = "2ECF73", art = "FE7100", normal = "C1F8FB" }
	ui.profile = function(p, n)
		if playerCache[n].profile.target then
			ui.removeProfile(n)
		end

		playerCache[n].profile.target = p
		playerCache[n].profile[1] = tfm.exec.addImage("165e26f4172.png", ":0", 256, 41, n)
		ui.addTextArea(0, "<p align='center'><font size='" .. (#p > 17 and 14 or 18) .. "' color='#" .. colors[(p == module.owner and "owner" or mapEvaluators[p] and "map" or artist[p] and "art" or "normal")] .. "'>" .. (p:gsub("#", "<font size='10'><N2>#", 1)), n, 280, 65, 240, nil, 1, 1, 0, true)
		playerCache[n].profile[2] = tfm.exec.addImage("165f818ebff.png", ":1", 290, 108, n) -- 165df8ebe60.png
		ui.addTextArea(1, "<font size='16' color='#C1F8FB'>" .. translation.soon, n, 350, 126, 150, nil, 1, 1, 0, true)

		local playerLevel, total, remaining = xpToLvl(playerData:get(p, "xp"))
		local width = math.clamp(total * (210 / (total + remaining)), 1, 210)

		ui.addTextArea(2, "", n, 295, 300, 210, 10, 0x151C2A, 0x00CCFF, 1, true)
		ui.addTextArea(3, "", n, 295, 300, width, 10, 0x00CCFF, 0x00CCFF, 1, true)
		ui.addTextArea(4, "<font color='#00CCFF'><B>LVL " .. playerLevel, n, 290, 275, 220, nil, 1, 1, 0, true)
		ui.addTextArea(5, "<p align='right'><BL>" .. total .. " / " .. (total + remaining) .. " XP", n, 290, 275, 220, nil, 1, 1, 0, true)
		ui.addTextArea(6, (p == n and "<a href='event:titles'>" or "") .. "<p align='center'><font size='16' color='#C1F8FB'>«" .. translation.titles[playerCache[p].titles[1][1]][playerCache[p].titles[1][2]] .. "»\n", n, 295, 322, 210, nil, 1, 1, 0, true)

		local counter, x = 2, 0
		for _, badge in next, playerCache[p].badges do
			x = x + 45
			counter = counter + 1
			playerCache[n].profile[counter] = tfm.exec.addImage(badge, ":2", 248 + x, 240, n)
		end

		ui.addTextArea(7, "<font size='14' color='#C1F8FB'>" .. translation.profile[1] .. " : <BL>" .. playerData:get(p, "rounds") .. "</BL>\n" .. translation.profile[2] .. " : <BL>" .. playerData:get(p, "victories") .. (counter > 2 and ("</BL>\n<font size='7'>\n</font><p align='center'>" .. translation.profile[3]) or ""), n, 290, 170, 220, nil, 1, 1, 0, true)
	end
end

--[[ Events ]]--
-- NewPlayer
eventNewPlayer = function(n)
	playerCache[n] = {
		ready = false,
		profile = { },
		badges = { },
		titles = { { 1, 1 }, 0, 0, 0 },
		afkMaps = 0
	}

	system.loadPlayerData(n)
	insert(players.room, n)

	tfm.exec.lowerSyncDelay(n)

	tfm.exec.chatMessage("<J>" .. translation.welcome .. "\n\t<ROSE>Discord: https://discord.gg/quch83R", n)

	system.bindKeyboard(n, keys.P, true, true)
	for i = 0, 3 do
		-- Moves not to be AFK
		system.bindKeyboard(n, i, true, true)
	end

	ui.banner("15d60d944f5", 140, 135, n)
end

-- PlayerDataLoaded
eventPlayerDataLoaded = function(playerName, data)
	playerData:newPlayer(playerName, data)

	local playerBadges, counter = playerData:get(playerName, "badges"), 0
	if playerBadges > 0 then
		for i = 1, #badges do
			if bit32.band(badges[i][1], playerBadges) ~= 0 then
				counter = counter + 1
				playerCache[playerName].badges[counter] = badges[i][2]
			end
		end
	end

	local t = playerData:get(playerName, "titles")
	local category, id = string.match(t[1], "(%d)(%d+)")
	playerCache[playerName].titles[1] = { tonumber(category), tonumber(id) }
	playerCache[playerName].titles[4] = t[4]

	local save = false
	for i = 1, 2 do
		save = checkTitle(playerName, i) or save
	end

	if save then
		playerData:save(playerName)
	end

	playerCache[playerName].ready = true
end

-- NewGame
local xmlFunctions = {
	[1] = {
		attribute = "cn",
		func = function(value)
			local coord, axY = xml.getCoordinates(value)
			if type(coord) == "table" then
				cannon.x = {}
				cannon.y = {}

				for k, v in next, coord do
					cannon.x[#cannon.x + 1] = v.x
					cannon.y[#cannon.y + 1] = v.y
				end
			else
				if axY == 0 then
					cannon.x = coord
				else
					cannon.y = axY
				end
			end
		end
	},
	[2] = {
		attribute = "cheese",
		func = function()
			for n in next, tfm.get.room.playerList do
				tfm.exec.giveCheese(n)
			end
		end
	},
	[3] = {
		attribute = "meep",
		func = function()
			for n in next, tfm.get.room.playerList do
				tfm.exec.giveMeep(n)
			end
		end
	},
	[4] = {
		attribute = "quantity",
		func = function(value)
			value = tonumber(value) or 1
			cannon.mul = math.clamp(value, 1, 3)
		end
	},
	[5] = {
		attribute = "bh",
		func = function()
			bhAttribute = true
		end
	},
	[6] = {
		attribute = "mgoc",
		func = function(value)
			mgocAttribute = tonumber(value)
		end
	},
	[7] = {
		attribute = "style",
		func = function(cannons)
			cannons = string.split(cannons, "[^,]+", function(id)
				id = tonumber(id)
				if id then
					if id == 0 then
						return 17
					else
						if id > 0 and id < 12 then
							return 1700 + id
						end
					end
				end
				return nil
			end)

			if #cannons > 0 then
				cannonID = cannons
			end
		end
	},
	[8] = {
		attribute = "time",
		func = function(value)
			value = tonumber(value)
			if value then
				tfm.exec.setGameTime(math.clamp(value * 60, 60, 180))
			end
		end
	},
	[9] = {
		attribute = "size",
		func = function(value)
			value = tonumber(value)
			if value then
				for n in next, tfm.get.room.playerList do
					tfm.exec.changePlayerSize(n, value)
				end
			end
		end
	}
}

local currentTime, leftTime, loadingNextMap = 0, 125, 0
eventNewGame = function()
	loadingNextMap = 0
	currentTime, leftTime = 0, 125

	currentRound = currentRound + 1
	if currentRound > #maps then
		currentRound = 1
		maps = table.shuffle(maps)
	end

	players.alive = table.copy(players.room)
	players.currentRound = table.copy(players.room)

	for player, data in next, tfm.get.room.playerList do
		if playerCache[player] then
			playerCache[player].afkMaps = playerCache[player].afkMaps + 1
			if playerCache[player].afkMaps < 3 then
				if playerCache[player].ready then
					if canSave() then
						playerData:set(player, "rounds", playerData:get(player, "rounds") + 1)
						checkTitle(player, 1)
						playerData:save(player)
					end
				end
				if playerCache[player].profile.target then
					ui.profile(playerCache[player].profile.target, player)
				end
			end
		else
			tfm.exec.killPlayer(player)
		end
	end

	toSpawn, toDespawn = {}, {}
	announceWinner = true
	cannonID = {}

	wasReview = review

	cannon = {
		x = 0,
		y = 0,
		time = 2.5,
		speed = 20,
		mul = 1
	}

	tfm.exec.setGameTime(125)

	for n in next, tfm.get.room.playerList do
		tfm.exec.changePlayerSize(n, 1) -- it doesn't reset by i
	end

	local bhAttribute, mgocAttribute = false, false

	xml.attribFunc(((tfm.get.room.xmlMapInfo or {}).xml or ""), xmlFunctions)

	cannon.quantity = math.ceil(math.max(1, (players.currentRound._count - (players.currentRound._count % 15)) / 10) * cannon.mul + hardMode)

	mapSettingsReview = false
end

-- Loop
eventLoop = function()
	timer.loop()
	if loadingNextMap > 0 then
		loadingNextMap = loadingNextMap - .5
		if loadingNextMap <= 0 then
			tfm.exec.newGame(maps[currentRound])
			loadingNextMap = 3
		end
		return
	end
	if not mapSettingsReview and review then
		mapSettingsReview = true
		local text = tostring(tfm.get.room.currentMap) .. " : " .. (bhAttribute and "<VP>has" or "<R>no") .. " bh <BL>| " .. (mgocAttribute and "has" or "<VP>no") .. " mgoc" .. ((mgocAttribute and ((mgocAttribute < 0 and " <R>" or " <VP>") .. "(" .. tostring(mgocAttribute) .. ")") or "")) .. " <BL>| <J>x" .. cannon.mul
		for k in next, mapEvaluators do
			tfm.exec.chatMessage(text, k)
		end
	end
	currentTime, leftTime = currentTime + .5, leftTime - .5

	soloGame = players.currentRound._count == 1

	local p

	local save = canSave()
	if currentTime % 30 == 0 and save then
		for i = 1, players.alive._count do
			p = players.alive[i]
			if playerCache[p] and playerCache[p].ready then
				playerData:set(p, "xp", playerData:get(p, "xp") + module.xp_per_30_sec):save(p)
			end
		end
	end

	if currentTime <= 3 then return end

	if not review and (leftTime < 3 or (not soloGame and players.alive._count < 2) or players.alive._count == 0) then
		if not soloGame and announceWinner then
			announceWinner = false
			if players.alive._count > 0 and not wasReview then
				for i = 1, players.alive._count do
					p = players.alive[i]
					if save then
						playerData:set(p, "victories", playerData:get(p, "victories") + 1)
						checkTitle(p, 2)
						playerData:set(p, "xp", playerData:get(p, "xp") + module.xp_per_victory)
						playerData:save(p)
					end
					tfm.exec.respawnPlayer(p)
					tfm.exec.setPlayerScore(p, 5, true)
					tfm.exec.giveCheese(p)
					tfm.exec.playerVictory(p)
				end
				tfm.exec.chatMessage("<J>" .. table.concat(players.alive, "<G>, <J>") .. " <J>" .. translation.won)
			else
				tfm.exec.chatMessage("<J>" .. translation.nowinner)
			end
		end
		loadingNextMap = 2
	else
		if currentTime % cannon.time == 0 then
			for i = 1, cannon.quantity do
				newCannon()
			end
		end

		for k, v in next, table.copy(toSpawn) do
			if os.time() > v[1] then
				toDespawn[#toDespawn + 1] = { tfm.exec.addShamanObject(table.unpack(v, 2)), os.time() + 5000 }
				toSpawn[k] = nil
			end
		end

		for k, v in next, table.copy(toDespawn) do
			if os.time() > v[2] then
				tfm.exec.removeObject(v[1])
				toDespawn[k] = nil
			end
		end

		if currentTime % 20 == 0 then
			cannon.quantity = math.ceil(math.max(1, (players.currentRound._count - (players.currentRound._count % 15)) / 10) * cannon.mul + hardMode)
			cannon.speed = cannon.speed + 20
			cannon.time = math.max(.5, cannon.time - .5)
		end
	end
end

-- ChatCommand
eventChatCommand = function(n, c)
	local p = string.split(c, "%S+", string.lower)

	if p[1] == "p" or p[1] == "profile" then
		if p[2] then
			p[2] = string.nick(p[2])
			if tfm.get.room.playerList[p[2]] and playerCache[p[2]] and playerCache[p[2]].ready then
				ui.profile(p[2], n)
			end
		elseif playerCache[n] and playerCache[n].ready then
			ui.profile(n, n)
		end
	elseif p[1] == "title" then
		if p[2] then
			local category, id = string.match(p[2], "^(%d)(%d+)$")
			category, id = tonumber(category), tonumber(id)

			if category and id then
				if category > 0 and category < 4 and id > 0 then
					if playerCache[n].titles[category + 1] >= id then
						playerCache[n].titles[1] = { category, id }

						local t = playerData:get(n, "titles")
						t[1] = tonumber(category .. id)
						playerData:set(n, "titles", t):save(n)

						tfm.exec.chatMessage("<BL>" .. string.format(translation.usetitle, translation.titles[category][id]), n)
					end
				end
			end
		else
			tfm.exec.chatMessage(translation.titlemsg, n)
			for cat = 1, 3 do
				for id = 1, playerCache[n].titles[cat + 1] do
					tfm.exec.chatMessage("!title " .. cat .. id .. " -> «" .. translation.titles[cat][id] .. "»", n)
				end
			end
		end
	elseif p[1] == "speak" and n == module.owner then
		tfm.exec.chatMessage("<VP><B>[#cannonup] " .. table.concat(p, " ", 2) .. "</B>")
	else
		if mapEvaluators[n] then
			if p[1] == "review" then
				review = not review
				wasReview = true
				tfm.exec.chatMessage("<PT>REVIEW : " .. string.upper(tostring(review)))
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

			if not string.find(tfm.get.room.name, "^*?#cannonup%d*$") then
				if p[1] == "next" then
					tfm.exec.newGame(maps[currentRound])
				elseif p[1] == "again" then
					currentRound = currentRound - 1
					tfm.exec.newGame(tfm.get.room.currentMap)
				end
			end
		end
	end
end

-- Keyboard
eventKeyboard = function(player, k)
	if playerCache[player].afkMaps > 0 and not tfm.get.room.playerList[player].isDead then
		playerCache[player].afkMaps = 0
	end

	if k == keys.P and playerCache[player] and playerCache[player].ready then
		if playerCache[player].profile.target then
			ui.removeProfile(player)
		else
			ui.profile(player, player)
		end
	end
end

-- TextAreaCallback
eventTextAreaCallback = function(i, player, c)
	if c == "close" then
		for i = 1,2 do
			ui.removeTextArea(i, player)
		end
	elseif c == "titles" then
		eventChatCommand(player, "title")
	end
end

-- PlayerLeft
eventPlayerLeft = function(player)
	playerData:save(player)
	remove(players.alive, player)
	remove(players.room, player)
	remove(players.currentRound, player)
end

-- PlayerDied
eventPlayerDied = function(player)
	if review then
		tfm.exec.respawnPlayer(player)
	end
	remove(players.alive, player)
end

-- PlayerRespawn
eventPlayerRespawn = function(playerName)
	if not review then return end

	insert(players.alive, playerName)
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

maps = table.shuffle(maps)

tfm.exec.disableAutoShaman()
tfm.exec.disableAutoScore()
tfm.exec.disableAutoNewGame()
tfm.exec.disableAutoTimeLeft()
tfm.exec.disablePhysicalConsumables()

tfm.exec.setRoomMaxPlayers(25)
tfm.exec.setGameTime(5, false) -- Prevention

system.disableChatCommandDisplay(nil, true)

for playerName in next, tfm.get.room.playerList do
	eventNewPlayer(playerName)
end
tfm.exec.newGame(maps[currentRound])
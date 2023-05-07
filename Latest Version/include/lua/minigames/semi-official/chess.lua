string.split = function(value, pattern, f)
	local out = {}
	for v in string.gmatch(value, pattern) do
		out[#out + 1] = (not f and v or f(v))
	end
	return out
end
table.copy = function(list)
	local out = {}
	for k,v in next, list do
		out[k] = (type(v) == "table" and table.copy(v) or v)
	end
	return out
end

-- Board
local setBoard = function()
	return
	{
		{'♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'},
		{'♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'},
		{'', '', '', '', '', '', '', ''},
		{'', '', '', '', '', '', '', ''},
		{'', '', '', '', '', '', '', ''},
		{'', '', '', '', '', '', '', ''},
		{'♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'},
		{'♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'}
	}
end
local board = setBoard()
local colors = {
	background = 0x2F363F,
	whiteSquare = 0xFFCE9E,
	whitePiece = 'FFFFFF',
	blackSquare = 0xD18B47,
	blackPiece = '1',
	specialMove = 0xB300EF,
	emptyMove = 0x2ECF73,
	captureMove = 0xAF2A2A,
	lastMove = 0xFFCF5F,
	selectedPiece = '<PT>',
}
local pieces = {
	king = 1,
	queen = 2,
	rook = 3,
	bishop = 4,
	knight = 5,
	pawn = 6
}

-- Info
local playerInfo = function()
	return 
	{
		[1] = { name = "", pieces = 16, castling = {true, true}, lastMove = "" },
		[2] = { name = "", pieces = 16, castling = {true, true}, lastMove = "" },
	}
end
local players = playerInfo()
local moveTimer = 0
local canStart = false
local currentPlayer = 2
local currentPlayerColor = ""
local lastMove = {}

-- StringReference
local stringReference = {}
stringReference.emptySquare = "<textformat leftmargin='30' rightmargin='30' leading='30'>"
stringReference.HREF_select = "<a href='event:select_%s_%s_%s_%s'>"
stringReference.squareFormat = "<font size='25'><B>"

stringReference.select = stringReference.emptySquare .. stringReference.HREF_select .. "\n"
stringReference.piece = stringReference.squareFormat .. stringReference.HREF_select .. "%s"
stringReference.castling = stringReference.emptySquare .. "<a href='event:kingpass_%s_%s_%s'>\n"

-- System
local isWhitePiece = function(p)
	p = string.byte(p, 3, 3)
	return p > 147 and p < 154
end
local existSquare = function(row, column)
	return board[row] and board[row][column]
end
local isPieceSquare = function(row, column)
	return existSquare(row, column) and board[row][column] ~= ''
end
local pieceDifColor = function(p1, p2)
	return isWhitePiece(p1) ~= isWhitePiece(p2)
end
local pieceID = function(p)
	return (string.byte(p, 3, 3) - 148) % 6 + 1
end
local checkCapture = function(n, row, column, newRow, newColumn, boolCapture, boolEmpty)
	boolCapture = boolCapture == nil or boolCapture
	boolEmpty = boolEmpty == nil or boolEmpty

	if isPieceSquare(newRow, newColumn) then
		if boolCapture and pieceDifColor(board[row][column], board[newRow][newColumn]) then
			uiupdateSquare(newRow, newColumn, n, colors.captureMove, string.format(stringReference.piece, row, column, newRow, newColumn, board[newRow][newColumn]))
		end
		return true
	end
	if boolEmpty then
		uiupdateSquare(newRow, newColumn, n, colors.emptyMove, string.format(stringReference.select, row, column, newRow, newColumn))
	end
	return false
end

local border = function(text)
	ui.addTextArea(-4, "<font color='#1'>" .. text, nil, 5, 367, 792, nil, 1, 1, 0, true)
	ui.addTextArea(-5, "<PS>" .. text, nil, 5, 365, 790, nil, 1, 1, 0, true)
end
local changeTurn = function()
	currentPlayer = (currentPlayer == 1 and 2 or 1)
	currentPlayerColor = ({"White", "Black"})[currentPlayer]
	
	local text = "<B><p align='center'><font size='18'>" .. currentPlayerColor .. "'s turn!"
	border(text)
end
local restart = function()
	canStart = false

	uiclearColoredSquares()
	
	for k, v in next, players do
		tfm.exec.movePlayer(v.name, 400, 375)
	end
	
	board = setBoard()
	players = playerInfo()

	currentPlayer = 2
	for i = 3, 5 do
		ui.removeTextArea(-i)
	end
	
	for i = 1, 2 do
		ui.addTextArea(-i, "<font color='#" .. ({"White", "Black"})[i] .. "'><p align='center'><font size='20'>[Space]", nil, 5 + (i - 1) * 595, 180, 200, nil, 1, 1, 0, true)
	end
	
	uiboard()
end

-- UI
local coloredSquares = {}
uiclearColoredSquares = function()
	for k, v in next, table.copy(coloredSquares) do
		if v then
			ui.removeTextArea(k)
			coloredSquares[k] = nil
		end
	end
end

uiupdateSquare = function(row, column, n, color, href, notNeg)
	if existSquare(row, column) then
		local isNeg = false
		if not notNeg then
			isNeg = not not (color or href)
		end

		local squareText = href or board[row][column] == '' and '' or string.format("%s%s<a href='event:square_%s_%s'>%s", stringReference.squareFormat, "<font color='#" .. colors[(isWhitePiece(board[row][column]) and "white" or "black") .. "Piece"] .. "'>", row, column, board[row][column])
		
		ui.addTextArea((row..column) * (isNeg and -1 or 1), squareText, n, 252 + (column - 1) * 38, 50 + (row - 1) * 38, 30, 30, color or (((row + column) % 2 == 0) and colors.whiteSquare or colors.blackSquare), 1, 1, true)
		
		ui.setShamanName(string.format("-   <G>|   <S>%s x %s", players[1].pieces, players[2].pieces))
		if isNeg then
			coloredSquares[-(row..column)] = true
		end
	end
end

local uiupdateLastMove = function(...)
	if lastMove[1] and lastMove[2] then
		uiupdateSquare(lastMove[1], lastMove[2])
	end
	lastMove = {...}
end

uiboard = function(n)
	--[[
		[11:88] -> Squares
		[-88:-11] -> Effects
		[-10:0] -> Others
	]]
	ui.addTextArea(0, "", n, 247, 45, 306, 306, colors.background, colors.background, 1, true)
	for row = 1, 8 do
		for column = 1, 8 do
			uiupdateSquare(row, column, n)
		end
	end
end

-- Callbacks
eventTextAreaCallback = function(i, n, c)
	if players[currentPlayer].name == n and os.time() > moveTimer then
		moveTimer = os.time() + 250
	
		c = string.split(c, "[^_]+", function(value)
			return tonumber(value) or value
		end)
		
		local row, column = c[2], c[3]
		
		uiclearColoredSquares()
		if c[1] == "transform" then
			ui.removeTextArea(-3, n)
			board[row][column] = string.char(226, 153, (c[4] == 2 and c[5] + 6 or c[5]))
			
			uiupdateSquare(row, column, nil, colors.lastMove, nil, true) 
			
			changeTurn()
		elseif c[1] == "kingpass" then
			local initialSquare = (c[4] == "left" and -1 or 1)
			local finalSquare = column + (c[4] == "right" and 3 or -4)
			
			local iniTwo = column + (2 * initialSquare)
			local iniSig = column + (1 * initialSquare)
			
			board[row][iniTwo] = board[row][column]
			board[row][column] = ''
			
			board[row][iniSig] = board[row][finalSquare]
			board[row][finalSquare] = ''
			
			players[currentPlayer].castling = {false, false}
			players[currentPlayer].lastMove = ''
			
			uiupdateLastMove(row, iniTwo)
			
			uiupdateSquare(row, iniTwo, nil, colors.lastMove, nil, true)
			uiupdateSquare(row, column)
			uiupdateSquare(row, iniSig)
			uiupdateSquare(row, finalSquare)
			
			changeTurn()
		else
			local piece = pieceID(board[row][column])
		
			if c[1] == "square" then
				local whitePiece = isWhitePiece(board[row][column])
				if (currentPlayer == 1 and not whitePiece) or (currentPlayer == 2 and whitePiece) then
					tfm.exec.chatMessage("<S>[#Chess] You can move only the " .. currentPlayerColor .. " pieces!", n)
					return
				end

				-- Highlights the piece you've selected
				uiupdateSquare(row, column, n, nil, stringReference.squareFormat .. colors.selectedPiece .. board[row][column])
				
				local dir = whitePiece and -1 or 1
				if piece == pieces.pawn then
					-- In front, 1 or 2 squares
					for i = 1, ((row == 2 or row == 7) and 2 or 1) do
						local newRow = row + i * dir
						
						if isPieceSquare(newRow, column) then
							break
						end
						
						uiupdateSquare(newRow, column, n, ((newRow == 1 or newRow == 8) and colors.specialMove or colors.emptyMove), string.format(stringReference.select, row, column, newRow, column))
					end
					
					-- En passant
					if players[3 - currentPlayer].lastMove ~= "" then
						local grid = string.split(players[3 - currentPlayer].lastMove, "[^_]+", tonumber)
						if grid[1] and grid[2] then
							for i = -1, 1, 2 do
								if grid[1] == row and grid[2] + i == column then
									uiupdateSquare(grid[1] + dir, grid[2], n, colors.specialMove, string.format(stringReference.piece, row, column, grid[1], grid[2] .. "_" .. (grid[1] + dir), "\n"))
									break
								end
							end
						end
					end
				end
				if piece == pieces.rook or piece == pieces.queen or piece == pieces.king then
					local range = (piece == pieces.king and 1 or 8)
					
					-- Horizontal and Vertical
					local coord = {{-1, 0}, {0, -1}, {1, 0}, {0, 1}}
					for i = 1, 4 do
						for j = 1, range do
							local newRow = row + j * coord[i][1]
							local newColumn = column + j * coord[i][2]
							
							if checkCapture(n, row, column, newRow, newColumn) then
								break
							end
						end
					end
				end
				if piece == pieces.knight then
					-- L Shape
					local coord = {{-2, -1}, {-1, -2}, {-2, 1}, {-1, 2}, {1, -2}, {2, -1}, {1, 2}, {2, 1}}
					for i = 1, 8 do
						local newRow = row + coord[i][1]
						local newColumn = column + coord[i][2]
						
						checkCapture(n, row, column, newRow, newColumn)
					end
				end
				if piece == pieces.bishop or piece == pieces.queen or piece == pieces.king or piece == pieces.pawn then
					local isPawn = piece == pieces.pawn
					local range = ((piece == pieces.king or isPawn) and 1 or 8)
					
					-- Diagonal
					local coord = {{-1, -1}, {-1, 1}, {1, -1}, {1, 1}}
					for i = 1, 4 do
						for j = 1, range do
							local newRow = row + j * coord[i][1]
							local newColumn = column + j * coord[i][2]
							
							local check = checkCapture(n, row, column, newRow, newColumn, (not isPawn or coord[i][1] == dir), not isPawn)
							if check then
								break
							end
						end
					end
				end
				if piece == pieces.king then
					-- Castling
					local d = 1
					for i = 1, 2 do
						if players[currentPlayer].castling[i] and not isPieceSquare(row, column + d) and not isPieceSquare(row, column + (d * 2)) then
							if d > 0 or not isPieceSquare(row, column - 3) then
								uiupdateSquare(row, column + (d > 0 and 2 or -3), n, colors.specialMove, string.format(stringReference.castling, row, column, (d > 0 and "right" or "left")))
							end
						end
						d = -d
					end
				end
			elseif c[1] == "select" then
				local newRow, newColumn = c[4], c[5]
			
				uiupdateLastMove(c[6] or newRow, newColumn)
				
				-- Checks the attack
				local checkmate = false
				if isPieceSquare(row, column) and isPieceSquare(newRow, newColumn) and pieceDifColor(board[row][column], board[newRow][newColumn]) then
					players[3 - currentPlayer].pieces = players[3 - currentPlayer].pieces - 1
					checkmate = pieceID(board[newRow][newColumn]) == pieces.king
				end
				
				-- Updates the squares
				board[c[6] or newRow][newColumn] = board[row][column]
				if c[6] then
					board[newRow][newColumn] = ''
					uiupdateSquare(c[6], newColumn, nil, colors.lastMove, nil, true) 
				end
				uiupdateSquare(newRow, newColumn, nil, (not c[6] and colors.lastMove or nil), nil, true)
				
				board[row][column] = ''
				uiupdateSquare(row, column)
				
				if checkmate then
					tfm.exec.chatMessage("<S>[#Chess] " .. currentPlayerColor .. " pieces won!")
					tfm.exec.setPlayerScore(n, 10, true)
					restart()
					return
				end
				
				-- Sets the lastMove
				players[currentPlayer].lastMove = ((piece == pieces.pawn and math.abs(newRow - row) == 2) and (newRow .. "_" .. newColumn) or '')

				-- Pawn promotion
				if piece == pieces.pawn then
					if newRow == 1 or newRow == 8 then
						local text = "<textformat leading='40'><p align='center'><font size='25'>PAWN PROMOTION<font size='15'>\n<B>"
						for k, v in next, {{'<ROSE>Queen', 149}, {'<J>Rook', 150}, {'<PT>Bishop', 151}, {'<BV>Knight', 152}} do
							text = text .. string.format("<a href='event:transform_%s_%s_%s_%s'>%s\n", newRow, newColumn, currentPlayer, v[2], "<CH>" .. string.char(226, 153, v[2]) .. " " .. v[1] .. " <CH>" .. string.char(226, 153, v[2] + 6))
						end
						ui.addTextArea(-3, text, n, 247, 45, 306, 306, nil, nil, .9, true)
						border("<B><p align='center'><font size='18'>" .. currentPlayerColor .. " Pawn promotion!")
						return
					end
				-- Disable Castling
				elseif piece == pieces.king then
					players[currentPlayer].castling = {false, false}
				elseif piece == pieces.rook then
					if players[currentPlayer].castling[1] or players[currentPlayer].castling[2] then
						local pieceColumn = column == 1 and 1 or column == 8 and 2 or 0
						if pieceColumn > 0 then
							players[currentPlayer].castling[pieceColumn] = true
						end
					end
				end
				
				changeTurn()
			end
		end
	end
end

-- Loop
eventLoop = function()
	if not canStart then
		local totalPlayers = 0
		for i = 1, 2 do
			if players[i].name == "" then
				tfm.exec.addShamanObject(0, 40 + 720 * (i - 1), 200)
			else
				totalPlayers = totalPlayers + 1
			end
		end
		
		if totalPlayers == 2 then
			canStart = true
			changeTurn()
		end
	end
end

-- New Game
eventNewPlayer = function(n)
	uiboard(n)
	tfm.exec.respawnPlayer(n)
	system.bindKeyboard(n, 32, true, true)
	tfm.exec.chatMessage("<S>[#Chess] Welcome to the module! Choose an armchair and enjoy the game with a friend!\n\tYou, chess lord, report any bug to Bolodefchoco!", n)
end

-- Keyboard & Emote
eventKeyboard = function(n, k, d, x)
	for k, v in next, players do
		if v.name == n then
			return
		end
	end
	
	local id = x < 76 and 1 or x > 724 and 2 or 0
	if id > 0 then
		if players[id].name == "" then
			players[id].name = n
			local color = ({"White", "Black"})[id]
			ui.addTextArea(-id, "<font color='#" .. colors[string.lower(color) .. "Piece"] .. "' size='20'><p align='center'>" .. n .. "\n«" .. color .. "»", nil, 5 + (id - 1) * 595, 180, 200, nil, 1, 1, 0, true)
			tfm.exec.playEmote(n, 8)
			tfm.exec.chatMessage("<S>[#Chess] " .. n .. " is in the " .. color .. " team!")
		end
	end
end
eventEmotePlayed = function(n, t)
	if t == 8 then
		eventKeyboard(n, 32, nil, tfm.get.room.playerList[n].x)
	end
end

-- Player left
eventPlayerLeft = function(n)
	for i = 1, 2 do
		if players[i].name == n then
			tfm.exec.chatMessage("<S>[#Chess] " .. n .. " left the game :(")
			restart()
			break
		end
	end
end

-- Respawn
eventPlayerDied = tfm.exec.respawnPlayer

-- Init
for k, v in next, {"AutoShaman", "AfkDeath", "AutoNewGame", "AutoScore"} do
	tfm.exec["disable" .. v]()
end

tfm.exec.newGame(1995980)
restart()
table.foreach(tfm.get.room.playerList, eventNewPlayer)
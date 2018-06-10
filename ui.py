from tkinter import *

class QuangoUI(object):
	
	size = 50
	currentPlayer = 0;
	colours = ["purple", "yellow", "blue", "orange", "green"]
	players = ["black", "white"]
	gameOver = False
	simple_board_rows = [
	[0,0,3,1,0,0],
	[0,3,2,4,1,0],
	[3,2,2,4,4,1],
	[1,4,4,2,2,3],
	[0,1,4,2,3,0],
	[0,0,1,3,0,0]
	]
	simple_board_state = [
	[-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1],
	[-1,-1,-1,-1,-1,-1],
	]

	def __init__(self):
		super(QuangoUI, self).__init__()
		self.app = Tk()
		self.app.title("Quango")
		self.app.bind("<r>", self.reset)
		self.initBoard()

	def getPosition(self, x, y):
		if x < 0 or y < 0 or x > self.size * len(self.simple_board_rows) or y > self.size * len(self.simple_board_rows):
			print("Invalid position")
			return
		xPos = (x - x % self.size) / self.size
		yPos = (y - y % self.size) / self.size
		return (xPos, yPos)

	def klicked(self, event):
		if self.gameOver:
			return
		pos = self.getPosition(event.x, event.y)
		#print("clicked at", event.x, event.y, pos)
		if pos != None:
			self.placeToken(int(pos[0]), int(pos[1]))
			self.checkGameOver()

	def reset(self, event):
		print("reseting game")
		self.gameOver = False
		self.board.delete("all")
		self.board.destroy()
		self.initBoard()
		for y in range(0, len(self.simple_board_state)):
			for x in range(0, len(self.simple_board_state)):
				self.simple_board_state[y][x] = -1

	def placeToken(self, x, y):
		if self.simple_board_state[y][x] == -1:
			self.simple_board_state[y][x] = self.currentPlayer
			xPos = x * self.size
			yPos = y * self.size 
			oval = self.board.create_oval(xPos, yPos, xPos + self.size, yPos + self.size, fill=self.nextPlayer())
		else:
			#print("Field occupied", x, y)
			pass
		return    	

	def nextPlayer(self):
		currentPlayerColour = self.players[self.currentPlayer]
		self.currentPlayer += 1
		if self.currentPlayer > len(self.players) - 1:
			self.currentPlayer = 0
		return currentPlayerColour

	def checkGameOver(self):
		if not self.gameOver:
			self.checkGroups()
		if not self.gameOver:
			self.checkSquares()
		if not self.gameOver:
			self.checkLine()

	def checkGroups(self):
		grop_rows = [
		(0,0,1),
		(0,1,2),
		(1,2,2)
		]
		
		offsets = [(0,0),(3,0),(3,3),(0,3)]
		
		for offsetId in range(0,4):
			for i in range(0,3):
				if self.checkGroup(grop_rows, i, 3, offsets[offsetId]):
					self.gameOver = True
					return
			#rotate check clockwise
			grop_rows = list(zip(*grop_rows[::-1]))

	def checkGroup(self, grop_rows, groupid, target, offset):
		player = -1
		groupElements = []
		#print("check",groupid)
		for y in range(0, len(grop_rows)):
			for x in range(0, len(grop_rows)):
				#print("cell",x+offset[0],y+offset[1])
				if grop_rows[y][x] == groupid:
					if self.simple_board_state[y + offset[1]][x + offset[0]] == -1:
						#print("unsuccessful", groupid, player, x+offset[0],y+offset[1])
						return False
					elif player == -1:
						player = self.simple_board_state[y + offset[1]][x + offset[0]]
					elif self.simple_board_state[y + offset[1]][x + offset[0]] != player:
						#print("failed", groupid, self.players[player], x+offset[0],y+offset[1])
						return False
					groupElements.append((x+offset[0],y+offset[1]))
					#print("occupied", groupid, self.players[player], x+offset[0],y+offset[1])
		self.printX(*groupElements)
		print("player", self.players[player], "won")
		return True

	def checkSquares(self):
		for y in range(0, len(self.simple_board_state) - 1):
			for x in range(0, len(self.simple_board_state) - 1):
				if (self.simple_board_state[y][x] != -1 and
						self.simple_board_state[y][x] == self.simple_board_state[y][x + 1] and 
						self.simple_board_state[y+1][x] == self.simple_board_state[y+1][x + 1] and
						self.simple_board_state[y][x] == self.simple_board_state[y+1][x + 1]):
					self.printX((x,y),(x,y+1),(x+1,y),(x+1,y+1))
					print("player", self.simple_board_state[y][x], "won")
					self.gameOver = True
					return
					
	def checkLine(self):
		#Check horizontal
		for y in range(0, len(self.simple_board_state)):
			for x in range(0, len(self.simple_board_state) - 4):
				if self.checkEqual(self.simple_board_state[y][x:x+5]):
					self.printX((x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y))
					print("player", self.simple_board_state[y][x], "won")
					self.gameOver = True
					return
		#Check vertical, rotate board state counter clockwise
		simple_board_state_rotated = list(zip(*self.simple_board_state[::1]))
		for y in range(0, len(self.simple_board_state)):
			for x in range(0, len(self.simple_board_state) - 4):
				if self.checkEqual(simple_board_state_rotated[y][x:x+5]):
					self.printX((y,x),(y,x+1),(y,x+2),(y,x+3),(y,x+4))
					print("player", simple_board_state_rotated[y][x], "won")
					self.gameOver = True
					return
		#Check diagonal
		self.checkDiagonal((0,0), 1, 1)
		self.checkDiagonal((1,0), 1, 1)
		self.checkDiagonal((1,1), 1, 1)
		self.checkDiagonal((0,1), 1, 1)
		self.checkDiagonal((4,0), -1, 1)
		self.checkDiagonal((5,0), -1, 1)
		self.checkDiagonal((5,1), -1, 1)
		self.checkDiagonal((4,1), -1, 1)

	def checkDiagonal(self, posStart, xDirection, yDirection):	
		first = self.simple_board_state[posStart[1]][posStart[0]]
		pos = posStart
		groupElements = []
		for x in range(0,5):
			if self.simple_board_state[pos[1]][pos[0]] == -1 or self.simple_board_state[pos[1]][pos[0]] != first:
				return False
			#print("occupied", posStart, self.players[self.simple_board_state[pos[1]][pos[0]]], (pos))
			groupElements.append(pos)
			pos = (pos[0] + xDirection, pos[1] + yDirection)
		self.printX(*groupElements)
		print("player", self.simple_board_state[posStart[1]][posStart[0]], "won")
		self.gameOver = True

	def checkEqual(self, test):
		first = test[0]
		for x in test:
			if x == -1 or x != first:
				return False
		return True

	def printX(self, *cells):
		for cell in cells:
			xPos = cell[0] * self.size + 10
			yPos = cell[1] * self.size + 10
			size = self.size - 20
			self.board.create_line(xPos, yPos, xPos + size, yPos + size, fill="red", width=2)
			self.board.create_line(xPos + size, yPos, xPos, yPos + size, fill="red", width=2)

	def initBoard(self):
		self.board = Canvas(self.app, width=self.size*len(self.simple_board_rows), height=self.size*len(self.simple_board_rows))
		self.board.pack()
		self.board.bind("<Button-1>", self.klicked)
		x = 0
		y = 0
		for simple_board_row in self.simple_board_rows:
			for cell in simple_board_row:
				xPos = x * self.size
				yPos = y * self.size
				#print(xPos, yPos, xPos + self.size, yPos + self.size, self.colours[cell])
				self.board.create_rectangle(xPos, yPos, xPos + self.size, yPos + self.size, fill=self.colours[cell])
				x += 1
			x = 0
			y += 1

def main():
	QuangoUI()
	mainloop()

if __name__ == "__main__":
	main()
	
#app.after(1000, lambda: app.destroy()) # Destroy the widget after 3 seconds


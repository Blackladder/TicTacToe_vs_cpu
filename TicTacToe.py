import numpy
import random
import time

class Player(object):
	def __init__(self, name):
		self.name = name
		self.tiles = numpy.full((3,3),False)

class Game(object):
	def __init__(self):
		self.init()
		random.seed(time.time())
		self.turn = 0
		self.main_while() #start

	def init(self):
		self.user = Player("User")
		self.cpu = Player("CPU")
		self.game = Player("N/A")
		self.turn = int(0)

	def main_while(self):
		while(True):#main:while
			self.init()
			print("User, you are O, CPU is X, and you go first.")
			while(True):#game_while
				self.player_turn()
				self.print_board()
				if (self.get_win(self.user)):
					print("Player won on turn ",self.turn+1, "!", "something went wrong")
					time.sleep(0.5)
					break
				if(self.turn == 4):
					print("Game over, it's a draw")
					break
				self.cpu_turn()
				self.print_board()
				if (self.get_win(self.cpu)):
					print("CPU won on turn", self.turn+1, "!")
					time.sleep(0.5)
					break
				self.turn += 1
			put = input("Play again? y/n\t")
			if(put.lower()=="n"):
				print("Ok, bye! Have a great time!")
				break
			elif(put.lower()=="y"):
				print("ok, here we go again")
			else:
				print("I'll take the silence as a yes, here we go again. Press \"Ctrl+C\" to cancel")

	#numpy array[x:y] = array[x, x+1, x+2, ... , y-2, y-1] , does not include array[y], like the MATLAB syntax

	def get_win(self, p): #p = Player
		if(p.tiles[1,1]): #Check if player.middle, if player.middle=False, then R2, C2, D1, D2 are false
			if(p.tiles[1, 0:3].all()): #check R2
				return True
			if(p.tiles[0:3, 1].all()): #check C2
				return True
			if(p.tiles[0,0]&p.tiles[1,1]&p.tiles[2,2]): #check D1
				return True
			if(p.tiles[0,2]&p.tiles[1,1]&p.tiles[2,0]): #check D2
				return True
		if(p.tiles[0, 0:3].all()): #check R1
			return True
		if(p.tiles[2, 0:3].all()): #check R3
			return True
		if(p.tiles[0:3, 0].all()): #check C1
			return True
		if(p.tiles[0:3, 2].all()): #check C3
			return True

	def player_turn(self):
		invalid = True
		while(invalid):
			try:
				put = int(input("Input which tile you would like to claim. (as a single number, use numpad for reference)"))
				r = int((put-1)/3)
				c = (put-1)%3
				if(~self.game.tiles[r,c]):
					self.game.tiles[r,c] = True
					self.user.tiles[r,c] = True
					invalid = False
				else:
					print("Invalid entry, tile already claimed, try again")
			except ValueError:
				print("ValueError, please input a number, and a number only, try again")
			except IndexError:
				print("IndexError, number has to be in the range [1,9], try again")
			except:
				print("\nother error, assuming Ctrl+C, exiting")
				exit()

	def cpu_turn(self):
		moved = False
		if(not self.game.tiles[1,1]):
			self.game.tiles[1,1] = True
			self.cpu.tiles[1,1] = True
			moved = True
		if(not moved):
			var = self.check_win_pot(self.cpu)
			r = var[0]
			c = var[1]
			if((r+c)!=-2):
				self.game.tiles[r,c] = True
				self.cpu.tiles[r,c] = True
				moved = True
		if(not moved):
			var = self.check_win_pot(self.user)
			r = var[0]
			c = var[1]
			if((r+c)!=-2):
				self.game.tiles[r,c] = True
				self.cpu.tiles[r,c] = True
				moved = True
		if(not moved):
			var = self.rand_corner()
			r = var[0]
			c = var[1]
			self.game.tiles[r,c] = True
			self.cpu.tiles[r,c] = True

	def print_board(self):
		hline = (' ___' *  3 )
		row1 = ""
		row2 = ""
		row3 = ""
		for i in range(0,3):
			row1 += "| " + self.tile_owner(0,i)
			row2 += "| " + self.tile_owner(1,i)
			row3 += "| " + self.tile_owner(2,i)
		row1 += "|"
		row2 += "|"
		row3 += "|"
		print('\n'.join((hline, row3, hline, row2, hline, row1, hline, ))) #swap row3 and row1 to flip reverse board vertically

	def tile_owner(self, r, c):
		if(~self.game.tiles[r,c]):
			return "  "
		elif(self.user.tiles[r,c]):
			return "O "
		elif(self.cpu.tiles[r,c]):
			return "X "

	def check_win_pot(self,p): #returns 
		if(p.tiles[1,1]): #Check if player.middle, if player.middle=False, then R2, C2, D1, D2 are false
			if(self.get_win_pot(p,[4,5,6])): #check R2
				return self.get_winning_move(p,[4,5,6])
			if(self.get_win_pot(p,[2,5,8])): #check C2
				return self.get_winning_move(p,[2,5,8])
			if(self.get_win_pot(p,[1,5,9])): #check D1
				return self.get_winning_move(p,[1,5,9])
			if(self.get_win_pot(p,[3,5,7])): #check D2
				return self.get_winning_move(p,[3,5,7])
		if(self.get_win_pot(p,[1,2,3])): #check R1
			return self.get_winning_move(p,[1,2,3])
		if(self.get_win_pot(p,[7,8,9])): #check R3
			return self.get_winning_move(p,[7,8,9])
		if(self.get_win_pot(p,[1,4,7])): #check C1
			return self.get_winning_move(p,[1,4,7])
		if(self.get_win_pot(p,[3,6,9])): #check C3
			return self.get_winning_move(p,[3,6,9])
		else:
			return [-1,-1]

	def get_win_pot(self,p,tiles):
		p_tiles = []
		game_tiles = []
		for put in tiles:
			r = int((put-1)/3)
			c = (put-1)%3
			p_tiles.append(p.tiles[r,c])
			game_tiles.append(self.game.tiles[r,c])
		game_tiles = numpy.logical_not(game_tiles)
		score=numpy.sum(p_tiles)+0.5*numpy.sum(game_tiles)
		return (score==2.5)

	def get_winning_move(self,p,tiles):
		for put in tiles:
			r = int((put-1)/3)
			c = (put-1)%3
			if(self.game.tiles[r,c]==False):
				return [r,c]

	def rand_corner(self):
		corners = [1,3,7,9]
		corners = random.sample(corners,4) #shuffles, had problems with random.shuffle
		for put in corners:
			r = int((put-1)/3)
			c = (put-1)%3
			if(self.game.tiles[r,c]==False):
				return [r,c]
		noncorners = [2,4,5,6,8]
		noncorners = random.sample(noncorners,5) #shuffles, had problems with random.shuffle
		for put in noncorners:
			r = int((put-1)/3)
			c = (put-1)%3
			if(self.game.tiles[r,c]==False):
				return [r,c]

game = Game()
print("Program finished")
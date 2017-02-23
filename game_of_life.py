import curses
import time
import random
import signal
import sys

class Grid:
	# An m x n grid of cells that can be 
	# alive - True , or
	# dead  - False

	def __init__(self,m, n, input_file = None):
		self.m = m
		self.n = n
		self.grid = None

		if not input_file:
			# If we have no input file,
			# Randomize the grid
			self.grid = [[random.choice([True,False]) for i in range(0,m)] 
										for i in range (0,n)]
		else:
			self.load_from_file(input_file)

	def load_from_file(self, path):
		# TODO Complete this
		with open(path) as input_file:
			lines = input_file.readlines()


	def get_alive_neighbors(self, x , y):
		# Returns number of neighbors of (x,y) 
		# that are alive

		neighbors = []

		if x - 1 >= 0 and y - 1 >= 0:

			neighbors.append(self.grid[y - 1][x - 1])
		if x - 1 >= 0:
			neighbors.append(self.grid[y][x - 1])
		if y - 1 >= 0:
			neighbors.append(self.grid[y - 1][x])
		if x + 1 < self.m and y + 1 < self.n:
			neighbors.append(self.grid[y + 1][x + 1])
		if x + 1 < self.m:
			neighbors.append(self.grid[y][x + 1])
		if y + 1 < self.n:
			neighbors.append(self.grid[y + 1][x])
		if x + 1 < self.m and y - 1 >= 0:
			neighbors.append(self.grid[y - 1][x + 1])
		if x - 1 >= 0 and y + 1 < self.n:
			neighbors.append(self.grid[y + 1][x - 1])

		return sum(neighbors)

	def updateGrid(self):
		# Updates the grid according to the rules
		# of Conway's Game of Life to the next state

		newgrid = [[False for i in range(0,self.m)] for i in range (0,self.n)]

		# Loop through each cell
		for y in range(0, self.n):
			for x in range(0, self.m):

				# Get number of alive neighbors for current cell
				num_neighbors = self.get_alive_neighbors(x,y)
				
				if self.grid[y][x]: 
					# The cell is alive

					# If the cell has < 2 or > 3 neighbors,
					# We do nothing (Cell is set to False)

					if num_neighbors == 2 or num_neighbors == 3:
						# For 2 or 3 neighbors, the cell gets to stay alive
						newgrid[y][x] = True
				else:
					# The cell is dead

					if num_neighbors == 3:
						# If the dead cell has 3 alive neighbors
						# A cell is born!
						newgrid[y][x] = True

		# Update the grid variable
		self.grid = newgrid

if __name__ == "__main__":

	# Set a signal handler for SIGINT to capture Ctrl-C
	def signal_handler(signal, frame):
		# Close up ncurses
		curses.endwin()
		# Exit the program
		sys.exit(0)

	# Set the handler function for SIGINT
	signal.signal(signal.SIGINT, signal_handler)

	input_file = None

	# Read command line arguments
	if len(sys.argv) < 3:
		print("Usage: python life.py ROWS COLUMNS [INPUT_FILE]")
	else:
		rows = int(sys.argv[1])
		columns = int(sys.argv[2])
		if len(sys.argv) > 3:
			input_file = sys.argv[3]

	# Initialize the grid
	life_grid = Grid(rows,columns)

	# Initialize ncurses
	screen = curses.initscr()
	screen.clear()
	# Add a border
	screen.border(0)
	# Heading
	screen.addstr(0, 0, "The Game Of Life", curses.A_BOLD)
	screen.addstr(2, 2, "Press Ctrl-C to exit", curses.A_UNDERLINE)


	# Loop until keyboard interrupt
	while True:
		for i in range(0, life_grid.n):
			display_line = " ".join('.' if j == False else "\u25A0" for j in life_grid.grid[i])
			
			try:
				# Print each row on the screen
				screen.addstr(i + 4,4, display_line)
			except curses.error as e:
				# We can end up with this exception if we don't
				# have enough vertical area to draw our lines

				print("ncurses Error. Grid possibly too large for Terminal size. Try resizing.")
				curses.endwin()
				sys.exit(0)

		# Draw the screen
		screen.refresh()
		
		# Don't move ahead so fast that we can't see anything
		time.sleep(0.1)  

		# Update the grid to the next grid state
		life_grid.updateGrid()



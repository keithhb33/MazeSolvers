from copy import deepcopy
import cv2
#Create 2d maze array

#Identify maze pixel dimensions (10x10 pixel maze)
rows = 6
columns = 4

#Create 2D maze array
maze = [[0 for y in range(columns)] for x in range(rows)]

#Read maze .png
img = cv2.imread("mazes/maze3.png")

#Hash white and black RGB codes to 'w' or 'b'
colors = {'[255 255 255]': 0, '[0 0 0]': 1}

#Identify each pixel in the maze by its color
for x in range(rows):
    for y in range(columns):
        maze[x][y] = colors[str((img[x][y]))]

for i in maze:
	print(i)

path = deepcopy(maze)

#label start and end of the maze
start = (0,0)
end = (3,5)

moves = []
found = False

def move(curX, curY):
	global maze, path, found
	if found:
		return False
	try:
		if path[curY][curX] == '+' or curY*curX < 0:
			return False
	except IndexError:
	    return False
	if (curX, curY) == start:
		path[curY][curX] = 'S'
	elif (curX, curY) == end:
		path[curY][curX] = 'E'
	else:
		path[curY][curX] = '+'

	if maze[curY][curX] == 1:
		return False
	elif (curX, curY) == end:
		found = True
		return True
	elif move(curX - 1, curY):
		moves.append('left')
		return True
	elif move(curX, curY - 1):
		moves.append('up')
		return True
	elif move(curX + 1, curY):
		moves.append('right')
		return True
	elif move(curX, curY + 1):
		moves.append('down')
		return True

def main():
	move(start[0], start[1])
	print('')
	print('moves: ', list(reversed(moves)))

if __name__ == '__main__':
	main()
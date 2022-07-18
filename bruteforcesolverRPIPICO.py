from machine import Pin,UART
from copy import deepcopy
from pico_car import pico_car
import time

maze = [
        [0,    0,    1,    1],
        [1,    0,    0,    0],
        [1,    0,    1,    1],
        [1,    0,    0,    1],
        [1,    1,    0,    1],
        [1,    1,    0,    1],
       ]

path = deepcopy(maze)

start = (0,0)
end = (2,5)

moves = []
steps = 0
found = False

Motor = pico_car()

uart = UART(0, 9600, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
led = machine.Pin(25, machine.Pin.OUT)

while True:
    if uart.any():
        data = uart.readline()
        print(data[0])
        
        if data == b'1':
            def moveCar(moves, steps):
                runtime = 2 #seconds
                rotate_pause = 2.4      #seconds
                speed = 140
                rotate_speed = 220
                
                right_counter = 0 
                left_counter = 0
                
                for i in range(len(moves)):
                    print("Moving " + str(moves[i]))
                    
                    if moves[i] == "right":
                        Motor.Car_Right(rotate_speed, rotate_speed)
                        time.sleep(rotate_pause)
                        
                        Motor.Car_Right(0, 0)
                        time.sleep(0.5)
                        
                        Motor.Car_Run(speed, speed)
                        time.sleep(runtime)
                        Motor.Car_Left(rotate_speed, rotate_speed)
                        time.sleep(rotate_pause)
                        
                        right_counter += 1
                        continue
                    
                    elif moves[i] == "left":
                        Motor.Car_Left(rotate_speed, rotate_speed)
                        time.sleep(rotate_pause)
                        Motor.Car_Run(speed, speed)
                        time.sleep(runtime)
                        Motor.Car_Right(rotate_speed, rotate_speed)
                        time.sleep(rotate_pause)
                        
                        left_counter += 1
                        continue
                    
                    elif moves[i] == "down":
                        Motor.Car_Back(speed, speed)
                        time.sleep(runtime)
                        Motor.Car_Stop()
                        continue
                    
                    else:
                        Motor.Car_Run(speed, speed)
                        time.sleep(runtime)
                        Motor.Car_Stop()
                    time.sleep(2)

            def move(curX, curY):
                global steps, maze, path, found
                if found == True:
                    return False
                try:
                    if (path[curY][curX] == '+' or curY*curX < 0):
                        return False
                except IndexError:
                    return False
                markMaze(curX, curY)
                steps = steps + 1

                if maze[curY][curX] == 1:
                    return False
                elif (curX, curY) == end:
                    found = True
                    return True
                elif (move(curX-1, curY)):
                    moves.append('left')
                    return True
                elif (move(curX, curY-1)):
                    moves.append('up')
                    return True
                elif (move(curX+1, curY)):
                    moves.append('right')
                    return True
                elif (move(curX, curY+1)):
                    moves.append('down')
                    return True

            def markMaze(curX, curY):
                print('X:', curX, ' Y:', curY)
                if (curX, curY) == start:
                    path[curY][curX] = 'S'
                elif (curX, curY) == end:
                    path[curY][curX] = 'E'
                else:
                    path[curY][curX] = '+'
                for x in path:
                    print ('\n', x)

            def main():
                move(start[0], start[1])
                print ('')
                print ('moves:' + str(list(reversed(moves))))
                print ('steps: ' + str(steps))
                moveCar((list(reversed(moves))), steps)

            if __name__ == '__main__':
                main()
        elif data== b'2':
            print('program paused')

        



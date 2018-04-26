“””” 
RaspberrySnake v0.1
Author: DoxPL
Check my Android apps:
https://play.google.com/store/apps/developer?id=DoxPL+Software
“”” 
from mcpi.minecraft import Minecraft
import random
import time
last_move = [1, 0]
def createTable():
    for rows in range(0, row_num):
        for cols in range(0, col_num):
            if cols == 0 or cols == col_num-1 or rows == 0 or rows == row_num-1:
                mc.setBlock(x+cols, y+rows, z, 49)
            else:
                mc.setBlock(x+cols, y+rows, z, 35, 0)

def createControls(player_x, player_y, player_z):
    global control_pos
    control_pos = (int)(player_x - 2)
    for i in range(-2, 2):
        mc.setBlock(player_x + i, player_y - 2, player_z, 20)
        mc.setBlock(player_x + i, player_y - 3, player_z-3, 20)
    mc.player.setPos(player_x, player_y, player_z-3)

def setPlayerPosition(_x, _y, _z):
    mc.player.setPos(_x, _y, _z - 15)

def setTail(snake):
    mc.setBlock(snake[0][0], snake[0][1], z, 35, 0)
    snake.pop(0)

def move():
    choice = 0
    event = mc.events.pollBlockHits()
    for e in event:
        choice = e.pos.x

    if choice == control_pos+1 and last_move[0] != -1:
        return [1, 0]
    if choice == control_pos and last_move[0] != 1:
        return [-1, 0]
    if choice == control_pos+3 and last_move[1] != -1:
        return [0, 1]
    if choice == control_pos+2 and last_move[1] != 1:
        return [0, -1]
    return last_move

def drawSnake(snake):
    for i in range(len(snake)):
        mc.setBlock(snake[i][0], snake[i][1], z, 22)

def setFood():
    mc.setBlock(x+random.randint(2, col_num-2), y+random.randint(2, row_num-2), z, 41)

def checkCollision(_x, _y, _z):
    tmp = mc.getBlock(_x, _y, _z)
    if tmp == 35 or tmp == 41:
        return False
    else:
        return True

mc = Minecraft.create()
x,y,z = mc.player.getPos()
x = x + 20
y = y + 5
row_num = 20 #wysokoœæ tablicy
col_num = 25 #szerokoœæ tablicy
createTable()
#ustawianie pozycji na œrodku planszy
pos_x = x + col_num/2
pos_y = y + row_num/2
mc.player.setPos(pos_x, pos_y - 4, z - 15)
createControls(pos_x, pos_y - 4, z - 15)
snake = []
snake.append([pos_x-2, pos_y])
snake.append([pos_x-1, pos_y])
snake.append([pos_x, pos_y])
mc.setBlock(pos_x, pos_y, z, 35, 3)
setFood()
last_time = int(round(time.time() * 1000))
interval = 700
score = 0
timeToStart = 5
mc.postToChat("RaspberrySnake by Dox")
mc.postToChat("Game will start in " + str(timeToStart) + " seconds")
time.sleep(timeToStart)
while True:
    new_time = int(round(time.time() * 1000))
    if new_time - last_time >= interval:
        last_time = new_time
        shift_x, shift_y = move()
        last_move = [shift_x, shift_y]
        pos_x = pos_x + shift_x
        pos_y = pos_y + shift_y
        if checkCollision(pos_x, pos_y, z):
            mc.postToChat("Game over, score: " + str(score))
            break
        snake.append([pos_x, pos_y])
        act_block = mc.getBlock(snake[-1][0], snake[-1][1], z)
        if act_block != 41:
            setTail(snake)
        else:
            setFood()
            score = score + 1
        drawSnake(snake)

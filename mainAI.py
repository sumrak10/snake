import pygame
import sys
import random
import numpy as np

BLACK    =   (0, 0, 0)
WHITE    =   (255, 255, 255)
ORANGE   =   (255, 150, 100)
BLUE     =   (0, 70, 225)
RED      =   (255, 10, 10)
GREEN    =   (10, 255, 10)

W = 300
H = 300
cell_w = 10
meals_num = 1

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Life')

def main():
    X = np.array([  [0,0,0,
                      0,0,0,
                      0,0,0],
                    [1,0,0,
                      1,0,0,
                      1,0,0],
                    [0,0,0,
                      0,0,0,
                      1,1,1],
                    [0,0,1,
                      0,0,1,
                      0,0,1],
                    [1,1,1,
                      0,0,0,
                      0,0,0],
                    [1,0,0,
                      1,0,0,
                      1,1,1],
                    [1,1,1,
                      1,0,0,
                      1,0,0],
                    [1,1,1,
                      0,0,1,
                      0,0,1],
                    [0,0,1,
                      0,0,1,
                      1,1,1] ])
    y = np.array([[1,1,1,1],
                  [1,0,1,1],
                  [1,1,0,1],
                  [1,1,1,0],
                  [0,1,1,1],
                  [1,0,0,1],
                  [0,0,1,1],
                  [0,1,1,0],
                  [1,1,0,0]])

    np.random.seed(1)
    syn0 = 2*np.random.random((9,20)) - 1
    syn1 = 2*np.random.random((20,4)) - 1
    for j in range(6000):
        l0 = X
        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))
        l2_error = y - l2
        l2_delta = l2_error*nonlin(l2,deriv=True)
        l1_error = l2_delta.dot(syn1.T)
        l1_delta = l1_error * nonlin(l1,deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)
    
    

    FPC = 1
    game = True
    r = 3
    x = (W//cell_w)//2-1
    y = (H//cell_w)//4-1
    coords = [[x,y-4], [x,y-3], [x,y-2], [x,y-1], [x,y]]
    pole =[]
    pole_backup = []
    px = []
    py = []
    for i in range(W//cell_w):
        px.append(1)
        if (i == 0) or (i == (H//cell_w-1)):
            py.append(1)
        else:
            py.append(0)
    for i in range(H//cell_w):
        if (i == 0) or (i == (W//cell_w-1)):
            pole.append(px)
        else:
            pole.append(py)
    pole_backup = pole
    coords_pole = [pole[x-1][y-1],pole[x][y-1],pole[x+1][y-1],
                   pole[x-1][y],pole[x][y],pole[x+1][y],
                   pole[x-1][y+1],pole[x][y+1],pole[x+1][y+1]]
    snake_w = 5
    meals = []
    for i in range(meals_num):
        meals.append([random.randint(1,W//cell_w-2), random.randint(1,H//cell_w-2)])
    motion = 'down'
    LEFT  = 'left'
    RIGHT = 'right'
    UP    = 'up'
    DOWN  = 'down'
    while game:   
        clock.tick(FPC)
        pole = pole_backup
        coords_pole = [pole[x-1][y-1],pole[x][y-1],pole[x+1][y-1],pole[x-1][y],pole[x][y],pole[x+1][y],pole[x-1][y+1],pole[x][y+1],pole[x+1][y+1]]
        l0 =  np.array([ coords_pole ] )
        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))
        mot = l2.tolist()
        mot = mot[0]

        # for i in range(len(coords)):
        #     cx = coords[i][0]
        #     cy = coords[i][1]
        #     pole[cx][cy] = 1
        #     print(cx,cy)
        for i in range(len(pole)):
            print(pole[i])
        
        # if (round(mot[0])) and not(motion == DOWN):
        #     motion = UP
        # elif (round(mot[1])) and not(motion == RIGHT):
        #     motion = LEFT
        # elif (round(mot[2])) and not(motion == UP):
        #     motion = DOWN
        # elif (round(mot[3])) and not(motion == LEFT):
        #     motion = RIGHT

        for i in pygame.event.get():
            if i.type == pygame.QUIT: exit()
            elif i.type == pygame.KEYDOWN:
                if (i.key == pygame.K_LEFT) and not(motion == RIGHT):
                    motion = LEFT
                elif (i.key == pygame.K_RIGHT) and not(motion == LEFT):
                    motion = RIGHT
                elif (i.key == pygame.K_UP) and not(motion == DOWN):
                    motion = UP
                elif (i.key == pygame.K_DOWN) and not(motion == UP):
                    motion = DOWN
            # elif i.type == pygame.KEYUP:
            #     if i.key == [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            #         motion = STOP
        if motion == LEFT:
            x-=1
        elif motion == RIGHT:
            x+=1
        elif motion == UP:
            y-=1
        elif motion == DOWN:
            y+=1

        if (x <= 0) or (y <= 0) or (x+1 >= (W//cell_w)) or (y+1 >= (H//cell_w)):
            game=False
        sc.fill(BLACK)
        #code
        drawWorld(pole)
        cds = coords[0:snake_w-1]
        if [x,y] in cds:
            game = False
        if not([x,y] in coords):
            coords.append([x,y])
        if len(coords) > snake_w:
            coords.pop(0)
        # for xx,yy in coords:
        #     # pole[yy][yy] = 1
        #     drawCell(xx,yy, GREEN)
        for i in range(len(meals)):
            # pole[meals[i][0]][meals[i][1]] = 1
            print(meals[i][0],meals[i][1])
            if (x == meals[i][0]) and (y == meals[i][1]):
                pole[meals[i][0]][meals[i][1]] = 0
                snake_w += 1
                meals[i][0] = random.randint(1,W//cell_w-2)
                meals[i][1] = random.randint(1,H//cell_w-2)
                FPC += 0.5
        # for i in range(len(meals)):
        #     drawCell(meals[i][0], meals[i][1], RED)
        pygame.display.update()

def drawCell(x,y, color=WHITE):
    pygame.draw.rect(sc, color, (x*cell_w, y*cell_w, cell_w, cell_w))
def drawWorld(arr):
    for x in range(len(arr)):
        for y in range(len(arr[0])):
            if arr[x][y] == 1:
                drawCell(x,y)

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

main()
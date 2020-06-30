import pygame
import sys
import random

BLACK    =   (0, 0, 0)
WHITE    =   (255, 255, 255)
ORANGE   =   (255, 150, 100)
BLUE     =   (0, 70, 225)
RED      =   (255, 10, 10)
GREEN    =   (10, 255, 10)

W = 600
H = 600
cell_w = 10

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake')

def main():
    FPC = 15
    game = True
    r = 3
    x = (W//cell_w)//2-1
    y = (H//cell_w)//4-1
    coords = [[x,y-4], [x,y-3], [x,y-2], [x,y-1], [x,y]]
    snake_w = 5
    meals = [random.randint(1,W//cell_w-2), random.randint(1,H//cell_w-2)]
    motion = 'to the down'
    LEFT  = 'to the left'
    RIGHT = 'to the right'
    UP    = 'to the up'
    DOWN  = 'to the down'
    while game:    
        clock.tick(FPC)
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
        drawWorld(W, H)
        # if [x,y] in coords:
        #     game = False
        cds = coords[0:snake_w-1]
        if [x,y] in cds:
            game = False
        if not([x,y] in coords):
            coords.append([x,y])
        if len(coords) > snake_w:
            coords.pop(0)
        for xx,yy in coords:
            drawCell(xx,yy, GREEN)
        if (x == meals[0]) and (y == meals[1]):
            snake_w += 1
            meals = [random.randint(1,W//cell_w-2), random.randint(1,H//cell_w-2)]
            FPC += 0.5
        drawCell(meals[0], meals[1], RED)
        pygame.display.update()

def drawCell(x,y, color=WHITE):
    pygame.draw.rect(sc, color, (x*cell_w, y*cell_w, cell_w, cell_w))
def drawWorld(width, height):
    for x in range(width//cell_w):
        drawCell(x, 0)
        drawCell(x, height//cell_w-1)
    for y in range(height//cell_w):
        drawCell(0, y)
        drawCell(width//cell_w-1, y)

main()
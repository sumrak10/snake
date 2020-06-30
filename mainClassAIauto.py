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

W = 600
H = 600
cell_w = 10

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Life')

class Snake_game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pole =[]
        self.pole_backup = []
        self.px = []
        self.py = []
        self.x = width//2
        self.y = height//2
        self.snake_w = 5
        self.motion = 'down'
        self.LEFT  = 'left'
        self.RIGHT = 'right'
        self.UP    = 'up'
        self.DOWN  = 'down'
        self.life = True
        self.coords = [[self.x,self.y-4], [self.x,self.y-3], [self.x,self.y-2], [self.x,self.y-1], [self.x,self.y]]
        self.motion_array = np.zeros((4))
        self.pole = np.zeros((width, height))
        for i in range(width):
            self.pole[i][0] = 1
            self.pole[i][height-1] = 1
        for i in range(height):
            self.pole[0][i] = 1
            self.pole[width-1][i] = 1
        self.meals_num = 5
        self.meals = []
        for i in range(self.meals_num):
            self.meals.append([random.randint(1,self.width-2), random.randint(1,self.height-2)])
            self.pole[self.meals[i][0]][self.meals[i][1]] = 1
    def update_meals(self, meals_num):
        pass
    def drawWorld(self):
        # for i in range(len(self.pole)):
            # self.pole[self.coords[i][0]][self.coords[i][1]] = 1
        
        # for i in range(len(self.coords)):
        #     drawCell(self.coords[i][0],self.coords[i][1], GREEN)
        
        sc.fill(BLACK)
        for x in range(len(self.pole)):
            for y in range(len(self.pole[0])):
                if self.pole[x][y] == 1:
                    drawCell(x,y)
    def motionSnake(self, AI_out):
        # for i in pygame.event.get():
        #     if i.type == pygame.QUIT: exit()
        #     elif i.type == pygame.KEYDOWN:
        #         if (i.key == pygame.K_LEFT) and not(self.motion == self.RIGHT):
        #             self.motion_array = np.zeros((4))
        #             self.motion = self.LEFT
        #             self.motion_array[1] = 1
        #         elif (i.key == pygame.K_RIGHT) and not(self.motion == self.LEFT):
        #             self.motion = self.RIGHT
        #             self.motion_array[3] = 1
        #         elif (i.key == pygame.K_UP) and not(self.motion == self.DOWN):
        #             self.motion = self.UP
        #             self.motion_array[0] = 1
        #         elif (i.key == pygame.K_DOWN) and not(self.motion == self.UP):
        #             self.motion = self.DOWN
        #             self.motion_array[2] = 1
        if (round(AI_out[0][1]) == 1) and (self.motion == self.RIGHT):
            self.x-=1
        elif (round(AI_out[0][3]) == 1) and (self.motion == self.LEFT):
            self.x+=1
        elif (round(AI_out[0][0]) == 1) and (self.motion == self.DOWN):
            self.y-=1
        elif (round(AI_out[0][2]) == 1) and (self.motion == self.UP):
            self.y+=1
    def logicSnake(self):
        # collision with meals
        for i in range(len(self.meals)):
            if (self.x == self.meals[i][0]) and (self.y == self.meals[i][1]):
                self.pole[self.meals[i][0]][self.meals[i][1]] = 0
                self.snake_w += 1
                self.meals[i][0] = random.randint(1,W//cell_w-2)
                self.meals[i][1] = random.randint(1,H//cell_w-2)
                self.pole[self.meals[i][0]][self.meals[i][1]] = 1
        # collision with walls
        if (self.x <= 0) or (self.y <= 0) or (self.x+1 >= self.width) or (self.y+1 >= self.height):
            self.life = False
        #collision with itself6
        cds = self.coords[0:self.snake_w-1]
        if [self.x,self.y] in cds:
            self.life = False
        #the tail of the snake
        if len(self.coords) > self.snake_w:
            self.coords.pop(0)
            self.pole[self.coords[0][0]][[self.coords[0][1]]] = 0
        if not([self.x,self.y] in self.coords):
            self.coords.append([self.x,self.y])
            self.pole[self.x][self.y] = 1

def main():
    FPC = 20
    game = True
    
    s1 = Snake_game(W//cell_w, H//cell_w)

    # np.random.seed(1)
    # syn0 = 2*np.random.random((3600, 1800)) - 1
    # syn1 = 2*np.random.random((1800,900)) - 1
    # syn2 = 2*np.random.random((900,4)) - 1
    syn = np.load('snake_brain.npz')
    syn0 = syn['syn0']
    syn1 = syn['syn1']
    syn2 = syn['syn2']


    while s1.life:   
        clock.tick(FPC)
        l0 = np.array( s1.pole.reshape(1,s1.width*s1.height) )
        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))
        l3 = nonlin(np.dot(l2,syn2))
        print(l3)
        s1.motionSnake(l3)
        s1.logicSnake()
        s1.drawWorld()
        pygame.display.update()

    np.savez('snake_brain',syn0=syn0, syn1=syn1, syn2=syn2)

def drawCell(x,y, color=WHITE):
    pygame.draw.rect(sc, color, (x*cell_w, y*cell_w, cell_w, cell_w))
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

main()
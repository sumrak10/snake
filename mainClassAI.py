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

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Life')

class Snake_game:
    def __init__(self, width, height, meals):
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
        self.error = False
        self.correct = False
        self.coords = [[self.x,self.y-4], [self.x,self.y-3], [self.x,self.y-2], [self.x,self.y-1], [self.x,self.y]]
        self.error_motion_array = np.zeros((4))
        self.motion_array = np.zeros((4))
        self.pole = np.zeros((width, height))
        for i in range(width):
            self.pole[i][0] = 1
            self.pole[i][height-1] = 1
        for i in range(height):
            self.pole[0][i] = 1
            self.pole[width-1][i] = 1
        self.meals = meals
        for i in range(len(self.meals)):
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
    def motionSnake(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT: exit()
            elif i.type == pygame.KEYDOWN:
                if (i.key == pygame.K_LEFT) and not(self.motion == self.RIGHT):
                    self.motion_array = np.zeros((4))
                    self.motion = self.LEFT
                    self.motion_array[1] = 1
                elif (i.key == pygame.K_RIGHT) and not(self.motion == self.LEFT):
                    self.motion_array = np.zeros((4))
                    self.motion = self.RIGHT
                    self.motion_array[3] = 1
                elif (i.key == pygame.K_UP) and not(self.motion == self.DOWN):
                    self.motion_array = np.zeros((4))
                    self.motion = self.UP
                    self.motion_array[0] = 1
                elif (i.key == pygame.K_DOWN) and not(self.motion == self.UP):
                    self.motion_array = np.zeros((4))
                    self.motion = self.DOWN
                    self.motion_array[2] = 1
        if self.motion == self.LEFT:
            self.x-=1
        elif self.motion == self.RIGHT:
            self.x+=1
        elif self.motion == self.UP:
            self.y-=1
        elif self.motion == self.DOWN:
            self.y+=1
    def logicSnake(self):
        # collision with meals
        for i in range(len(self.meals)):
            if (self.x == self.meals[i][0]) and (self.y == self.meals[i][1]):
                self.pole[self.meals[i][0]][self.meals[i][1]] = 0
                self.snake_w += 1
                # self.meals[i][0] = random.randint(1,W//cell_w-2)
                # self.meals[i][1] = random.randint(1,H//cell_w-2)
                self.meals[i][0] = self.width // 2 - 10
                self.meals[i][1] = self.height // 2
                self.pole[self.meals[i][0]][self.meals[i][1]] = 1
                self.correct = True
        # collision with walls
        if (self.x <= 0) or (self.y <= 0) or (self.x+1 >= self.width) or (self.y+1 >= self.height):
            self.life = False
            self.error = True
        #collision with itself6
        cds = self.coords[0:self.snake_w-1]
        if [self.x,self.y] in cds:
            self.life = False
            self.error = True
        #the tail of the snake
        if len(self.coords) > self.snake_w:
            self.coords.pop(0)
            self.pole[self.coords[0][0]][[self.coords[0][1]]] = 0
        if not([self.x,self.y] in self.coords):
            self.coords.append([self.x,self.y])
            self.pole[self.x][self.y] = 1

def main():
    FPC = 60
    game = True
    meals = []
    meals_num = 3
    width = W//cell_w
    height = H//cell_w
    mealx = width // 2
    mealy = height // 2
    for i in range(meals_num-1):
        meals.append([random.randint(1,width-2), random.randint(1,height-2)])
        meals.append([mealx-5, mealy])

    # np.random.seed(1)
    # syn0 = 2*np.random.random((9, 18)) - 1
    # syn1 = 2*np.random.random((18,8)) - 1
    # syn2 = 2*np.random.random((8,4)) - 1
    syn = np.load('snake_brain.npz')
    syn0 = syn['syn0']
    syn1 = syn['syn1']
    syn2 = syn['syn2']

    for loop in range(300):
        s1 = Snake_game(W//cell_w, H//cell_w, meals)
        s1.life = True
        while s1.life:   
            clock.tick(FPC)

            l0 = np.array( [[s1.pole[s1.x-1][s1.y-1],    s1.pole[s1.x][s1.y-1],     s1.pole[s1.x+1][s1.y-1], 
                            s1.pole[s1.x-1][s1.y],      s1.pole[s1.x][s1.y],       s1.pole[s1.x+1][s1.y], 
                            s1.pole[s1.x+1][s1.y-1],    s1.pole[s1.x][s1.y+1],     s1.pole[s1.x+1][s1.y+1] ]] )
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            if round(l3[0][0]) == 1:
                s1.motion_array = np.zeros((4))
                s1.motion = s1.UP
                s1.motion_array[0] = 1
                error_motion = np.array([[0,1,0,1]])
                correct_motion = np.array([[1,0,0,0]])
            elif round(l3[0][1]) == 1:
                s1.motion_array = np.zeros((4))
                s1.motion = s1.LEFT
                s1.motion_array[1] = 1
                error_motion = np.array([[1,0,1,0]])
                correct_motion = np.array([[0,1,0,0]])
            elif round(l3[0][2]) == 1:
                s1.motion_array = np.zeros((4))
                s1.motion = s1.DOWN
                s1.motion_array[2] = 1
                error_motion = np.array([[0,1,0,1]])
                correct_motion = np.array([[0,0,1,0]])
            elif round(l3[0][3]) == 1:
                s1.motion_array = np.zeros((4))
                s1.motion = s1.RIGHT
                s1.motion_array[3] = 1
                error_motion = np.array([[1,0,0,1]])
                correct_motion = np.array([[0,0,0,1]])
            s1.motionSnake()
            s1.logicSnake()
            s1.drawWorld()
            if s1.correct:
                l3_error = correct_motion - l3
                s1.correct = False
            elif s1.error:
                l3_error = error_motion - l3
                s1.error = False
            else: 
                l3_error = s1.motion_array - l3
            
            l3_delta = l3_error*nonlin(l3,deriv=True)
            l2_error = l3_delta.dot(syn2.T)
            l2_delta = l2_error*nonlin(l2,deriv=True)
            l1_error = l2_delta.dot(syn1.T)
            l1_delta = l1_error * nonlin(l1,deriv=True)

            syn2 += l2.T.dot(l3_delta)
            syn1 += l1.T.dot(l2_delta)
            syn0 += l0.T.dot(l1_delta)
            pygame.display.update()
        print(loop)
    np.savez('snake_brain',syn0=syn0, syn1=syn1, syn2=syn2)
    print('saved')

def drawCell(x,y, color=WHITE):
    pygame.draw.rect(sc, color, (x*cell_w, y*cell_w, cell_w, cell_w))
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))



main()
import random
import pygame, random, sys
from pygame.locals import *
import time

# initialize with pygame
pygame.init()

# create game window, width and height
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
JUMP_HEIGHT_FACTOR = 0.50
pygame.mixer.music.load('background.mid')

#Title of game
pygame.display.set_caption("a cool thing to play")

clock = pygame.time.Clock()
fps = 27

#load images into pygame, into an array
walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'), pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'), pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]

walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'), pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'), pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]

bg = pygame.image.load('pics/bg.png')
char = pygame.image.load('pics/standing.png')
tweed = pygame.image.load('pics/tumbleweed.png')

tumbleweeds = []

#tumbleWeed class
class TumbleWeed(object):
    def __init__(self):
        self.direction = random.randint(0,1)
        if self.direction == 0:
            self.direction = -1
        self.velocity = random.randint(5,10) * self.direction
        if self.direction == 1:
            self.x = 0
            self.y = 432
        else:
            self.x = 750
            self.y = 432
        tumbleweeds.append(self)
    def draw(self, window):
        if (self.x > 750 or self.x < 0):
            tumbleweeds.remove(self)
        else:
            window.blit(tweed, (self.x, self.y))
        self.x += self.velocity
        
        return self.x
        
        
t1 = TumbleWeed()

#player class
class Player(object):
    #constructor
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.stopped = True
        self.walkCount = 0
        
    def draw(self, window):
        if self.walkCount + 1 >= fps: # bc we have 9 sprites per side, and use 3 per frame
               self.walkCount = 0
               
        if self.left:
            window.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # integer division in python //
            self.walkCount += 1
        elif self.right:
            window.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
           window.blit(char, (self.x, self.y))
           self.walkCount = 0
            
        
        return [self.x, self.y]


class drawWindow(object):
    def __init__(self):
        self.NUM_LIVES = 15
        self.POINTS = 0

    # edit sprite at the end of each main loop
    def redrawGameWindow(self, mode = 0):
        # prevents object from drawing on top of itself
        window.blit(bg, (0,0))
        
        
        font = pygame.font.Font('freesansbold.ttf', 32)
        str_text = "Lives Left: " +  str((self.NUM_LIVES // 5) + 1)
        text_img = font.render(str_text, True, (255, 255, 255))
        textRect = text_img.get_rect()
        textRect.center = (150, 50)
        window.blit(text_img, textRect)
        
        if (mode == 0):
            self.POINTS += 1
            
        text_img = font.render("Points: " + str(self.POINTS), True, (255, 255, 255))
        textRect = text_img.get_rect()
        textRect.center = (150, 100)
        window.blit(text_img, textRect)
            
        # draw character
        player_place = p1.draw(window)
        
        upper_bound = 75
        gen_new = random.randint(0, upper_bound)
        if gen_new == 0:
            TumbleWeed()
        if gen_new == 1:
            upper_bound -= 1
        for item in tumbleweeds:
            tweed_place = item.draw(window)
            tweed_place += 16
            if (player_place[1] >= 400 - 32 and
                abs(tweed_place - player_place[0]) <= 16):
                    self.NUM_LIVES -= 1
        
        
        if mode != 0:
            font = pygame.font.Font('freesansbold.ttf', 32)
            str_text = "GAME OVER"
            text_img = font.render(str_text, True, (255, 255, 255))
            textRect = text_img.get_rect()
            textRect.center = (375, 250)
            window.blit(text_img, textRect)
            
            str_text = "Press SPACE to Start Over."
            text_img = font.render(str_text, True, (255, 255, 255))
            textRect.center = (375, )
            window.blit(text_img, textRect)
            
        pygame.display.update()
        
        return {"num_lives": (self.NUM_LIVES // 5) + 1, "points": self.POINTS}
            
        
def renderGameOver(points):
    w1.redrawGameWindow(1)
    
    loop = True
    while loop:
        pygame.time.delay(50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
           return
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            
    
  
#main loop
p1 = Player(50, 400, 64, 64)
w1 = drawWindow()
run = True
pygame.mixer.music.play(-1, 0.0)
game_state = {"num_lives": 4, "points": 0}
while run:
    # make game not run too fast from key presses
    # pygame.time.delay(50) # 100 ms
    
    #set frame rate to 27
    clock.tick(fps)
            
    # check for events (input from user, ex: key presses, mouse moement)
    # loop through all events
    for event in pygame.event.get():
        # check if user tries to exit, let them exit (exit loop first)
        if event.type == pygame.QUIT:
            run = False
        
        # key presses, hold right arrow key (only moves character one time,
        # doesn't continue to move character
        # HOLD DOWN key, continue to move character that direction
            # make list of key presses
    keys = pygame.key.get_pressed()
        # THIS way if these keys are pressed or they are held down
        # move character by the velocity in whatever direction
        
        # pygame grid, top left is 0, 0
        # down is positive y, right is positive x
    if keys[pygame.K_LEFT] and p1.x > p1.vel: # left arrow key
        p1.x -= p1.vel
        p1.left = True
        p1.right = False
        p1.stopped = False
    elif keys[pygame.K_LEFT]:
        p1.x = 0
        p1.left = True
        p1.right = False
    elif keys[pygame.K_RIGHT] and p1.x < SCREEN_WIDTH - p1.width:
        p1.x += p1.vel
        p1.left = False
        p1.right = True
    elif keys[pygame.K_RIGHT]:
        p1.x = SCREEN_WIDTH - p1.width
        p1.left = False
        p1.right = True
    else:
        p1.walkCount = 0
        p1.left = False
        p1.right = False
        
        
    
    if not(p1.isJump):
        if keys[pygame.K_UP]:
            p1.isJump = True
        # want to do a parabola
    else:
        if p1.jumpCount >= 0:
            #quadratically jump
            p1.y -= (p1.jumpCount ** 2) * JUMP_HEIGHT_FACTOR
            p1.jumpCount -= 1
        elif p1.jumpCount >= -10:
            p1.y += (p1.jumpCount **2) * JUMP_HEIGHT_FACTOR
            p1.jumpCount -= 1
        else:
            #jump has concluded
            p1.isJump = False
            p1.jumpCount = 10
            
    game_state = w1.redrawGameWindow()
    
    if game_state["num_lives"] <= 0:
        renderGameOver(game_state["points"])
        p1 = Player(50, 400, 64, 64)
        w1 = drawWindow()
        
    


#quit the window
pygame.quit()


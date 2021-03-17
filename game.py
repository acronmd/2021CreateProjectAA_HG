
import pygame, sys, os
from pygame.locals import *


#define important variables
screenWidth = 1080
screenHeight = 720
size = screenWidth, screenHeight
gameRunning = True
clock = pygame.time.Clock()

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption('Aidan\'s new game!')
    ball = Player("ball2.png")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #camera offsets and minimum values to move camera, while also setting variables for the tile renderer to use
    CameraX = 0
    CameraY = 0
    screenMinRight = 950
    screenMinRightMap = screenMinRight
    screenMinLeft = 130
    screenMinLeftMap = screenMinLeft

    #jumping variables, force is how high player jumps
    jumping = False
    jumpForce = 12
    jumpTime = jumpForce

    #velocity variables
    xChange = 0
    accel = 0
    maxSpeed = 12
    accelChange = .8

    holdingLeft = False
    holdingRight = False

    #uses os to generate an array based on the names of files in the directory, creates the map index
    #and screen offset horizontal variable used in the tile renderer
    mapTileset = os.listdir("Graphics\\Tiles")
    mapIndex = 0
    screenOffsetX = 0

    #tile loader and unloader, used for loading and unloading background when needed
    def showTiles():
        screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex]).convert_alpha(), (screenOffsetX * (1080 * mapIndex) - CameraX, 0 - CameraY))
        screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex + 1]).convert_alpha(), (screenOffsetX + 1 * (1080 * (mapIndex + 1)) - CameraX, 0 - CameraY))

    # Event loop
    while gameRunning == True:
        #FPS lock
        clock.tick(60)
        #detect X on window and key release
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    holdingLeft = False
                    accel = 0
                if event.key == pygame.K_d:
                    holdingRight = False
                    accel = 0
                

        #gravity plus initial floor collision
        if jumping == True:
            gravityVal = 0
        else:
            gravityVal = 10
            if ball.y <= 580:
                ball.y += gravityVal

        #Pygame Control Detection   
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            holdingLeft = True
        if keys[pygame.K_d]:
            holdingRight = True
        
        if keys[pygame.K_t]:
            if mapIndex == 1:
                CameraX = 2160
                CameraY = 0
        
        #jumping system, uses a math equation to generate a smooth arc
        if jumping == False:
            if keys[pygame.K_SPACE]:
                jumping = True
        
        if jumping == True:
            if jumpTime >= -jumpForce:
                ball.y -= (jumpTime * abs(jumpTime)) * 0.5
                jumpTime -= 1
            else:
                jumpTime = jumpForce
                jumping = False


        #blit camera movement and player movement, order matters
        showTiles()
        screen.blit(ball.getImage(), (ball.x - CameraX,ball.y - CameraY))

        #tile renderer, detects where the player is on the horizontal scale between the 3 mapIndex floor levels
        if ball.x >= (screenWidth + screenMinRightMap) and mapIndex <1:
            screenMinRightMap += 950
            screenOffsetX += 1
            mapIndex += 1
        
        if ball.x <= (screenWidth + screenMinLeftMap) and mapIndex == 1:
            screenMinRightMap = 950
            screenOffsetX -= 1
            mapIndex -= 1

        #if player is past a certain x value, move camera to adjust for it
        if ball.x > screenMinRight and ball.x < 3110:
            CameraX += 10
            screenMinRight += 10
            screenMinLeft += 10
        if ball.x < screenMinLeft and ball.x > 130:
            CameraX += -10
            screenMinRight += -10
            screenMinLeft += -10
        
        #accelerate code

        if holdingLeft == True:
            accel = -accelChange
        if holdingRight == True:
            accel = accelChange

        xChange += (accel*1.4)
        
        if accel == 0 and xChange > .6:
            xChange -= .3
        elif accel == 0 and xChange < -.6:
            xChange += .3
        elif accel == 0:
            xChange = 0
        

        if abs(xChange) >= maxSpeed:
            xChange = xChange/abs(xChange) * maxSpeed

        ball.x += xChange
        
        pygame.display.flip()

#entity class to make loading assets easier
class Entity(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

#generate entity with imagename as input under the player subclass of entity class
class Player(Entity):
    def __init__(self, imageName):
        self.x=0
        self.y=0
        Entity.__init__(self)
        self.image = pygame.image.load("Graphics\\" + imageName).convert_alpha()
    
    def getImage(self):
        return self.image

if __name__ == '__main__': main()
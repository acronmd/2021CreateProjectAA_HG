
import pygame, sys, os
from pygame.locals import *


#define important variables
screenWidth = 1080
screenHeight = 720
size = screenWidth, screenHeight
gameRunning = True
clock = pygame.time.Clock()
scores = open("scores.txt", "r")
highScores = scores.read().split(",")
### next portion of code reworked from kite python docs about replacing strings in lists
highScores = [s.replace("[", "") for s in highScores]
highScores = [s.replace("]", "") for s in highScores]
### end of reworked code
for i in range(0, len(highScores)):
    highScores[i] = int(highScores[i])

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption('Draft Game')
    ball = Player("turtle1.png", 0, 0)
    wall = Collision("Wall.png", 600, 590)
    isDead = False
    isMoving = False
    enemyRunning = False
    affected = True
    scoreSet = False
    speed = 11
    wallMinVal = 0

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #camera offsets and minimum values to move camera, while also setting variables for the tile renderer to use
    CameraX = 0
    CameraY = 0
    screenMinRight = 650
    screenMinRightMap = screenMinRight
    screenMinLeft = 130
    screenMinLeftMap = screenMinLeft
    offset = 0

    #jumping variables, force is how high player jumps
    grounded = False
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
    mapIndex2 = 3
    
    screenOffsetX = 0


    #tile loader and unloader, used for loading and unloading background when needed
    def showTiles(offset):
        if isMoving == False:
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex]).convert_alpha(), (offset * (1080 * mapIndex) - CameraX, 0))
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex + 1]).convert_alpha(), (offset + 1 * (1080 * (mapIndex + 1)) - CameraX, 0 - CameraY))
        elif mapIndex == 3:
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex]).convert_alpha(), (offset + 1 * (1080 * mapIndex2 + 1) - CameraX, 0))
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex + 1]).convert_alpha(), (offset + 1 * (1080 * (mapIndex2 + 1)) - CameraX, 0 - CameraY))
        else:
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex]).convert_alpha(), (offset + 1 * (1080 * mapIndex + 1) - CameraX, 0))
            screen.blit(pygame.image.load("Graphics\\Tiles\\" + mapTileset[mapIndex + 1]).convert_alpha(), (offset + 1 * (1080 * (mapIndex + 1)) - CameraX, 0 - CameraY))
            print("player" + str(ball.x))
            print("enemy" + str(wall.x))

    player_image = ball.getImage()
    player_rect = pygame.Rect(ball.x, ball.y, player_image.get_width() - 60, player_image.get_height())
    
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
        if jumping or grounded == True:
            gravityVal = 0
        else:
            gravityVal = 10
            if ball.y <= 465:
                ball.y += gravityVal

        if ball.y == 470:
            grounded = True

        #Pygame Control Detection   
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_a] and isDead == False:
            holdingLeft = True
        if inputs[pygame.K_d] and isDead == False:
            holdingRight = True
        
        if inputs[pygame.K_t]:
            if mapIndex == 1:
                isMoving = True
                enemyRunning = True
                affected = False
                wall.x = 1100
                CameraX = 2160
                screenMinRightMap = 2159
                CameraY = 0
        
        #jumping system, uses a math equation to generate a smooth arc
        if jumping == False:
            if inputs[pygame.K_SPACE] and isDead == False:
                jumping = True
                grounded = False
        
        if jumping == True:
            if jumpTime >= -jumpForce:
                ball.y -= (jumpTime * abs(jumpTime)) * 0.5
                jumpTime -= 1
            else:
                jumpTime = jumpForce
                jumping = False

        if affected == True:
            player_rect.x = ball.x + 30
        else:
            player_rect.x = ball.x + 30 - CameraX
        player_rect.y = ball.y
        wall.rect.x = wall.x
        wall.rect.y = wall.y
        showTiles(screenOffsetX)
        screen.blit(ball.getImage(), (ball.x - CameraX,ball.y - CameraY))
        #make the spike move with camera or being a stationary object independent from the camera
        if affected == True:
            screen.blit(wall.getImage(), (wall.x - CameraX, wall.y - CameraY))
        else:
            screen.blit(wall.getImage(), (wall.x , wall.y))
        #death screen and collision
        if isDead == True:
            screen.blit(pygame.image.load("Graphics\\" + "death.png").convert_alpha(), (90, 90))
            if scoreSet == False:
                highScores.append(round(ball.x))
                highScores.sort(reverse=True)
                open("scores.txt", "w+").write(str(highScores))
                scoreSet = True
                print(highScores)
        if player_rect.colliderect(wall.rect): 
            isDead = True

        #tile renderer, detects where the player is on the horizontal scale between the mapIndex floor levels
        if affected == False and CameraX > screenMinRightMap:
            screenMinRightMap += 1080
            if mapIndex == 3:
                mapIndex = mapIndex
                mapIndex2 += 1
            else:
                mapIndex += 1


        if ball.x >= (screenWidth + screenMinRightMap) and mapIndex <1:
            screenMinRightMap += 650
            screenOffsetX += 1
            mapIndex += 1

        if isMoving == True:
            CameraX += 5
            screenMinRight += 5
            screenMinLeft += 5

        if enemyRunning == True:
            wall.x -= speed
            if wall.x < -30:
                speed += 2
                wall.x = 1100
        


        # vertical map code
        #if ball.x <= (screenWidth + screenMinLeftMap) and mapIndex == 1:
        #    screenMinRightMap = 950
        #    screenOffsetX -= 1
        #    mapIndex -= 1
        
        #if player is past a certain x value, move camera to adjust for it
        if ball.x > screenMinRight and isMoving == False:
            CameraX += 10
            screenMinRight += 10
            screenMinLeft += 10
        if ball.x < screenMinLeft and ball.x > 130 and isMoving == False:
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
    def __init__(self, imageName, xPos, yPos):
        self.x= xPos
        self.y= yPos
        Entity.__init__(self)
        self.image = pygame.image.load("Graphics\\" + imageName).convert_alpha()
        self.walkIndex = 0
    
    def getImage(self):
        return self.image
    

class Collision(Entity):
    def __init__(self, imageName, provX, provY):
        self.image = pygame.image.load("Graphics\\" + imageName).convert_alpha()
        self.x = provX
        self.y = provY
        self.rect = self.image.get_rect()
        self.rect.x = provX
        self.rect.y = provY
    
    def getImage(self):
        return self.image

if __name__ == '__main__': main()
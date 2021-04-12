import pygame
from pathlib import Path

pygame.init()

screen = pygame.display.set_mode((800,600))



logo_path = Path('./images/logo.png')
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(logo_path)
pygame.display.set_icon(icon)
running = True



#Player
playerImg = pygame.image.load(Path('./images/spaceship.png'))
playerX = 370
playerY = 480

delta_X = 0
delta_Y = 0

delta=1

enemyImg = pygame.image.load(Path('./images/ufo.png'))
enemyX = 370
enemyY = 100

enemy_speed = 0.5

projectile_speed= -2
projectileImg = pygame.image.load(Path('./images/laser.png'))
hitcount=0



def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y):
    screen.blit(enemyImg, (x,y))

def laser(projectiles):
    for projectile in projectiles:
        screen.blit(projectileImg,projectile)

def checkColission(enemyX, enemyY, projectiles):
    global hitcount
    for i,projectile in enumerate(projectiles):
        if enemyX<projectile[0]+8<enemyX+64 and enemyY<projectile[1]<enemyY+64:
            hitcount+=1
            print(f"Hit! Hit count is: {hitcount}")
            del projectiles[i]
            return


projectiles = []
while running:
    
    screen.fill((0,0,0))
    
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_X = -delta
            if event.key == pygame.K_RIGHT:
                delta_X = delta
            if event.key == pygame.K_UP:
                delta_Y = -delta
            if event.key == pygame.K_DOWN:
                delta_Y = delta
            if event.key == pygame.K_z:
                projectiles.append([playerX+24, playerY])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                delta_X=0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                delta_Y=0
        
    if (playerX > 800-64 and delta_X > 0) or (playerX<=0 and delta_X < 0):
        x_stop_factor=0
    else:
        x_stop_factor=1
    
    if (playerY > 600-64 and delta_Y > 0) or (playerY <= 0 and delta_Y < 0):
        y_stop_factor=0
    else:
        y_stop_factor=1

    if not 700 > enemyX > 100-64:
        enemy_speed*=-1            


    playerX += delta_X*x_stop_factor
    playerY += delta_Y*y_stop_factor

    enemyX += enemy_speed
    projectiles = [[x,y+projectile_speed] for x,y in projectiles if not y+projectile_speed<=0]

    player(playerX,playerY)
    enemy(enemyX,enemyY)
    laser(projectiles)
    checkColission(enemyX,enemyY,projectiles)


    pygame.display.update()
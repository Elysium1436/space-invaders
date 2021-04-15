import pygame
import numpy as np
""" 
Todo:
Use the draw methods of the sprite superclass.
music, repetition, game over screen, 

"""

def obj_creator(obj, position, image_path):
    obj.image = pygame.image.load(image_path)
    obj.rect = obj.image.get_rect(topleft=position)

class EnemyContainer(pygame.sprite.Group):
    def __init__(self,game,n_rows=3, n_cols=6,y_offset=100, period=2000,**kwargs):
        super().__init__(kwargs)
        self.create_group(game,n_cols,n_rows, y_offset)
        pygame.time.set_timer(33333, period)
        self.move_y = False

    def create_group(self, game,n_cols, n_rows, y_offset, space_in_between=20):
        assert n_cols%2==0
        placeholder = Enemy(game)
        enemy_width = placeholder.rect.width + space_in_between
        enemy_height = placeholder.rect.height
        self.vx = enemy_width
        self.vy = enemy_height
        screen_width = game.screen.get_width()
        
        x_offset = (screen_width-n_cols*enemy_width)//2
        self.rect = pygame.Rect(x_offset, y_offset, n_cols*enemy_width, n_rows*enemy_height)
        
        for x in range(n_cols):
            for y in range(n_rows):
                position = (x_offset+x*enemy_width, y_offset+y*enemy_height)
                self.add(Enemy(game, initial_position=position))

    def move_group(self,game):
        if self.rect.left + self.vx < 0 or self.rect.right + self.vx > game.screen.get_width():
            self.vx*=-1
            self.move_y = True
        self.rect.move_ip(self.vx*(not self.move_y), self.vy*self.move_y)
        for enemy in self:
            enemy.rect.move_ip(self.vx*(not self.move_y), self.vy*self.move_y)
        self.move_y = False
          
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, speed=5, initial_position=None):
        super().__init__()
        self.game = game
        self.vx = 0 
        self.vy = 0
        self.image = pygame.image.load('./images/ufo.png')
        self.speed = speed
        self.explosion_sound = pygame.mixer.Sound('./sound/explosion.mp3')
        self.shoot_sound = pygame.mixer.Sound('./sound/zap.mp3')
        if not initial_position:
            initial_x = self.game.screen.get_width()//2
            initial_y = self.game.screen.get_height()//5
            initial_position = (initial_x, initial_y)

        obj_creator(self, initial_position, './images/ufo.png')
    
    def set_position(self,position,rect_attr='topleft'):
        setattr(self, rect_attr, position)
    
    def kill(self):
        self.explosion_sound.play()
        super().kill()
    
    def shoot(self):
        Projectile(self.game, self.rect.midtop, 0, 2, self.game.playergroup)
        self.shoot_sound.play()
    
    def check_shoot(self):
        l = 0.10/60
        p = 1-np.exp(-l)
        if p >= np.random.random():
            self.shoot()
        
    def update(self):
        self.rect.move_ip((self.vx,self.vy))
        self.check_shoot()
        self.game.screen.blit(self.image, self.rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, initial_position, vx, vy, target_group):
        super().__init__()
        obj_creator(self, initial_position, './images/laser.png')
        self.vx = vx
        self.vy = vy
        self.target = target_group
        self.game = game
        self.game.projectiles.add(self)
    
    def check_oob(self):
        if self.rect.bottom > self.game.screen.get_height() or self.rect.bottom < 0:
            self.kill()
    
    def check_collision(self):
        hl = pygame.sprite.spritecollide(self, self.target, True)
        if hl:
            print('collided')
            self.kill()
    
    def update(self):
        self.rect.move_ip((self.vx, self.vy))
        self.check_collision()
        self.check_oob()
        self.game.screen.blit(self.image, self.rect)
        
class Player(pygame.sprite.Sprite):
    def __init__(self,game, speed=5, initial_position=None):
        super().__init__()
        self.game = game
        self.vx = 0
        self.vy = 0
        self.image = pygame.image.load('./images/spaceship.png')
        self.speed = speed
        if initial_position is None:
            #Get default initial position based on screen dimensions
            init_x = self.game.screen.get_width()//2
            init_y = int(self.game.screen.get_height()*0.85)
            initial_position = (init_x, init_y)
           
        self.rect = self.image.get_rect(center=initial_position)
        
    def move_left(self):
        self.vx -= self.speed
    
    def move_right(self):
        self.vx += self.speed
    
    def move_up(self):
        self.vy -= self.speed
    
    def move_down(self):
        self.vy += self.speed
    
    def mirror(self):
        """Implements mirroring of player. Transports the player to the other of of the
        screen if he passes the boundry"""
        
        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()

        if self.rect.centerx < 0 and self.vx < 0:
            self.rect.centerx = screen_width
        if self.rect.centerx > screen_width:
            self.rect.centerx = 0
        if self.rect.centery < 0 and self.vy < 0:
            self.rect.centery = 0
        if self.rect.centery > screen_height and self.vy > 0:
            self.rect.centery = screen_height
        
    def shoot(self):
        Projectile(self.game, self.rect.midtop, 0, -2, self.game.enemy_group)
   
    def kill(self):
       print("Game Over")
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left()
                if event.key == pygame.K_RIGHT:
                    self.move_right()
                if event.key == pygame.K_UP:
                    self.move_up()
                if event.key == pygame.K_DOWN:
                    self.move_down()
                if event.key == pygame.K_z:
                    self.shoot()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_right()
                if event.key == pygame.K_RIGHT:
                    self.move_left()
                if event.key == pygame.K_UP:
                    self.move_down()
                if event.key == pygame.K_DOWN:
                    self.move_up()

        self.rect.move_ip((self.vx, self.vy))
        self.mirror()
        self.game.screen.blit(self.image, self.rect)
    
class Game:
    def __init__(self, screen_size=((800,600))):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.background = pygame.image.load('./images/background.jpg')
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load('./images/logo.png')
        pygame.display.set_icon(icon)
        self.running = True
        self.player = Player(self)
        self.playergroup = pygame.sprite.Group()
        self.playergroup.add(self.player)
        self.projectiles = pygame.sprite.Group()
        self.enemy_group = EnemyContainer(self)
        

    def execute(self):
        c = pygame.time.Clock()
        while self.running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.background, (0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == 33333:
                    self.enemy_group.move_group(self)
            self.playergroup.update(events)
            self.projectiles.update()
            self.enemy_group.update()
            pygame.display.update()
            c.tick(60)

g = Game()
g.execute()
import pygame
from settings import *

class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
      super().__init__(groups)
      self.image = pygame.Surface(size)
      self.image.fill(COLORS['yellow'])
      self.rect = self.image.get_rect(topleft =  pos)
      self.old_rect = self.rect.copy()
      
class MovingVerticalObstacle(StaticObstacle):
    def __init__(self, pos, size, groups):
       super().__init__(pos, size, groups)
       self.image.fill(COLORS['green'])
       self.pos = vec(self.rect.topleft)
       self.direction = vec(0,1)
       self.speed = 450
       self.old_rect = self.rect.copy()
       
    def update(self, dt):
        self.old_rect = self.rect.copy()
        if self.rect.bottom > HEIGHT - self.rect.height:
            self.rect.bottom = 600
            self.pos.y = self.rect.y
            self.direction *= -1
        if self.rect.top < 120:
            self.rect.top = 120
            self.pos.y = self.rect.y
            self.direction *= -1
            
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        
class MovingHorizontalObstacle(StaticObstacle):
    def __init__(self, pos, size, groups):
       super().__init__(pos, size, groups)
       self.image.fill(COLORS['purple'])
       self.pos = vec(self.rect.topleft)
       self.direction = vec(1,0)
       self.speed = 450
       self.old_rect = self.rect.copy()
       
    def update(self, dt):
        self.old_rect = self.rect.copy()
        if self.rect.right > WIDTH - self.rect.width:
            # self.rect.right = 1000
            self.pos.x = self.rect.x
            self.direction *= -1
        if self.rect.left < self.rect.width:
            # self.rect.left = 600
            self.pos.x = self.rect.x
            self.direction *= -1
            
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, player):
      super().__init__(groups)
      self.image = pygame.Surface((40, 40))
      self.image.fill(COLORS['red'])
      self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))
      
      self.pos = vec(self.rect.topleft)
      self.direction = vec(1,1)
      self.speed = 400
      self.old_rect = self.rect.copy()
      
      self.obstacles = obstacles
      self.player = player
    
    def window_collision(self, direction):
        if direction == DIRECTION[0]:
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1     
            if self.rect.right >= WIDTH:
                self.rect.right =  WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
                
        if direction == DIRECTION[1]:
            if self.rect.top <= 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1   
                  
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom =  HEIGHT
                self.pos.y = self.rect.y
                self.direction.y *= -1       
             
    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        
        # collision with player
        if(self.rect.colliderect(self.player.rect)):
            collision_sprites.append(self.player)
        
        # body obstacle
        if collision_sprites:
            if direction == DIRECTION[0]:
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction *= -1
                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction *= -1
                    
            if direction == DIRECTION[1]:
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.bottom:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction *= -1
                    # collision on the bottom
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction *= -1
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
               
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()        
            
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision(DIRECTION[0])
        self.window_collision(DIRECTION[0])
        
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision(DIRECTION[1])
        self.window_collision(DIRECTION[1])

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles):
      super().__init__(groups)
      
      # image
      self.image = pygame.Surface((32, 32))
      self.image.fill(COLORS['blue'])
      
      # position
      self.rect = self.image.get_rect(topleft = (640, 360))
      self.old_rect = self.rect.copy()
      
      # movement
      self.pos = vec(self.rect.topleft)
      self.direction = vec((0, 0))
      self.speed = 200
      
      
      # collision
      self.obstacles = obstacles
      
    def input(self):
        if INPUTS['up']:
            self.direction.y = -1
        elif INPUTS['down']:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if INPUTS['left']:
            self.direction.x = -1
        elif INPUTS['right']:
            self.direction.x = 1
        else:
            self.direction.x = 0
    
    def window_collision(self, direction):
        if direction == DIRECTION[0]:
            if self.rect.left <= 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1     
            if self.rect.right >= WIDTH:
                self.rect.right =  WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
                
        if direction == DIRECTION[1]:
            if self.rect.top <= 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1   
                  
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom =  HEIGHT
                self.pos.y = self.rect.y
                self.direction.y *= -1       
       
    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:
            if direction == DIRECTION[0]:
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                    
            if direction == DIRECTION[1]:
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.bottom:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                    # collision on the bottom
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()        
            
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision(DIRECTION[0])
        self.window_collision(DIRECTION[0])
        
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision(DIRECTION[1])
        self.window_collision(DIRECTION[1])
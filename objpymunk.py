import pygame, pymunk
from settings import *

class Ball():
    def __init__(self, space, pos, radius= 32, size =(32, 32)) -> None:
        # pymunk
        self.space = space 
        self.body = pymunk.Body()
        self.body.position = pos
        self.radius = radius 
         
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color =(255, 0, 0, 100)
        self.shape.mass = 10
        self.shape.elasticity = 0.9
        self.shape.friction = 0.8
        self.space.add(self.body, self.shape)

           
class Floor():
    def __init__(self, space, pos, size =(32, 32)) -> None:
        # pymunk
        self.space = space 
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.size = size
                     
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.color = (255, 255, 255, 100)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        self.space.add(self.body, self.shape)
   
   
class Ship(pygame.sprite.Sprite):
    def __init__(self, space, groups, image, pos, size =(16, 16)) -> None:
        super().__init__(groups)
        # pymunk
        self.pos = pymunk.vec2d.Vec2d(pos[0], pos[1])
        self.body = pymunk.body.Body()
        self.body.position = self.pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.color = (255, 255, 255, 100)
        self.shape.mass = 10
        self.shape.elasticity = 0.9
        self.shape.friction = 0.8
        space.add(self.body, self.shape)
        
        # pygame
        self.image = image
        self.rect = image.get_rect(center = pos)
        
        
    def update(self,dt):
        x, y = round(self.shape.body.position.x), round(self.shape.body.position.y)
        self.rect.centerx = x
        self.rect.centery = y 
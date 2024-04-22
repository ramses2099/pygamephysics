import pygame, sys, os
import pymunk.pygame_util
from settings import *
# from objects import *
from objpymunk import *

class Game:
    def __init__(self):
      pygame.init()
      self.clock = pygame.time.Clock()
      self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
      pygame.display.set_caption(TITLE)
      self.font = pygame.font.Font(FONT, TITLESIZE)
      self.running = True
      
      # pymunk word
      self.space = pymunk.Space()
      self.space.gravity =0, 981
      self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
      
      # pymunk object
      self.ball = Ball(self.space,(50, 50), 25)     
      self.floor = Floor(self.space,(WIDTH/2, HEIGHT),(WIDTH,32))
      
      self.all_sprites = pygame.sprite.Group()
      self.ship = Ship(self.space, self.all_sprites, IMAGE_SHIP,(WIDTH/2,50))
      self.ball = Ball(self.space,(WIDTH/2, 450), 25)
      
    #   self.all_sprites = pygame.sprite.Group()
    #   self.collision_sprite = pygame.sprite.Group()
    #   self.st_obj1 = StaticObstacle((100, 300),(100, 50),[self.all_sprites, self.collision_sprite])
    #   self.st_obj2 = StaticObstacle((800, 600),(100, 50),[self.all_sprites, self.collision_sprite])
    #   self.st_obj3 = StaticObstacle((900, 200),(100, 50),[self.all_sprites, self.collision_sprite])
    #   self.mv_obj1 = MovingVerticalObstacle((200, 300),(200, 60),[self.all_sprites, self.collision_sprite])
    #   self.mv_obj2 = MovingHorizontalObstacle((850, 350),(100, 100),[self.all_sprites, self.collision_sprite])
    #   self.player = Player(self.all_sprites, self.collision_sprite)
    #   self.ball = Ball(self.all_sprites, self.collision_sprite, self.player)
      
    def debugger(self, debug_list):
        for idx, name in enumerate(debug_list):
            self.render_text(name, COLORS['white'], self.font, (10, 15 * idx), False)
          
    def custom_cursor(self):
        pygame.mouse.set_visible(False)
        curs_image = pygame.image.load('./assets/images/crosshair182.png').convert_alpha()
        curs_image = pygame.transform.scale(curs_image,(32,32))
        curs_rect = curs_image.get_frect(center=pygame.mouse.get_pos())
        curs_image.set_alpha(150)
        self.screen.blit(curs_image, curs_rect)        
          
    def render_text(self, text, color, font, pos, centrilised=True):
        surf = font.render(str(text), False, color)
        rect = None 
        if centrilised:
            rect = surf.get_rect(center = pos)
        else:
            rect = surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)
    
    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images
    
    def get_animatinos(self, path):
        animation = {}
        for file_name in os.listdir(path):
            animation.update({file_name:[]})
        return animation
             
    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    INPUTS['space'] = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS['left'] = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS['right'] = True
                elif event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS['up'] = True
                elif event.key in (pygame.K_DOWN, pygame.K_x):
                    INPUTS['down'] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    INPUTS['space'] = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS['left'] = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS['right'] = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS['up'] = False
                elif event.key in (pygame.K_DOWN, pygame.K_x):
                    INPUTS['down'] = False 
      
    def loop(self):
        while self.running:
            self.screen.fill(COLORS['black'])
            dt = self.clock.tick(FPS)/1000
            self.get_inputs()
            # state machine
            # update
            
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            
                       
            
            # draw
            self.debugger([
                str(f'FPS: {round(self.clock.get_fps(), 2)}'),
            ])
            
            #
            # self.custom_cursor() 
            
            # pymunk debug
            self.space.debug_draw(self.draw_options)
            #
            pygame.display.flip()
            # pymunk update world
            
            self.space.step(dt)


if __name__ == "__main__":
    Game().loop()
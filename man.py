import pygame, sys, os
from settings import *

class Game:
    def __init__(self):
      pygame.init()
      self.clock = pygame.time.Clock()
      self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
      pygame.display.set_caption(TITLE)
      self.font = pygame.font.Font(FONT, TITLESIZE)
      self.running = True
      
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
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    INPUTS['space'] = False   
      
    def loop(self):
        while self.running:
            self.screen.fill(COLORS['black'])
            dt = self.clock.tick(FPS)/1000
            self.get_inputs()
            # state machine
            # update
            
            # draw
            self.debugger([
                str(f'FPS: {round(self.clock.get_fps(), 2)}'),
            ])
            
            #
            self.custom_cursor() 
            #
            pygame.display.flip()


if __name__ == "__main__":
    Game().loop()
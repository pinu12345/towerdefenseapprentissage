import sys, os, pygame

class Menu():
    def __init__(self):
        self.btnGrid = GridButton(850,250)
        self.btnStart = StartButton(850,300)
        self.btnExit = ExitButton(850,350)
        self.menu = pygame.sprite.Group(self.btnGrid, self.btnStart, self.btnExit)

    def draw(self, screen):
        self.menu.draw(screen)

    def onClick(self, pos, map):
        if self.btnGrid.rect.collidepoint(pos):
            if map.showGrid == 1:
                map.showGrid = 0
            else:
                map.showGrid = 1

        if self.btnStart.rect.collidepoint(pos):
            pass

        if self.btnExit.rect.collidepoint(pos):
            pygame.quit()

class GridButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images', 'ok.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class StartButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images', 'ok.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ExitButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images', 'ok.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
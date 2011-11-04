import pygame, os, Images
from Global import *

def init():

    # Master SpriteSheet
    Images.spriteSheet = pygame.image.load(os.path.join ('Images', 'Spritesheet32.png')).convert()
    
    # Enemy Images
    Images.EnemyImages = []
    for i in range(len(enemyOffsets)):
        tmpImg = pygame.Surface((tileSize, tileSize))
        tmpImg.blit(Images.spriteSheet, (0, 0), (enemyOffsets[i], (tileSize, tileSize)))
        Images.EnemyImages.append(tmpImg)

    # Tower Images
    Images.TowerImages = \
        [[pygame.image.load(os.path.join ('Images\Towers', '1 - 0.png')).convert(),
          pygame.image.load(os.path.join ('Images\Towers', '1 - 1.png')).convert(),
          pygame.image.load(os.path.join ('Images\Towers', '1 - 2.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '2 - 0.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '3 - 0.png')).convert(), pygame.image.load(os.path.join ('Images\Towers', '2 - 1.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '4 - 0.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '5 - 0.png')).convert()]]

    Images.Background = pygame.image.load(os.path.join ('Images\Menu', 'background.jpg')).convert()
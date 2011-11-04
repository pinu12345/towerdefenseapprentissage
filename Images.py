import pygame, os, Images
from Global import *

def init():

    # Master SpriteSheet
    Images.spriteSheet = pygame.image.load(os.path.join ('Images', 'Spritesheet32.png')).convert()
    
    # Enemy Images
    Images.EnemyImages = []
    for i in range(len(enemyOffsets)):
        tmpImg = pygame.Surface((tileSize, tileSize))
        tmpImg.set_colorkey(spritepink)
        tmpImg.blit(Images.spriteSheet, (0, 0), (enemyOffsets[i], (tileSize, tileSize)))
        Images.EnemyImages.append(tmpImg)

    # Tower Images
    Images.TowerImages = []
    for i in range(len(towerOffsets)):
        Images.TowerImages.append([])
        for j in range(len(towerOffsets[i])):
            tmpImg = pygame.Surface((tileSize, tileSize))
            tmpImg.set_colorkey(spritepink)
            tmpImg.blit(Images.spriteSheet, (0, 0), (towerOffsets[i][j], (tileSize, tileSize)))
            Images.TowerImages[i].append(tmpImg)
        #[[pygame.image.load(os.path.join ('Images\Towers', '1 - 0.png')).convert(),
        #  pygame.image.load(os.path.join ('Images\Towers', '1 - 1.png')).convert(),
        #  pygame.image.load(os.path.join ('Images\Towers', '1 - 2.png')).convert()],
        #[pygame.image.load(os.path.join ('Images\Towers', '2 - 0.png')).convert()],
        #[pygame.image.load(os.path.join ('Images\Towers', '3 - 0.png')).convert(), pygame.image.load(os.path.join ('Images\Towers', '2 - 1.png')).convert()],
        #[pygame.image.load(os.path.join ('Images\Towers', '4 - 0.png')).convert()],
        #[pygame.image.load(os.path.join ('Images\Towers', '5 - 0.png')).convert()]]

    Images.Background = pygame.image.load(os.path.join ('Images\Menu', 'background.jpg')).convert()
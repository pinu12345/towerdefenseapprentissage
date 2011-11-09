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

    # Map Images
    Images.MapImages = []
    for i in range(len(mapOffsets)):
        Images.MapImages.append([])
        for j in range(len(mapOffsets[i])):
            tmpImg = pygame.Surface((tileSize, tileSize))
            tmpImg.set_colorkey(spritepink)
            tmpImg.blit(Images.spriteSheet, (0, 0), (mapOffsets[i][j], (tileSize, tileSize)))
            Images.MapImages[i].append(tmpImg)
    
    # Titre
    Images.Background = pygame.image.load(os.path.join ('Images\Menu', 'title.png')).convert()
    
    # Fond d'interface
    Images.InterfaceBG = pygame.image.load(os.path.join ('Images\Interface', 'bg_delave.png')).convert()
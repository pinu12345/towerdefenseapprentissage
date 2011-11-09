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
    
    # Interface
    Images.InterfaceBGwashed = pygame.image.load(os.path.join ('Images\Interface', 'bg_washed.png')).convert()
    Images.InterfaceBGopaque = pygame.image.load(os.path.join ('Images\Interface', 'bg_opaque.png')).convert()
    Images.InterfaceBGbright = pygame.image.load(os.path.join ('Images\Interface', 'bg_bright.png')).convert()
    Images.InterfaceL1 = pygame.image.load(os.path.join ('Images\Interface', 'lv1.png')).convert()
    Images.InterfaceL2 = pygame.image.load(os.path.join ('Images\Interface', 'lv2.png')).convert()
    Images.InterfaceL3 = pygame.image.load(os.path.join ('Images\Interface', 'lv3.png')).convert()
    Images.InterfaceDI = pygame.image.load(os.path.join ('Images\Interface', 'def_inf.png')).convert()
    Images.InterfaceDA = pygame.image.load(os.path.join ('Images\Interface', 'def_arm.png')).convert()
    Images.InterfaceDS = pygame.image.load(os.path.join ('Images\Interface', 'def_shi.png')).convert()
    
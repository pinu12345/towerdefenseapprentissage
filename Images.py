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

    # Radio splash
    # Niveau 1: 128x128
    Images.RS1 = pygame.image.load(os.path.join ('Images\Towers', 'RadioSplash1.png')).convert()
    # Niveau 2: 160x160
    Images.RS2 = pygame.image.load(os.path.join ('Images\Towers', 'RadioSplash2.png')).convert()
    # Niveau 3: 192x192
    Images.RS3 = pygame.image.load(os.path.join ('Images\Towers', 'RadioSplash3.png')).convert()
    
            
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
    Images.InterfaceLevels = [pygame.image.load(os.path.join ('Images\Interface', 'lv1.png')).convert(),
                              pygame.image.load(os.path.join ('Images\Interface', 'lv2.png')).convert(),
                              pygame.image.load(os.path.join ('Images\Interface', 'lv3.png')).convert()]
    for i in range(len(Images.InterfaceLevels)):
        Images.InterfaceLevels[i].set_colorkey(spritepink)
    Images.InterfaceType = [pygame.image.load(os.path.join ('Images\Interface', 'def_inf.png')).convert(),
                            pygame.image.load(os.path.join ('Images\Interface', 'def_arm.png')).convert(),
                            pygame.image.load(os.path.join ('Images\Interface', 'def_shi.png')).convert()]
    for i in range(len(Images.InterfaceType)):
        Images.InterfaceType[i].set_colorkey(spritepink)
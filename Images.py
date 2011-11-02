import pygame, os, Images

def init():
    # Enemy Images
    Images.EnemyImages = \
        [pygame.image.load(os.path.join ('Images\Enemies', '0.png')).convert(),
        #[pygame.image.load(os.path.join ('Images\Enemies', '0.png')),
        #pygame.image.load(os.path.join ('Images\Enemies', '1.png')),
        #pygame.image.load(os.path.join ('Images\Enemies', '2.png')),
        #pygame.image.load(os.path.join ('Images\Enemies', '3.png')),
        #pygame.image.load(os.path.join ('Images\Enemies', '4.png'))]
        pygame.image.load(os.path.join ('Images\Enemies', '1.png')).convert(),
        pygame.image.load(os.path.join ('Images\Enemies', '2.png')).convert(),
        pygame.image.load(os.path.join ('Images\Enemies', '3.png')).convert(),
        pygame.image.load(os.path.join ('Images\Enemies', '4.png')).convert()]

    Images.TowerImages = \
        [[pygame.image.load(os.path.join ('Images\Towers', '1 - 0.png')).convert(), pygame.image.load(os.path.join ('Images\Towers', '1 - 1.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '2 - 0.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '3 - 0.png')).convert(), pygame.image.load(os.path.join ('Images\Towers', '2 - 1.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '4 - 0.png')).convert()],
        [pygame.image.load(os.path.join ('Images\Towers', '5 - 0.png')).convert()]]

    Images.Background = pygame.image.load(os.path.join ('Images\Menu', 'background.jpg')).convert()
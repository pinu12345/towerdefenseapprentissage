import sys, os, pygame, Enemy

class Wave():
    def __init__(self):
        self.tileSize = 33
        self.enemyb = Enemy.Enemy(0, self, 0, 0)
        self.enemya = Enemy.Enemy(1, self, 0, 1)
        self.enemyc = Enemy.Enemy(2, self, 0, 2)
        self.enemyd = Enemy.Enemy(3, self, 0, 3)
        self.enemye = Enemy.Enemy(4, self, 0, 4)
        self.enemyf = Enemy.Enemy(0, self, 0, 5)
        self.enemyg = Enemy.Enemy(1, self, 0, 6)
        self.enemyh = Enemy.Enemy(2, self, 0, 7)
        self.enemyi = Enemy.Enemy(3, self, 0, 8)
        self.enemyj = Enemy.Enemy(4, self, 0, 9)
        self.enemyk = Enemy.Enemy(0, self, 0, 10)
        self.enemyl = Enemy.Enemy(1, self, 0, 11)
        self.enemym = Enemy.Enemy(2, self, 0, 12)
        self.enemyn = Enemy.Enemy(3, self, 0, 13)
        self.enemyo = Enemy.Enemy(4, self, 0, 14)
        self.enemies = pygame.sprite.Group(self.enemya,
            self.enemyb,
            self.enemyc,
            self.enemyd,
            self.enemye,
            self.enemyf,
            self.enemyg,
            self.enemyh,
            self.enemyi,
            self.enemyj,
            self.enemyk,
            self.enemyl,
            self.enemym,
            self.enemyn,
            self.enemyo)

    def draw(self, screen):
        #Move the enemies
        for enemy in self.enemies:
            enemy.move(1,1)
        #Draw their new positions
        self.enemies.draw(screen)
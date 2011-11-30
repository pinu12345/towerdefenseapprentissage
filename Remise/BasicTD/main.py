import pygame, enemySprites, mapbuilder, towerSprites
from startup import *
pygame.mixer.init()

def main():
    """Main program, where everything is started."""
    pygame.init()

    #Sounds
    pygame.mixer.stop()
    backSound = pygame.mixer.Sound(os.path.join ('data', 'hifi.ogg'))
    backSound2 = pygame.mixer.Sound(os.path.join ('data', 'crim.ogg'))
    backSound.set_volume(1)
##    backSound2.set_volume(1)
    shootSound = pygame.mixer.Sound(os.path.join ('data', 'gun.ogg'))
    shootSound.set_volume(0.3)

    backSound.play(-1) # loop the background music

    se = 0

    #Menu building
    button1 = MapChoice(75,100,0)
    button2 = MapChoice(325,100,1)
    button3 = ModeButton (200,350,0)
    button4 = OkButton (470,350)

    #Map building
    mapType = 'empty'
    mapS = mapbuilder.Map(mapType, background)
    mapS.buildMap()

    mode = 'easy'
    cont = 0
    towerselected = None

    #Sets all important variables
    clock = pygame.time.Clock()
    noQuit = True
    noUnderQuit = True

    #Tower Costs
    t1cost = 50
    t2cost = 75
    t3cost = 125

    #Tower Icons
    icon1 = towerSprites.TIcons(695, 175, 1)
    icon2 = towerSprites.TIcons(725, 175, 2)
    icon3 = towerSprites.TIcons(755, 175, 3)

    #Setting Sprite Groups
    others = pygame.sprite.Group(button1,button2,button3,button4)
    icons = pygame.sprite.Group(icon1,icon2,icon3)

    lives = 20
    money = 150
    score = 0

    countdown = 10 #10 frames between each enemy sending
    cntDwn = countdown
    eType = 'normal'
    nextWavePrep = 0
    count = 0
    targetlines = 1
    waveWait = True
    youwin = 0
    winCount = 1

    while noQuit:
        clock.tick(30)
        while noUnderQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    noUnderQuit = False
                    noQuit = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    noUnderQuit = False
                    noQuit = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.rect.collidepoint(pygame.mouse.get_pos()):
                        button1.change()
                        mapType = 'easy'
                        if button2.selected == 1:
                            button2.selected = 0
                            button2.change()
                    if button2.rect.collidepoint(pygame.mouse.get_pos()):
                        button2.change()
                        mapType = 'hard'
                        if button1.selected == 1:
                            button1.selected = 0
                            button1.change()
                    if button3.rect.collidepoint(pygame.mouse.get_pos()):
                        button3.change()
                        if mode == 'easy':
                            mode = 'hard'
                            winCount = 3
                        else:
                            mode = 'easy'
                            winCount = 1
                    if button4.rect.collidepoint(pygame.mouse.get_pos()):
                        if mapType != 'empty':
                            cont = 1
                            noUnderQuit = False

            others.clear(screen, background)
            mapS.buildMap()
            pygame.draw.rect(screen, (51,117,20),(60,85,505,300))
            others.draw(screen)
            pygame.display.flip()

        if cont == 1:
            others.clear(screen, background)

            map = mapbuilder.Map(mapType, background)
            map.buildMap()
            waypoints = map.checkWaypoints()

            #set up the grid
            grid = mapbuilder.GridControl(mapType, screen, map.getGrid())

            noUnderQuit = True

        while noUnderQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    noQuit = False
                    noUnderQuit = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    noQuit = False
                    noUnderQuit = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r: #restarts the game
                    del baddieList[:]
                    del towerList[:]
                    baddies.empty()
                    towers.empty()
                    player.money = player.BASECASH
                    player.score = 0
                    player.health = player.BASEHP
                    player.wave = 0
                    player.enemyCount = 0
                    main()

##                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
##                    enemySprites.HardEnemy(player.wave, map.checkWaypoints(), mode)
##                if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
##                    enemySprites.NormalEnemy(player.wave, map.checkWaypoints(), mode)
##                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
##                    enemySprites.WeakEnemy(player.wave, map.checkWaypoints(), mode)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x,m_y = pygame.mouse.get_pos()
                    if m_x < 625:
                        grid.click()
                    else:
                        grid.unclick()
                    info.unClick()
                    twrSurf.fill((255,0,255))
                    for tower in towerList:
                        if tower.rect.collidepoint(pygame.mouse.get_pos()):
                            towerselected = tower
                            pygame.draw.circle(twrSurf,(153,204,255),towerselected.rect.center,towerselected.range,towerselected.range)
                            info.setInfo(towerselected.damage,towerselected.range,towerselected.upcost,towerselected.level,towerselected.type)

                    if icon1.rect.collidepoint(pygame.mouse.get_pos()):
                        if grid.checkTower() == 'No':
                            if player.money >= t1cost:
                                towers.add(towerSprites.Tower(grid.setTower(),1))
                                player.money -= t1cost

                    if icon2.rect.collidepoint(pygame.mouse.get_pos()):
                        if grid.checkTower() == 'No':
                            if player.money >= t2cost:
                                towers.add(towerSprites.Tower(grid.setTower(),2))
                                player.money -= t2cost

                    if icon3.rect.collidepoint(pygame.mouse.get_pos()):
                        if grid.checkTower() == 'No':
                            if player.money >= t3cost:
                                towers.add(towerSprites.Tower(grid.setTower(),3))
                                player.money -= t3cost

                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    if towerselected != None:
                        if towerselected.upcost <= player.money:
                            player.money -= towerselected.upcost
                            towerselected.upgrade()
                            info.setInfo(towerselected.damage,towerselected.range,towerselected.upcost,towerselected.level,towerselected.type)
                            pygame.draw.circle(twrSurf,(153,204,255),towerselected.rect.center,towerselected.range,towerselected.range)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if waveWait == True:
                        waveWait = False
                        if player.wave <= 4:
                            player.wave +=1

##                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
##                    if grid.checkTower() == 'No':
##                        towers.add(towerSprites.Tower(grid.setTower(),1))
##                    twrSurf.fill((255,0,255))
##                    for tower in towerList:
##                        if tower.rect.collidepoint(pygame.mouse.get_pos()):
##                            towerselected = tower
##                            pygame.draw.circle(twrSurf,(153,204,255),towerselected.rect.center,towerselected.range,towerselected.range)
##                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
##                    if grid.checkTower() == 'No':
##                        towers.add(towerSprites.Tower(grid.setTower(),2))
##                    twrSurf.fill((255,0,255))
##                    for tower in towerList:
##                        if tower.rect.collidepoint(pygame.mouse.get_pos()):
##                            towerselected = tower
##                            pygame.draw.circle(twrSurf,(153,204,255),towerselected.rect.center,towerselected.range,towerselected.range)
##                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
##                    if grid.checkTower() == 'No':
##                        towers.add(towerSprites.Tower(grid.setTower(),3))
##                    twrSurf.fill((255,0,255))
##                    for tower in towerList:
##                        if tower.rect.collidepoint(pygame.mouse.get_pos()):
##                            towerselected = tower
##                            pygame.draw.circle(twrSurf,(153,204,255),towerselected.rect.center,towerselected.range,towerselected.range)


            if player.wave <= 5:
                if nextWavePrep == 1:
                    if eType == 'weak':
                        eType = 'normal'
                        nextWavePrep = 0
                        count = 0
                        waveWait = True
                        cntDwn = 10
                    else:
                        eType = 'weak'
                        nextWavePrep = 0
                        count = 0
                        waveWait = True
                        cntDwn = 5

            if player.wave == 5 and se == 0:
                countdown = 300
                pygame.mixer.stop()
                backSound2.play(-1)
                se = 1
            #Wave Sending Code
            if player.health > 0:
                if waveWait == True:
                    i = 1
                else:
                    if player.wave == 5:
                        if countdown == 0:
                            if count < winCount:
                                enemySprites.HardEnemy(player.wave, map.checkWaypoints(), mode)
                                count +=1
                                countdown = 50

                            if (winCount == count) and (player.enemyCount == 0):
                                youwin = 1
                        else:
                            countdown -=1

                    else:
                        if countdown == 0:
                            if eType == 'weak':
                                if count <= player.wave*3 + 10:
                                    enemySprites.WeakEnemy(player.wave, map.checkWaypoints(), mode)
                                    count +=1
                                if player.enemyCount == 0:
                                    nextWavePrep = 1
                            else:
                                if count <= player.wave*3 + 5:
                                    enemySprites.NormalEnemy(player.wave, map.checkWaypoints(), mode)
                                    count +=1
                                if player.enemyCount == 0:
                                    nextWavePrep = 1
                            countdown = cntDwn
                        else:
                            countdown -= 1

            else:
                youwin = 2
                #player Loses The Game

            baddies.clear(screen, background)
            towers.clear(screen, background)
            icons.clear(screen, background)


            baddies.update()
            towers.update()

            map.buildMap()

            others.update()
            icons.update()

            screen.blit(twrSurf,(0,0))

            icons.draw(screen)
            towers.draw(screen)


            #Tower Shooting Code
            for tower in towerList:
                if tower.reloadNum >= tower.reload:
                    enemypoint = tower.target()
                    if enemypoint: #Returns true if an enemy's in range
                        tower.reloadNum = 0
                    if (enemypoint != None): #and targetlines:
                        if tower.type == 1:
                            pygame.draw.line(screen,(255,255,255), tower.rect.center,enemypoint,2)
                        if tower.type == 2:
                            pygame.draw.line(screen,(0,0,0), tower.rect.center,enemypoint,5)
                        if tower.type == 3:
                            pygame.draw.line(screen,(255,255,255), tower.rect.center,enemypoint,1)
                        shootSound.play()
                else:
                    tower.reloadNum += 1

            baddies.draw(screen)

            #For drawing the enemy healthbar
            for enemy in baddieList:
                pygame.draw.line(screen, (0,0,0), (enemy.rect.left,enemy.rect.top-2),\
                    (enemy.rect.right,enemy.rect.top-2), 3)
                pygame.draw.line(screen, (255,0,0), (enemy.rect.left,enemy.rect.top-2),\
                    (enemy.rect.left+(enemy.health*1.0/enemy.starthealth*1.0)\
                    *enemy.rect.width,enemy.rect.top-2), 3)

            screen.blit(grid.surf,(grid.m_x,grid.m_y))
            drawText()
            info.drawInfo()
            if player.wave == 5:
                screen.blit(drkSurf,(0,0))

            if waveWait == True:
                pygame.draw.rect(screen,(50,50,50),(0,625-40,625,40))
                to1Font = pygame.font.SysFont("None", 30)
                spaceTxt = to1Font.render("Press Space to Start Next Wave",1,(255,255,255))
                screen.blit(spaceTxt,(200,625-25))

            if youwin == 1:
                pygame.draw.rect(screen,(51,117,20),(200,200,210,98))
                to1Font = pygame.font.SysFont("None", 30)
                spaceTxt = to1Font.render("You Win!",1,(255,255,255))
                scoreTxt = to1Font.render("Final Score: %d"% player.score,1,(255,255,255))
                restText = to1Font.render("To restart, press R",1,(255,255,255))
                screen.blit(spaceTxt,(255,213))
                screen.blit(scoreTxt,(213,213+30))
                screen.blit(restText,(213,213+60))
            if youwin == 2:
                pygame.draw.rect(screen,(51,117,20),(200,200,210,98))
                to1Font = pygame.font.SysFont("None", 30)
                spaceTxt = to1Font.render("You Lose!",1,(255,255,255))
                scoreTxt = to1Font.render("Final Score: %d"% player.score,1,(255,255,255))
                restText = to1Font.render("To restart, press R",1,(255,255,255))
                screen.blit(spaceTxt,(255,213))
                screen.blit(scoreTxt,(213,213+30))
                screen.blit(restText,(213,213+60))

            pygame.display.flip()

            m__x,m__y = pygame.mouse.get_pos()
            pygame.display.set_caption(str(m__x) + " , " +str(m__y))

    pygame.quit()

if __name__ == "__main__":
    main()

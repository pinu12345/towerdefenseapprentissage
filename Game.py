import sys, os, pygame, Map, Menu, TowerBar, Wave, Towers, Shot, Global, Game, Images, Level
import pygame.examples.aliens
from Global import *
from MainMenu import *
from Shots import *

def main():
    # Initialize pygame
    # os.environ['SDL_VIDEODRIVER'] = 'windib'
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    os.environ['SDL_VIDEO_CENTERED'] = '1'#
    
    Game.framesPerSecond = 48
    Game.speedModifier = 1
    Game.autoMode = 0
    Game.balanceMode = 0
    
    drawTick = 0
    Game.state = STATE_INITMENU

    # Set the height and width of the screen
    size = [mapWidth*(tileSize+1) + rightMenuSize, mapHeight*(tileSize+1) + bottomMenuSize]
    screen = pygame.display.set_mode(size)
    screen.fill(background)
    layer = pygame.Surface(size)
    layer.set_colorkey(spritepink)
    layer.set_alpha(120)
    
    # Variables to tell Game what to draw
    Game.drawMouseOver = 0
    Game.drawMessage = 0
    Game.repaintMap = 0
    Game.placedTower = 0

    # Initialize the MainMenu
    mainMenu = cMenu(128, 320, 20, 5, 'vertical', 100, screen,
               [('Start Automatic Tests', 1, None),
                ('Start Basic Map', 2, None),
                ('Start Map 1', 3, None),
                ('Start Map 2', 4, None),
                ('Start Map 3', 5, None),
                ('Start Test Map', 6, None),
                ('Start Balance Tests', 7, None),
                ('Exit', 8, None)])
    gameMenu = cMenu(128, 320, 20, 5, 'vertical', 100, screen,
               [('Resume', 1, None),
                ('Back to main menu (current progress will be lost!)', 2, None)])
    Images.init()

    menubackground = Images.Background
    interfaceBGwashed = Images.InterfaceBGwashed
    InterfaceBGopaque = Images.InterfaceBGopaque
    rect_list = []

    # Initialize the map
    map = Map.Map(mapWidth,mapHeight)
    
    # Initialize the wave
    wave = Wave.Wave(map)
    
    # Initialize the Towers class
    towers = Towers.Towers(map, wave)
    wave.setTowers(towers)
    
    # Initialize the shot graphics
    shots = Shots()

    # Initialize the tower bar
    towerBar = TowerBar.TowerBar(0, mapHeight*tileSize)

    # Initialize the menu
    menu = Menu.Menu(map, wave, towers)

    # Initialize the level
    Game.level = Level.Level(map, wave, towers, towerBar, menu)

    # Set title of screen
    pygame.display.set_caption("AI Tower Defense -- (c) POB & ND")

    #Loop until the user clicks the close button.
    close_game = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while close_game == False:
        
        ## Init menu
        if Game.state == STATE_INITMENU:
            screen.fill(background)
            screen.blit(menubackground, (0, 0))
            pygame.display.flip()
            mainMenustate = 0
            mainMenuprev_state = 1
            Game.state = STATE_MENU
        
        ## Menu
        elif Game.state == STATE_MENU:
            if mainMenuprev_state != mainMenustate:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                mainMenuprev_state = mainMenustate
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                if mainMenustate == 0:
                    rect_list, mainMenustate = mainMenu.update(e, mainMenustate)
                elif mainMenustate == 1:
                    Game.state = STATE_LOADGAME
                    Game.autoMode = 1
                    Game.level.autoWave()
                elif mainMenustate == 2:
                    map.loadFileMap('basicmap')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 3:
                    map.loadFileMap('map1')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 4:
                    map.loadFileMap('map2')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 5:
                    Game.level.loadLevel('map3')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 6:
                    map.loadFileMap('testmap')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 7:
                    Game.state = STATE_LOADGAME
                    Game.balanceMode = 1
                    Game.level.balanceWave()
                else:
                    pygame.quit()
                    sys.exit()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update(rect_list)

        ## Init Game Menu
        elif Game.state == STATE_INITGAMEMENU:
            screen.fill(background)
            screen.blit(menubackground, (0, 0))
            pygame.display.flip()
            gameMenustate = 0
            gameMenuprev_state = 1
            Game.state = STATE_GAMEMENU
        
        ## Game Menu
        elif Game.state == STATE_GAMEMENU:
            if gameMenuprev_state != gameMenustate:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                gameMenuprev_state = gameMenustate
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                if e.key == pygame.K_ESCAPE:
                    Game.state = STATE_LOADGAME
                else:
                    if gameMenustate == 0:
                        rect_list, gameMenustate = gameMenu.update(e, gameMenustate)
                    elif gameMenustate == 1:
                        Game.state = STATE_LOADGAME
                    elif gameMenustate == 2:
                        shots.clear()
                        towers.clear()
                        wave.clear()
                        Game.state = STATE_INITMENU
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update(rect_list)
        
        else:
            for event in pygame.event.get(): # User did something
                # If user clicked close
                if event.type == pygame.QUIT: 
                    close_game = True # Flag that we are done so we exit this loop

                ## Mouse Events
                # User moves over the mouse 
                elif event.type == pygame.MOUSEMOTION:
                    Game.drawMouseOver = 0
                    if towerBar.selectedTower > -1:
                        pos = pygame.mouse.get_pos()                
                        column = pos[0] // tileSize
                        row = pos[1] // tileSize
                        # Inside Map
                        if (column < mapWidth) and (row < mapHeight):
                            map.O[map.currentOY][map.currentOX] = 0
                            if (map.M[row][column] == car_turret) and (map.T[row][column] == 0):
                                map.currentOY = row
                                map.currentOX = column
                                map.O[row][column] = towerBar.selectedTower
                                Game.drawMouseOver = 1

                # User clicks the mouse. Get the position
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Change the x/y screen coordinates to grid coordinates (For the map)
                    column = pos[0] // tileSize
                    row = pos[1] // tileSize

                    # Inside Map
                    if (column < mapWidth) and (row < mapHeight):
                        if towerBar.selectedTower > -1:
                            if map.M[row][column] == car_turret:
                                if map.T[row][column] == 0:
                                    #TODO : money check
                                    towers.placeTower(map, towerBar.selectedTower, 0, row, column)
                                    Game.placedTower = 1
                                else:
                                    towers.updateTower(map, towerBar.selectedTower, 0, row, column)
                                    Game.placedTower = 1

                    # Inside Menu
                    elif column >= mapWidth:
                        menu.onClick(pos, map)

                    # Inside Tower Bar
                    else:
                        towerBar.onClick(pos)
                
                ## Keyboard Events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.state = STATE_INITGAMEMENU
                    elif event.key == pygame.K_SPACE:
                        if Game.state == STATE_GAME:
                            Game.state = STATE_PREPARATION
                        elif Game.state == STATE_PREPARATION: 
                            Game.state = STATE_GAME
                    elif event.key == pygame.K_1:
                        towerBar.selectTower(0)
                    elif event.key == pygame.K_2:
                        towerBar.selectTower(1)
                    elif event.key == pygame.K_3:
                        towerBar.selectTower(2)
                    elif event.key == pygame.K_4:
                        towerBar.selectTower(3)
                    elif event.key == pygame.K_5:
                        towerBar.selectTower(4)
                    elif event.key == pygame.K_6:
                        towerBar.selectTower(5)
                    elif event.key == pygame.K_EQUALS:
                        if Game.speedModifier <= 25.0:
                            Game.speedModifier *= 5
                    elif event.key == pygame.K_MINUS:
                        if Game.speedModifier >= 0.2:
                            Game.speedModifier /= 5
                    elif event.key == pygame.K_c:
                        towers.resetCooldowns()
                    elif event.key == pygame.K_r:
                        towerBar.selectTower(-2)
                    elif event.key == pygame.K_e:
                        towerBar.selectTower(-3)
                    elif event.key == pygame.K_a:
                        towers.clear()
                        wave.clear()
                        shots.clear()
                    elif event.key == pygame.K_t:
                        towers.clear()
                        shots.clear()
            
            ## Init Game
            if Game.state == STATE_LOADGAME:
                screen.blit(InterfaceBGopaque, (0, 0))
                #screen.fill(background)
                #pygame.draw.rect(screen, background, ([mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize]))
                #pygame.draw.rect(screen, background, ([0, mapHeight*tileSize, mapWidth*tileSize, bottomMenuSize]))
                
                # Draw the map
                drawMap(map, screen)
                # Draw the game information menu
                menu.draw(screen)
                # Draw the tower bar ~ 0
                towerBar.draw(screen)
                
                Game.state = STATE_PREPARATION
                pygame.display.flip()
            
            ## Game Paused
            elif Game.state == STATE_PREPARATION:
                if Game.autoMode or Game.balanceMode:
                    Game.state = STATE_GAME
                else:
                    ## Display
                    drawTick += 1
                    #print(clock.get_fps())
                    if drawTick >= clock.get_fps()/24:
                        #print(clock.get_fps())
                        drawTick = 0
                        drawGame(map, towerBar, towers, wave, shots, menu, screen, layer)
                    
            ## Game Running
            elif Game.state == STATE_GAME:
                # Spawn any new enemy in the wave queue
                wave.spawn()
                # Move the enemies
                wave.move()
                # Tower target
                towers.target(shots)

                ## Display
                if not Game.autoMode and not Game.balanceMode:
                    drawTick += 1
                    #print(clock.get_fps())
                    if drawTick >= clock.get_fps()/24:
                        #print(clock.get_fps())
                        drawTick = 0
                        drawGame(map, towerBar, towers, wave, shots, menu, screen, layer)

        #Limit to 24 frames per second
        #print(pygame.time.get_ticks())
        clock.tick(Game.framesPerSecond * Game.speedModifier)

    pygame.quit()

def drawGame(map, towerBar, towers, wave, shots, menu, screen, layer):

    # Empty layer 2 (MOUSE OVER WENT OUTSIDE A TURRET SPOT...)
    layer.fill(spritepink)

    #Draw the route
    #drawRoute(map, screen)
    drawMap(map, screen)
    
    # Draw On Mouse Over ~ 0
    if Game.drawMouseOver:
        if towerBar.redraw:
            drawMap(map, screen)
        else:
            drawTowerEmplacements(map, screen)
        drawOnMouseOver(map, towerBar, layer)
        Game.repaintMap = 1
    else:
        if Game.repaintMap:
            #drawMap(map, screen)
            Game.repaintMap = 0

    if Game.placedTower:
        if Game.repaintMap:
            drawMap(map, screen)
            Game.repaintMap = 0
        else:
            drawTowerEmplacements(map, screen)
        Game.placedTower = 0
    
    if Game.drawMessage:
        pass
    
    # Draw the towers
    # IF NEW TOWER...
    towers.draw(screen)

    # Draw the wave
    wave.draw(screen)
    
    # Towers Target
    shots.draw(screen)
    
    # Update the game portion of the screen
    screen.blit(layer, (0, 0), (0, 0, mapWidth*tileSize, mapHeight*tileSize))
    pygame.display.update(0, 0, mapWidth*tileSize, mapHeight*tileSize)
    
    # Update the right menu portion of the screen
    if 0:
        pygame.display.update(mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize)
        
    # Update the towerbar portion of the screen
    if towerBar.redraw:
        towerBar.draw(screen)
        pygame.display.update(0, mapHeight*tileSize, mapWidth*tileSize, bottomMenuSize)

def drawOnMouseOver(map, towerBar, screen):
    # Draw tower on mouse over
    for row in range(mapHeight):
        for column in range(mapWidth):
            if (map.T[row][column] == 0) and (map.O[row][column] > 0):
                ##  vvv  A MODIFER PAR P-O vvv
                TowerLEVEL_TEMP = 0
                ##  ^^^  A MODIFER PAR P-O ^^^
                if TowerStats[towerBar.selectedTower][TowerLEVEL_TEMP][TowerRANGE] == 0:
                    pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), TowerStats[towerBar.selectedTower][TowerLEVEL_TEMP][TowerSPLASH], 0)
                else:
                    pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), 
                    TowerStats[towerBar.selectedTower][TowerLEVEL_TEMP][TowerRANGE], 0)
                pygame.draw.circle(screen, ShotGraphs[towerBar.selectedTower][ShotCOLOR], (tileSize*column+tileSize/2, tileSize*row+tileSize/2), TowerStats[towerBar.selectedTower][TowerLEVEL_TEMP][TowerRANGE] + TowerStats[towerBar.selectedTower][TowerLEVEL_TEMP][TowerSPLASH], tileSize/16)
                screen.blit(Images.TowerImages[towerBar.selectedTower][0], (tileSize*column,tileSize*row), None, 0)

def drawRoute(map, screen):
    for row in range(mapHeight):
        for column in range(mapWidth):
            if map.M[row][column] == car_path:
                    screen.blit(map.S[row][column], (column*tileSize, row*tileSize))
            elif map.M[row][column] == car_base:
                    screen.blit(map.S[row][column], (column*tileSize, row*tileSize))

def drawTowerEmplacements(map, screen):
    for row in range(mapHeight):
        for column in range(mapWidth):
            if map.M[row][column] == car_turret:
                    screen.blit(map.S[row][column], (column*tileSize, row*tileSize))
            if map.M[row][column] == car_base:
                    screen.blit(map.S[row][column], (column*tileSize, row*tileSize))

def drawMap(map, screen):
    # Draw the map
    for row in range(mapHeight):
        for column in range(mapWidth):
             screen.blit(map.S[row][column], (column*tileSize, row*tileSize))

if __name__ == "__main__":
    main()
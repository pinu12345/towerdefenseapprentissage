import sys, os, pygame, Map, Menu, TowerBar, Wave, Towers, Shot, Global, Game, Images
import pygame.examples.aliens
from Global import *
from MainMenu import *
from Shots import *

def main():

    # Initialize pygame
    # os.environ['SDL_VIDEODRIVER'] = 'windib'
    pygame.init()
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    mapWidth = 24
    mapHeight = 16
    tileSize = 32

    cash = 2100
    health = 100
    drawTick = 0
    Game.state = STATE_INITMENU

    # Set the height and width of the screen
    size = [mapWidth*(tileSize+1) + rightMenuSize, mapHeight*(tileSize+1) + bottomMenuSize]
    screen = pygame.display.set_mode(size)
    layer1 = pygame.Surface(size)
    layer2 = pygame.Surface(size)
    layer3 = pygame.Surface(size)
    layer1.set_colorkey(pink)
    layer2.set_colorkey(pink)
    layer3.set_colorkey(pink)
    layer2.set_alpha(150)

    # Initialize the MainMenu
    mainMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
               [('Start Random Map', 1, None),
                ('Start Test Map', 2, None),
                ('Options', 3, None),
                ('Exit', 4, None)])
    gameMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
               [('Resume', 1, None),
                ('Back to main menu', 2, None)])
    mainMenu.set_center(True, True)
    gameMenu.set_center(True, True)
    mainMenu.set_alignment('center', 'center')
    gameMenu.set_alignment('center', 'center')

    Images.init()

    menubackground = Images.Background
    rect_list = []

    # Initialize the map
    map = Map.Map(mapWidth,mapHeight)

    # Initialize the wave
    wave = Wave.Wave(map)
    
    # Initialize the Towers class
    towers = Towers.Towers(map, wave)
    
    # Initialize the shot graphics
    shots = Shots()
    
    # Initialize the tower bar
    towerBar = TowerBar.TowerBar(17, mapHeight*(tileSize+1)+35)

    # Initialize the menu
    menu = Menu.Menu(map, wave, towers)

    # Set title of screen
    pygame.display.set_caption("4D tower defense - (c) POB + ND")

    #Loop until the user clicks the close button.
    close_game = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while close_game == False:
    
        if Game.state == STATE_INITMENU:
            screen.fill(background)
            screen.blit(menubackground, (0, 0))
            pygame.display.flip()
            mainMenustate = 0
            mainMenuprev_state = 1
            Game.state = STATE_MENU
            
        elif Game.state == STATE_MENU:
            if mainMenuprev_state != mainMenustate:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                mainMenuprev_state = mainMenustate
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                if mainMenustate == 0:
                    rect_list, mainMenustate = mainMenu.update(e, mainMenustate)
                elif mainMenustate == 1:
                    map.loadRandomMap()
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 2:
                    map.loadFileMap('testmap')
                    Game.state = STATE_LOADGAME
                elif mainMenustate == 3:
                    pygame.examples.aliens.main()
                else:
                    pygame.quit()
                    sys.exit()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update(rect_list)

        elif Game.state == STATE_INITGAMEMENU:
            screen.fill(background)
            screen.blit(menubackground, (0, 0))
            pygame.display.flip()
            gameMenustate = 0
            gameMenuprev_state = 1
            Game.state = STATE_GAMEMENU
        
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

                # User moves over the mouse 
                elif event.type == pygame.MOUSEMOTION:
                    if towerBar.selectedTower != -1:
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

                # User clicks the mouse. Get the position
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Change the x/y screen coordinates to grid coordinates (For the map)
                    column = pos[0] // tileSize
                    row = pos[1] // tileSize

                    # Inside Map
                    if (column < mapWidth) and (row < mapHeight):
                        if towerBar.selectedTower != 0:
                            if map.M[row][column] == car_turret:
                                if map.T[row][column] == 0:
                                    #TODO : money check
                                    towers.placeTower(map, towerBar.selectedTower, row, column)

                    # Inside Menu
                    elif column >= mapWidth:
                        menu.onClick(pos, map)

                    # Inside Tower Bar
                    else:
                        towerBar.onClick(pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.state = STATE_INITGAMEMENU
                    elif event.key == pygame.K_SPACE:
                        if Game.state == STATE_GAME:
                            Game.state = STATE_PREPARATION
                        elif Game.state == STATE_PREPARATION: 
                            Game.state = STATE_GAME
                    elif event.key == pygame.K_1:
                        towerBar.selectTower(1)
                    elif event.key == pygame.K_2:
                        towerBar.selectTower(2)
                    elif event.key == pygame.K_3:
                        towerBar.selectTower(3)
                    elif event.key == pygame.K_4:
                        towerBar.selectTower(4)
                    elif event.key == pygame.K_5:
                        towerBar.selectTower(5)
                    elif event.key == pygame.K_r:
                        towers.clear()
                        wave.clear()
                        shots.clear()
                    elif event.key == pygame.K_t:
                        towers.clear()
                        shots.clear()
            
            if Game.state == STATE_LOADGAME:
                screen.fill(background)
                layer1.fill(pink)
                layer3.fill(pink)
                pygame.draw.rect(layer3, background, ([mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize]))
                # Draw the map
                drawMap(map, layer1)
                # Draw the game information menu
                menu.draw(layer3)
                # Draw the tower bar ~ 0
                towerBar.draw(layer3)
                Game.state = STATE_PREPARATION
                screen.blit(layer3, (0,0))
                pygame.display.flip()
            elif Game.state == STATE_PREPARATION:
                drawTick += 1
                #print(clock.get_fps())
                if drawTick >= clock.get_fps()/10:
                    drawTick = 0
                    drawGame(map, towerBar, towers, wave, shots, menu, screen, layer1, layer2, layer3)

            elif Game.state == STATE_GAME:
                ## Game
                # Spawn any new enemy in the wave queue
                wave.spawn()
                # Move the enemies
                wave.move()
                # Tower target
                towers.target(shots)
                ## Display
                
                drawTick += 1
                #print(clock.get_fps())
                if drawTick >= clock.get_fps()/10:
                    drawTick = 0
                    drawGame(map, towerBar, towers, wave, shots, menu, screen, layer1, layer2, layer3)

            
        
        # Limit to 24 frames per second
        #print(pygame.time.get_ticks())
        clock.tick()

    pygame.quit ()

def drawGame(map, towerBar, towers, wave, shots, menu, screen, layer1, layer2, layer3):

    # Empty layer 2 (MOUSE OVER WENT OUTSIDE A TURRET SPOT...)
    layer2.fill(pink)
    
    # Draw route
    #drawRoute(map, layer1)
    # Draw Tower Spots
    #drawTowerEmplacements(map, layer1)
    drawMap(map, layer1)

    # Draw On Mouse Over ~ 0
    # IF ON MOUSE OVER ON TURRET...
    drawOnMouseOver(map, towerBar, layer2)
    
    # Draw the towers
    # IF NEW TOWER...
    towers.draw(layer1)

    # Draw the wave
    wave.draw(layer1)
    
    # Towers Target
    shots.draw(layer1)

    # Draw the layers ~ 200 fps
    screen.blit(layer1, (0, 0), (0, 0, mapWidth*tileSize, mapHeight*tileSize))
    screen.blit(layer2, (0, 0), (0, 0, mapWidth*tileSize, mapHeight*tileSize))

    # Update the screen
    pygame.display.update(0, 0, mapWidth*tileSize, mapHeight*tileSize + bottomMenuSize)

def drawOnMouseOver(map, towerBar, layer):
    # Draw tower on mouse over
    for row in range(mapHeight):
        for column in range(mapWidth):
            if (map.T[row][column] == 0) and (map.O[row][column] > 0):
                if TowerTypes[towerBar.selectedTower-1][TowerRANGE] == 0:
                    pygame.draw.circle(layer, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), TowerTypes[towerBar.selectedTower-1][TowerSPLASH][0]*tileSize, 0)
                else:
                    pygame.draw.circle(layer, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), 
                    TowerTypes[towerBar.selectedTower-1][TowerRANGE][0]*tileSize, 0)
                pygame.draw.circle(layer, TowerShotGraphs[towerBar.selectedTower-1][0], (tileSize*column+tileSize/2, tileSize*row+tileSize/2), (TowerTypes[towerBar.selectedTower-1][TowerRANGE][0] + TowerTypes[towerBar.selectedTower-1][TowerSPLASH][0]) * tileSize, tileSize/16)
                layer.blit(Images.TowerImages[towerBar.selectedTower-1][0], (tileSize*column,tileSize*row), None, 1)

def drawRoute(map, layer):
    for row in range(mapHeight):
        for column in range(mapWidth):
            if map.M[row][column] == car_path:
                #map.drawAt(layer, route, row, column)
                # Draw tiles with Grid
                if map.showGrid == 1:
                    pygame.draw.rect(layer, route, [tileSize*column, tileSize*row, tileSize-gridSize, tileSize-gridSize])
                # Draw tiles without grid
                else:
                    pygame.draw.rect(layer, route, [tileSize*column, tileSize*row, tileSize, tileSize])

def drawTowerEmplacements(map, layer):
    for row in range(mapHeight):
        for column in range(mapWidth):
            if map.M[row][column] == car_turret:
                # Draw tiles with Grid
                if map.showGrid == 1:
                    pygame.draw.rect(layer, tower, [tileSize*column, tileSize*row, tileSize-gridSize, tileSize-gridSize])
                # Draw tiles without grid
                else:
                    pygame.draw.rect(layer, tower, [tileSize*column, tileSize*row, tileSize, tileSize])

def drawMap(map, layer):
    # Draw the map
    for row in range(mapHeight):
        for column in range(mapWidth):

            # Identify terrain type
            color = empty
            if map.M[row][column] == car_path:
                color = route
            if map.M[row][column] == car_turret:
                color = tower
            if map.M[row][column] == car_base:
                color = base

            # Draw tiles with Grid
            if map.showGrid == 1:
                pygame.draw.rect(layer, color, [tileSize*column, tileSize*row, tileSize-gridSize, tileSize-gridSize])

            # Draw tiles without grid
            else:
                pygame.draw.rect(layer, color, [tileSize*column, tileSize*row, tileSize, tileSize])

if __name__ == "__main__":
    main()
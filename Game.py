import sys, os, pygame, Map, Menu, TowerBar, Wave, Towers, Shot, Global, Game, Images, Level
import pygame.examples.aliens
from Global import *
from MainMenu import *
from Shots import *
from pgu import gui

class SiampleDialog(gui.Dialog):
    def __init__(self):
        title = gui.Label("Popup")
        main = gui.Container(width=20, height=20)
        super(SimpleDialog, self).__init__(title, main, width=40, height=40)

    def close(self, *args, **kwargs):
        print "closing"
        Game.state = STATE_LOADGAME
        return super(SimpleDialog, self).close(*args, **kwargs)

class SimpleDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Map 3")
        width = 400
        height = 200
        doc = gui.Document(width=width)
        space = title.style.font.size(" ")
        
        doc.block(align=0)
        
        for word in """Welcome to map 3""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        for word in """Good luck, have fun etc.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])

        gui.Dialog.__init__(self,title,gui.ScrollArea(doc,width,height))

    def close(self, *args, **kwargs):
        print "closing"
        Game.state = STATE_LOADGAME
        return super(SimpleDialog, self).close(*args, **kwargs)

def newPopup():
    #Create popup
    dialog = SimpleDialog()
    Game.popUp = gui.App()
    Game.popUp.init(dialog)
    Game.state = STATE_INITPOPUP

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
    Game.mainMenuFont = pygame.font.Font(None, 32)
    Game.gameMenuFont = pygame.font.Font(None, 24)
    Game.enemyCountFont = pygame.font.Font(None, 30)

    # Set the height and width of the screen
    size = [mapWidth*tileSize + rightMenuSize, mapHeight*tileSize + bottomMenuSize]
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

    # Initialize the Images
    Images.init()
    
    # Initialize the MainMenu
    mainMenu = cMenu(128, 320, 20, 5, 'vertical', 100, screen,
               [('Start Automatic Tests', 1, None),
                ('Start Basic Map', 2, None),
                ('Start Map 1', 3, None),
                ('Start Map 2', 4, None),
                ('Start Map 3', 5, None),
                ('Start Test Map', 6, None),
                ('Start Balance Tests', 7, None),
                ('Exit', 8, None)], Images.Background)
    gameMenu = cMenu(128, 320, 20, 5, 'vertical', 100, screen,
               [('Resume', 1, None),
                ('Back to main menu (current progress will be lost!)', 2, None)], Images.Background)

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
                    Game.state = STATE_LOADGAME
                    map.loadFileMap('basicmap')
                elif mainMenustate == 3:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('map1')
                elif mainMenustate == 4:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('map2')
                elif mainMenustate == 5:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('map3')
                elif mainMenustate == 6:
                    Game.state = STATE_LOADGAME
                    map.loadFileMap('testmap')
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

        ## POP UP
        if Game.state == STATE_INITPOPUP:
            print 'Popup Init'
            Game.state = STATE_POPUP
            #Add a background or the game behind the text...
            screen.blit(InterfaceBGopaque, (0, 0))
            drawMap(map, screen)
            menu.draw(screen)
            towerBar.draw(screen)
            pygame.display.flip()

        elif Game.state == STATE_POPUP:
            drawTick += 1
            if drawTick >= clock.get_fps()/24:
                drawTick = 0
                Game.popUp.paint(screen)
                pygame.display.update(267,190,458,265)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        dialog.open()
                    else:
                        Game.popUp.event(event)
                elif event.type == pygame.QUIT:
                    sys.exit()
                else:
                    Game.popUp.event(event)
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
                            map.O[map.currentOY][map.currentOX] = -1
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
                        if 0 in Game.level.levelTowers:
                            towerBar.selectTower(0)
                    elif event.key == pygame.K_2:
                        if 1 in Game.level.levelTowers:
                            towerBar.selectTower(1)
                    elif event.key == pygame.K_3:
                        if 2 in Game.level.levelTowers:
                            towerBar.selectTower(2)
                    elif event.key == pygame.K_4:
                        if 3 in Game.level.levelTowers:
                            towerBar.selectTower(3)
                    elif event.key == pygame.K_5:
                        if 4 in Game.level.levelTowers:
                            towerBar.selectTower(4)
                    elif event.key == pygame.K_6:
                        if 5 in Game.level.levelTowers:
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
                Game.state = STATE_PREPARATION
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
    if menu.redraw:
        menu.draw(screen)
        pygame.display.update(mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize)

    # Update the towerbar portion of the screen
    if towerBar.redraw:
        towerBar.draw(screen)
        pygame.display.update(0, mapHeight*tileSize, mapWidth*tileSize + rightMenuSize, bottomMenuSize)

def drawOnMouseOver(map, towerBar, screen):
    # Draw tower on mouse over
    for row in range(mapHeight):
        for column in range(mapWidth):
            if (map.T[row][column] == 0) and (map.O[row][column] >= 0):
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
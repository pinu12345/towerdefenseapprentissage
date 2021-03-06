import sys, os, pygame, Map, Menu, TowerBar, Wave, Towers, Shot, Global, Game, Images, Level, Evaluate, Progress
import pygame.examples.aliens
from pygame.locals import *
from Global import *
from MainMenu import *
from Shots import *
from pgu import gui
from pgu import html

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
    def __init__(self,message):
        title = gui.Label(" ")
        width = 600
        height = 400
        space = title.style.font.size(" ")
        doc = html.HTML(message,width=580)
        gui.Dialog.__init__(self,title,gui.ScrollArea(doc,width,height))

    def close(self, *args, **kwargs):
        Game.state = STATE_LOADGAME
        return super(SimpleDialog, self).close(*args, **kwargs)

def newPopup(message):
    #Create popup
    Game.dialog = SimpleDialog(message)
    Game.popUp = gui.App()
    Game.popUp.init(Game.dialog)
    Game.state = STATE_INITPOPUP
    
def increaseSpeed(menu):
    if Game.speedModifier < 8.0:
        Game.speedModifier *= 2.0
        menu.drawSpeed += 1
        menu.redrawSpeed = 1

def reduceSpeed(menu):
    if Game.speedModifier > 0.5:
        Game.speedModifier /= 2.0
        menu.drawSpeed -= 1
        menu.redrawSpeed = 1

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
    Game.enemyCountFont = pygame.font.Font(None, 24)
    Game.popUpFont = pygame.font.Font(None, 24)

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
    
    Game.EndLevelDraw = 0
    Game.restartWave = 0
    Game.nextWave = 0

    # Initialize the Images
    Images.init()
    
    # Initialize the MainMenu
    mainMenu = cMenu(128, 320, 20, 5, 'vertical', 100, screen,
               [('Campaign', 1, None),
                ('Challenge 1', 2, None),
                ('Challenge 2', 3, None),
                ('Challenge 3', 4, None),
                ('Challenge 4', 5, None),
                ('Challenge 5', 6, None),
                ('Random Level', 7, None),
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
    towerBar = TowerBar.TowerBar(0, mapHeight*tileSize, map, towers)

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
                #Campagin
                elif mainMenustate == 1:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Campaign1')
                #Challenges
                elif mainMenustate == 2:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Challenge1')
                elif mainMenustate == 3:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Challenge2')
                elif mainMenustate == 4:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Challenge3')
                elif mainMenustate == 5:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Challenge4')
                elif mainMenustate == 6:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Challenge5')
                #Random Level
                elif mainMenustate == 7:
                    Game.state = STATE_LOADGAME
                    Game.level.loadLevel('Campaign1')
                #Quit
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
            Game.state = STATE_POPUP
            #Add a background or the game behind the text...
            screen.blit(InterfaceBGopaque, (0, 0))
            drawMap(map, screen)
            menu.draw(screen)
            Game.redrawSPBtn = 1
            menu.drawSPBtn(screen)
            towerBar.draw(screen)
            towerBar.moneyUpdated(screen)
            towerBar.showTower(screen)
            towerBar.updateTowerCost = 0
            pygame.display.flip()

        elif Game.state == STATE_POPUP:
            drawTick += 1
            if drawTick >= clock.get_fps()/24:
                drawTick = 0
                Game.popUp.paint(screen)
                pygame.display.update(167,90,658,465)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.dialog.close()
                    elif event.key == pygame.K_RETURN:
                        Game.dialog.close()
                    elif event.key == pygame.K_SPACE:
                        Game.dialog.close()
                elif event.type == pygame.QUIT:
                    sys.exit()
                else:
                    Game.popUp.event(event)
                    
        ## Wave finished [Draw then restartWave or start next Wave] -> PopUp lorsque level finished?
        elif Game.state == STATE_ENDWAVE:
            if not Game.autoMode and not Game.balanceMode:
                drawTick += 1
                if drawTick >= clock.get_fps()/24:
                    Game.EndLevelDraw += 1
                    drawTick = 0
                    drawGame(map, towerBar, towers, wave, shots, menu, screen, layer)
                    if Game.EndLevelDraw >= 5:
                        Game.state = STATE_PREPARATION
                        Game.EndLevelDraw = 0
                        if Game.restartWave:
                            Game.restartWave = 0
                            Game.level.restartWave()
                        elif Game.nextWave:
                            Game.nextWave = 0
                            Game.level.nextWave()
                        else:
                            print 'Confus :('
        else:
            for event in pygame.event.get(): # User did something
                # If user clicked close
                if event.type == pygame.QUIT: 
                    close_game = True # Flag that we are done so we exit this loop

                ## Mouse Events
                # User moves over the mouse 
                elif event.type == pygame.MOUSEMOTION:
                    updateUnderMouse(map, towerBar, towers)

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
                                    towers.placeTower(towerBar.selectedTower, 0, row, column)
                                    Game.placedTower = 1
                                else:
                                    towers.updateTower(towerBar.selectedTower, row, column)
                                    Game.placedTower = 1
                        elif towerBar.selectedTower == TowerUPGRADE:
                            if map.M[row][column] == car_turret:
                                if map.T[row][column] != 0:
                                    towers.updateTower(towerBar.selectedTower, row, column)
                                    Game.placedTower = 1
                        elif towerBar.selectedTower == TowerERASE:
                            if map.M[row][column] == car_turret:
                                if map.T[row][column] != 0:
                                    towers.eraseTower(row, column)
                                    Game.placedTower = 1
                        updateUnderMouse(map, towerBar, towers)

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
                            Game.redrawSPBtn = 1
                            Game.state = STATE_PREPARATION
                        elif Game.state == STATE_PREPARATION: 
                            Game.redrawSPBtn = 2
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
                        Game.increaseSpeed(menu)
                    elif event.key == pygame.K_MINUS:
                        Game.reduceSpeed(menu)
                    elif event.key == pygame.K_c:
                        towers.resetCooldowns()
                    elif event.key == pygame.K_r:
                        towerBar.selectTower(TowerUPGRADE)
                    elif event.key == pygame.K_e:
                        towerBar.selectTower(TowerERASE)
                    elif event.key == pygame.K_a:
                        towers.clear()
                        wave.clear()
                        shots.clear()
                    elif event.key == pygame.K_t:
                        towers.clear()
                        shots.clear()
                    elif event.key == pygame.K_v:
                        Evaluate.evalPlayerPosition()
                    elif event.key == pygame.K_b:
                        Progress.prog()
            
            ## Init Game
            if Game.state == STATE_LOADGAME:
                Game.redrawSPBtn = 1
                Game.state = STATE_PREPARATION
                screen.blit(InterfaceBGopaque, (0, 0))
                #screen.fill(background)
                #pygame.draw.rect(screen, background, ([mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize]))
                #pygame.draw.rect(screen, background, ([0, mapHeight*tileSize, mapWidth*tileSize, bottomMenuSize]))
                
                # Draw the map
                drawMap(map, screen)

                # Draw the game information menu
                menu.draw(screen)
                Game.redrawSPBtn = 1
                menu.drawSPBtn(screen)
                
                towerBar.moneyUpdated(screen)
                towerBar.showTower(screen)
                towerBar.updateTowerCost = 0

                # Draw the tower bar ~ 0
                towerBar.draw(screen)
                
                
                pygame.display.flip()

            ## Game Paused
            if Game.state == STATE_PREPARATION:
                if Game.autoMode or Game.balanceMode:
                    Game.redrawSPBtn = 1
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
        drawOnMouseOver(map, layer)
        Game.repaintMap = 1
    else:
        if Game.repaintMap:
            Game.repaintMap = 0

    if Game.placedTower:
        if Game.repaintMap:
            drawMap(map, screen)
            Game.repaintMap = 0
        else:
            drawTowerEmplacements(map, screen)
        Game.placedTower = 0

    # Draw the towers
    towers.drawRadioactivity(screen)
    # Draw les bases de tours sans contour
    drawTowerEmplacementsSquares(map, screen)
    # Draw les tours
    towers.draw(screen)

    # Draw the wave
    wave.draw(screen)
    
    # Towers Target
    shots.draw(screen)
    
    # Update the game portion of the screen
    if Game.drawMouseOver:
        screen.blit(layer, (0, 0), (0, 0, mapWidth*tileSize, mapHeight*tileSize))
    pygame.display.update(0, 0, mapWidth*tileSize, mapHeight*tileSize)

    ## UPDATE THE INTERFACE ##
    # Update the right menu portion of the screen
    if menu.redraw:
        menu.draw(screen)
        pygame.display.update(mapWidth*tileSize, 0, rightMenuSize, mapHeight*tileSize + bottomMenuSize)
    
    # Update the speed arrows
    if menu.redrawSpeed:
        menu.drawSpeedArrows(screen)
        pygame.display.update(850, 62, 62, 24)

    # Update the Start Pause button
    if Game.redrawSPBtn:
        menu.drawSPBtn(screen)
        pygame.display.update(784, 14, 92, 28)

    # Update the towerbar portion of the screen
    if towerBar.updateMoney:
        towerBar.moneyUpdated(screen)
        pygame.display.update(280, 520, 183, 32)
    if towerBar.redraw:
        towerBar.draw(screen)
        pygame.display.update(0, mapHeight*tileSize, 194, bottomMenuSize)
    if towerBar.updateTowerCost:
        towerBar.showTower(screen)
        towerBar.updateTowerCost = 0
        pygame.display.update(196, mapHeight*tileSize, mapWidth*tileSize + rightMenuSize - 196, bottomMenuSize)
        
def drawOnMouseOver(map, screen):
    # Draw tower on mouse over
    for row in range(mapHeight):
        for column in range(mapWidth):
            if (map.O[row][column] >= 0):
                if TowerStats[map.O[row][column]][map.currentOLevel][TowerRANGE] == 0:
                    pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), TowerStats[map.O[row][column]][map.currentOLevel][TowerSPLASH], 0)
                else:
                    pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), 
                    TowerStats[map.O[row][column]][map.currentOLevel][TowerRANGE], 0)
                pygame.draw.circle(screen, ShotGraphs[map.O[row][column]][ShotCOLOR], (tileSize*column+tileSize/2, tileSize*row+tileSize/2), TowerStats[map.O[row][column]][map.currentOLevel][TowerRANGE] + TowerStats[map.O[row][column]][map.currentOLevel][TowerSPLASH], tileSize/16)
                screen.blit(Images.TowerImages[map.O[row][column]][0], (tileSize*column,tileSize*row), None, 0)

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

def drawTowerEmplacementsSquares(map, screen):
    for row in range(mapHeight):
        for column in range(mapWidth):
            if map.M[row][column] == car_turret:
                    screen.blit(map.S[row][column], (7+column*tileSize, 7+row*tileSize), (7, 7, 18, 18))
            if map.M[row][column] == car_base:
                    screen.blit(map.S[row][column], (7+column*tileSize, 7+row*tileSize), (7, 7, 18, 18))

def drawMap(map, screen):
    # Draw the map
    for row in range(mapHeight):
        for column in range(mapWidth):
             screen.blit(map.S[row][column], (column*tileSize, row*tileSize))

def updateUnderMouse(map, towerBar, towers):
    Game.drawMouseOver = 0
    pos = pygame.mouse.get_pos()
    column = pos[0] // tileSize
    row = pos[1] // tileSize
    towerBar.displayTower = towerBar.selectedTower
    towerBar.displayTowerLevel = 0
    # Inside Map
    if (column < mapWidth) and (row < mapHeight):
        map.O[map.currentOY][map.currentOX] = -1
        towerBar.updateTowerCost = 1
        if towerBar.selectedTower > -1:
            if map.M[row][column] == car_turret:
                map.currentOY = row
                map.currentOX = column
                if map.T[row][column] == 0:
                    map.currentOLevel = 0
                    map.O[row][column] = towerBar.selectedTower
                    Game.drawMouseOver = 1
                else:
                    towerType, towerLevel, isMaxLevel = towers.getUpgradedTower(row, column)
                    if towerBar.selectedTower == towerType:
                        towerBar.displayTower = towerType
                        towerBar.displayTowerLevel = towerLevel
                        map.currentOLevel = towerLevel
                        if not isMaxLevel:
                            map.O[row][column] = towerBar.selectedTower
                            Game.drawMouseOver = 1
                        else:
                            towerBar.updateTowerCost = 2
        elif towerBar.selectedTower == TowerUPGRADE:
            if (map.M[row][column] == car_turret) and (map.T[row][column] != 0):
                towerBar.displayTower, towerBar.displayTowerLevel, isMaxLevel = towers.getUpgradedTower(row, column)
                map.currentOY = row
                map.currentOX = column
                map.currentOLevel = towerBar.displayTowerLevel
                if not isMaxLevel:
                    map.O[row][column] = towerBar.displayTower
                    Game.drawMouseOver = 1
                else:
                    towerBar.updateTowerCost = 2
        elif towerBar.selectedTower == TowerERASE:
            if (map.M[row][column] == car_turret) and (map.T[row][column] != 0):
                towerBar.displayTower, towerBar.displayTowerLevel = towers.getCurrentTower(row, column)
                map.currentOY = row
                map.currentOX = column
                map.currentOLevel = towerBar.displayTowerLevel
                towerBar.updateTowerCost = 3

if __name__ == "__main__":
    main()
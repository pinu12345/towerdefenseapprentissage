import sys, os, pygame, Map, Menu, TowerBar, Wave, Towers, Shot
from Global import *

def main():

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    mapWidth = 24
    mapHeight = 16
    tileSize = 32
    rightMenuSize = 200
    bottomMenuSize = 100

    cash = 2100
    health = 100

    # Set the height and width of the screen
    size = [mapWidth*(tileSize+1) + rightMenuSize,mapHeight*(tileSize+1) + bottomMenuSize]
    screen = pygame.display.set_mode(size)
    layer1 = 
    
    # Initialize the map
    map = Map.Map(mapWidth,mapHeight)
    map.loadRandomMap()
    # map.loadBasicMap()
    # map.loadFileMap('testmap')
    # map.loadTestMap()

    # Initialize the wave
    wave = Wave.Wave(map)
    
    # Initialize the Towers class
    towers = Towers.Towers(map, wave)
    
    # Initialize the shot graphics
    shots = []
    
    # Initialize the tower bar
    towerBar = TowerBar.TowerBar(17, mapHeight*(tileSize+1)+35)

    # Initialize the menu
    menu = Menu.Menu(map, wave, towers)

    # Initialize pygame
    pygame.init()

    # Set title of screen
    pygame.display.set_caption("4D tower defense - (c) POB + ND")

    #Loop until the user clicks the close button.
    close_game = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
        
    # -------- Main Program Loop -----------
    while close_game == False:
        
        for event in pygame.event.get(): # User did something

            # If user clicked close
            if event.type == pygame.QUIT: 
                close_game = True # Flag that we are done so we exit this loop

            # User moves over the mouse 
            if event.type == pygame.MOUSEMOTION:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        # Set the screen background
        screen.fill(background)

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
                    pygame.draw.rect(screen, color, \
                    [tileSize*column, tileSize*row, \
                    tileSize-gridSize, tileSize-gridSize])

                # Draw tiles without grid
                else:
                    pygame.draw.rect(screen, color, \
                    [tileSize*column, \
                    tileSize*row, tileSize, tileSize])

        # Draw tower on mouse over
        for row in range(mapHeight):
            for column in range(mapWidth):
                if (map.T[row][column] == 0) and (map.O[row][column] > 0):
                    if TowerTypes[towerBar.selectedTower-1][TowerRANGE] == 0:
                        pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), TowerTypes[towerBar.selectedTower-1][TowerSPLASH]*tileSize, 0)
                    else:
                        pygame.draw.circle(screen, rangeCircle, (tileSize*column + tileSize/2,tileSize*row + tileSize/2), TowerTypes[towerBar.selectedTower-1][TowerRANGE]*tileSize, 0)
                    screen.blit(pygame.image.load(os.path.join( \
                        'Images\Towers', str(towerBar.selectedTower)+'.png')).convert(), \
                        (tileSize*column,tileSize*row), None, 1)
                    pygame.draw.circle(screen, \
                        TowerShotGraphs[towerBar.selectedTower-1][0], \
                        (tileSize*column+tileSize/2, tileSize*row+tileSize/2), \
                        (TowerTypes[towerBar.selectedTower-1][TowerRANGE] + \
                        TowerTypes[towerBar.selectedTower-1][TowerSPLASH]) \
                        * tileSize, tileSize/16)
                    
        # Draw the tower bar
        towerBar.draw(screen)
        
        # Draw the towers
        towers.draw(screen)

        # Spawn any new enemy in the wave queue
        wave.spawn()

        # Move the enemies
        wave.move()

        # Draw the wave
        wave.draw(screen)
        
        # Towers Target
        towers.target(screen, shots)
        for shot in shots:
            shot.draw(screen)
        
        # Draw the game information menu
        menu.draw(screen)

        # Limit to 24 frames per second
        clock.tick_busy_loop(30)

        # Update the screen
        pygame.display.flip()

    pygame.quit ()

if __name__ == "__main__":
    main()
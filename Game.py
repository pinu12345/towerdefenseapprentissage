import sys, os, pygame, Map, Menu, TowerBar, Wave
from Global import *

# Colors
background    = (   0,   0,   0)
empty         = ( 120,  80,  40)
route         = ( 200, 190, 170)
tower         = ( 130, 140, 160)
base          = ( 200,  80,  20)

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

    # Initialize the map
    map = Map.Map(mapWidth,mapHeight)
    map.loadRandomMap()
    # map.loadBasicMap()
    # map.loadFileMap('testmap')
    # map.loadTestMap()
    
    # Initialize the menu
    menu = Menu.Menu()
    
    # Initialize the wave
    wave = Wave.Wave(map)
    
    # Initialize the tower bar
    towerBar = TowerBar.TowerBar(17, mapHeight*(tileSize+1)+35)

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
                    if (column < map.mapWidth) and (row < map.mapHeight):
                        map.O[map.currentOY][map.currentOX] = 0
                        if (map.M[row][column] == 2) and (map.T[row][column] == 0):
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
                if (column < map.mapWidth) and (row < map.mapHeight):
                    if map.M[row][column] == 2:
                        if map.T[row][column] == 0:
                            #TODO : money check
                            map.T[row][column] = towerBar.selectedTower

                # Inside Menu
                elif column >= map.mapWidth:
                    menu.onClick(pos, map)

                # Inside Tower Bar
                else:
                    towerBar.onClick(pos)

        # Set the screen background
        screen.fill(background)

        # Draw the map
        for row in range(map.mapHeight):
            for column in range(map.mapWidth):

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
                    [tileSize*column, \
                    tileSize*row, tileSize-gridSize, tileSize-gridSize])

                # Draw tiles without grid
                else:
                    pygame.draw.rect(screen, color, \
                    [tileSize*column, \
                    tileSize*row, tileSize,tileSize])

                # Draw tower on mouse over
                if map.O[row][column] != 0:
                    screen.blit(pygame.image.load(os.path.join ('Images\Towers', str(towerBar.selectedTower)+'.png')),\
                    (tileSize*column,tileSize*row),None,1)

                # Draw towers on map
                if map.T[row][column] != 0:
                    screen.blit(pygame.image.load(os.path.join ('Images\Towers', str(map.T[row][column])+'.png')),\
                    (tileSize*column,tileSize*row),None,0)

        # Draw the tower bar
        towerBar.draw(screen)

        # Spawn the wave
        wave.spawn()

        # Move the enemies
        wave.move()

        # Draw the wave
        wave.draw(screen)

        # Draw the game information menu
        menu.draw(screen)

        # Limit to 24 frames per second
        clock.tick(24)

        # Update the screen
        pygame.display.flip()

    pygame.quit ()

if __name__ == "__main__":
    main()
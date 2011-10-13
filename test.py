import pygame
import random
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

pygame.init()

# Set the height and width of the screen
sizex = 704
sizey = 512
size=[sizex,sizey]
screen=pygame.display.set_mode(size)

# This sets the width and height of each grid location
width=32
height=32

# Create a 2 dimensional array. A two dimesional
# array is simply a list of lists.
grid=[]
for row in range(sizey/height):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(sizex/width):
        grid[row].append(0) # Append a cell


# Set the title of the game 
pygame.display.set_caption("SGGTD : Snowy Grid Greenline Tower Defense")

#Loop until the user clicks the close button.
done=False

#Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Create an empty array
star_list=[]

# Loop 50 times and add a star in a random x,y position
for i in range(50):
    x=random.randrange(0,sizex)
    y=random.randrange(0,sizey)
    star_list.append([x,y])

def draw_map(screen):
    pygame.draw.line(screen,green,[50,250],[650,250],16)
    
def draw_grid(screen):
    # Draw the grid
    for row in range(sizey/height):
        for column in range(sizex/width):
            color = green
            pygame.draw.rect(screen,color,[width*column,height*row,width,height],1)
            
def draw_stars(screen):
    # Process each star in the list
    for i in range(len(star_list)):
        # Draw the star
        pygame.draw.circle(screen,white,star_list[i],2)

        # Move the star down one pixel
        star_list[i][1]+=1
         
        # If the star has moved off the bottom of the screen
        if star_list[i][1] > sizey:
            # Reset it just above the top
            y=random.randrange(-50,-10)
            star_list[i][1]=y
            # Give it a new x position
            x=random.randrange(0,sizex)
            star_list[i][0]=x

# -------- Main Program Loop -----------
while done==False:

	# Limit to 40 frames per second
    clock.tick(40)

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(black)

    # Draw the stars
    draw_stars(screen) 
            
    # Draw the map
    #draw_map(screen)

    # Draw the grid
    draw_grid(screen)
    
	# update the screen
    pygame.display.flip()

pygame.quit ()
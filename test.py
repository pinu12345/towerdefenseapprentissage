import pygame
import random
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

pygame.init()

# Set the height and width of the screen
size=[700,500]
screen=pygame.display.set_mode(size)

# This sets the width and height of each grid location
width=15
height=15
# This sets the margin between each cell
margin=1

# Create a 2 dimensional array. A two dimesional
# array is simply a list of lists.
grid=[]
for row in range(3):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(20):
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
    x=random.randrange(0,700)
    y=random.randrange(0,500)
    star_list.append([x,y])

def draw_map(screen):
    pygame.draw.line(screen,green,[50,250],[650,250],16)

# -------- Main Program Loop -----------
while done==False:

	# Limit to 40 frames per second
    clock.tick(40)

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(black)
    
    # Process each star in the list
    for i in range(len(star_list)):
        # Draw the star
        pygame.draw.circle(screen,white,star_list[i],2)

        # Move the star down one pixel
        star_list[i][1]+=1
         
        # If the star has moved off the bottom of the screen
        if star_list[i][1] > 500:
            # Reset it just above the top
            y=random.randrange(-50,-10)
            star_list[i][1]=y
            # Give it a new x position
            x=random.randrange(0,700)
            star_list[i][0]=x

    # Draw the map
    draw_map(screen)
    
    # Draw the grid
    for row in range(3):
        for column in range(20):
            color = white
            if grid[row][column] == 1:
                color = green
            pygame.draw.rect(screen,color,[(margin+width)*column+margin+50,(margin+height)*row+margin+100,width,height])

	# update the screen
    pygame.display.flip()

pygame.quit ()
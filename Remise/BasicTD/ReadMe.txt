				     __~~::How to Play::~~__
A Manual for the game
   1. how do I start it? Start the main.py file
   2. choose the options then click ok, set towers and watch the war take place
   3. controls:
	to place a tower:
	click the grid square where you want to place the tower
	    then click the tower icon which represents the tower you want to place
	press spacebar to go to the next level
   4. the buying mechanism is that you purchase towers, select them, and then upgrade them by pressing u


				     __~~::Implementation::~~__

    I implemented the game with mostly normal methods. A thing to note is the use of global variables in order to keep watch of the important aspects of the game. I had kept all related functions and classes grouped together. I tried to make multi-purpose classes so that there could be less copy-paste code to handle multiple similar objects. The tower sprite class is used for all of the towers being used in the game. If I had more time I would have merged the enemy sprites to offer more flexibility. The main file only handles sprite creation and the watching of the tower shooting functions. The startup file watches the condition of  the player and the changes to the player variables. The art for the enemies is borrowed as well as the sounds, other than that all else is mine. This game has turned out to be almost exactly what I wanted it to become and I am happy about it. An abnormal way I had gone about doing this project was using global variables, which is something I havent done recently. All else is fairly normal.

Anything left undone: N/A


                                        __~~::Credits::~~__
Code:
Most of the code is mine but is commented in the sections that I had borrowed code from Python PyGame Tower Defense - 0.3.5 from http://pygame.org/project-Python+PyGame+Tower+Defense-1296-.html


Images:
Michael Jackson from Michael Jackson's Moonwalker
Mario art from a mario game
ball like enemy from type-zero
all others are mine

Sounds:
gunshot noise: http://www.flashkit.com/soundfx/Mayhem/Handguns/10mm_Gun-box_o_bu-8676/index.php
death sound:http://www.flashkit.com/soundfx/People/Laughing/demented-Wiretrip-7786/index.php
you getting hurt: http://www.flashkit.com/soundfx/People/Screams/AHHOOOH_-Sam_Love-8923/index.php
background music 1: http://www.flashkit.com/loops/Ambient/Electronica/r-ken0-7912/index.php
background music 2: music from Michael Jackson's Moonwalker
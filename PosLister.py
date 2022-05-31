
"""
This file is the input of the user, user can draw the shape they wish to get the equation for

"""


import pygame as pg
from os.path import dirname
pg.init() # initialise pygame

# initial values
win_width, win_height, run = 1000, 600, True

# the list that stores the coordinate points
longlist = []

# start pygame window
win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Stuff")

# FPS counter is used for an important reason:
# High FPS causes multiple points to be added on a single click
# FPS is set to 2 so the code will run every 0.5 seconds
# This stops many points to be added on a single run
# Though this is bad practice, because pg.time.Clock.tick() stops the whole program for given time
# Which can lead to time outs and slowing down for low FPS values
# Fix: use a timer to make sure every point would be addad every 0.5 seconds and do not touch FPS
FPS = pg.time.Clock()
while run: 
    if pg.mouse.get_pressed()[0] == 1 and pg.mouse.get_pos() not in longlist:
        longlist.append(pg.mouse.get_pos()) # append to the list
        pg.draw.circle(win, (255, 255, 255), pg.mouse.get_pos(), 1, 1)  # display the coordinate on screen
        pg.display.update()  # update the screen

    # break if X is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
    

    FPS.tick(2)

# write to txt file
f = open(f"{dirname(__file__)}/txtfiles/points.txt", "w")
for i in longlist:
    f.write(str(i[0]) + " " + str(i[1]) + "\n")
f.close()

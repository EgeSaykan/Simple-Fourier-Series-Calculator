from math import floor, ceil
from os.path import dirname
import pygame as pg #import pygame (if not installed already: pip3 install pygame)
import coefficientMaker as cf
import functions as fn
pg.init() # initilise pygame to avoid some potential problems

def drawSeries():
    e, pi = 2.718281828459045, 3.14159265358979     # define absulute constants
    win_width, win_height, run = 1000, 600, True    # declare window size, run state
    number_of_circles = 101

    win = pg.display.set_mode((win_width, win_height)) # set the window size
    pg.display.set_caption("Stuff")                    # set window title

    #theCoefficientList = cf.comLater(number_of_circles, win_width, win_height)   # the list of coefficients for each circle, n -> 0 to +/- incrementing n    -> c0, c1, c-1, c2, c-2
    theCoefficientList = fn.cordListGenerate(-150) # precreated coefficients for a nice heart

    t = 0                                           # keeps a track of the time variable
    t_increase = 0.001                              # how much will t increase every run, less the more accurate
    pointsList = []                                 # the list of points of the equation as t varies from 0 to 1

    FPS = pg.time.Clock() # clock object is used to set fps
    while run: # loop to keep the window open

        for event in pg.event.get(): # breaks the loop when X is clicked
            if event.type == pg.QUIT:
                run = False
                break

        
        win.fill((15, 15, 15)) # set all the window black/grey


        total = win_width * 0.5 + win_height * 0.5j # keeps a track of there to add the next circle

        for i, coef in enumerate(theCoefficientList): # iterate through each circle
            firstCordTemporary = total
            if i % 2 == 0:
                thiscoef = 1j*  2*pi * (i / -2) * t     # exponent of clockwise circles and 0 circle
                total += e**(thiscoef) * coef           # the cumilitive centre of the circles
                
                pg.draw.circle(win, (111, 49, 118), (total.real, total.imag), abs(coef), 1)   # draw the circles (purple)
                pg.draw.line(win, (161, 89, 168), (firstCordTemporary.real, firstCordTemporary.imag), (total.real, total.imag), 2)   # draw the lines (purple)

            else:
                thiscoef = 1j*  2*pi * ((i + 1) // 2) * t   # exponent of anticlockwise circles and 0 circle
                total += e**(thiscoef) * coef               # the cumilitive centre of the circles
                #arg = cm.phase(e**(thiscoef))               # argument of the exponent
                
                pg.draw.circle(win, (57, 32, 138), (total.real, total.imag), abs(coef), 1)   # draw the circles (blue)
                pg.draw.line(win, (97, 72, 198), (firstCordTemporary.real, firstCordTemporary.imag), (total.real, total.imag), 2)   # draw the lines (blue)
            
            if i == len(theCoefficientList) - 1 and len(pointsList) + 1 <= 1 / t_increase:   pointsList.append(total)   # append the point to the list if it is at the end
        
        
        # loop through every point and draw them on the screen
        for color in range(len(pointsList)):
            # set the pixel at given term
            win.set_at((floor(pointsList[color].real), floor(pointsList[color].imag)), (50, 190, 145))

        t += t_increase     # increment t
        if t >= 1: t = 0    # if t is i set it back to 0 for an infinate loop
        pg.display.update()     # update the screen rendering
        FPS.tick(100)            # set fps
    pg.quit()

    finalEquation = ""      # the final equation created by the fourier series
    for i, m in enumerate(theCoefficientList):
        if i != 0: forecast = " + "
        else: forecast = ''
        circleN = ceil(i / 2) * ((e**((i+1) * pi * 1j)).real)# hack to give the pattern 0, 1, -1, 2, -2....
        print(f'{forecast}{m} * e^(2pi * i * {str(round(circleN))} * t)')
        finalEquation += (f'{forecast}{m} * e^(2pi * i * {str(round(circleN))} * t)')
    print("\n\n")
    
    with open(f"{dirname(__file__)}/txtfiles/finalequation.txt", "w") as f:
        f.write(finalEquation)



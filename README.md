# Fourier Series Calculator
Fourier series basically calculates the equation that links input the points in given order.
The points are treated as complex numbers in an argand diagram and equation f(t) produces the curve that includes the finest approximation to given points as t varies from 0 to 1.


## This application:
This application first lets users to input a series of points and then when that window is closed and the program is run again, user can chose to see the output of the equation created depending on those points.


## How to use:
The console will first ask 1 or 2,
if chosen 1, user will be able to draw a shape, just keep down the mouse button and draw.

The program will run on 2 FPS because other wise inconsistency in number of points might occur. This could be changed in PosLister.py, line 43 (FPS.tick(2))
When the window is closed via pressing the X on top right corner the points will be written to txtfiles/points.txt.
Note that points will not be written if the window is not closed appropriately.

Then user can run the program again and chose option 2.
A new window will pop up and draw the function with circles used to draw it.
When the widnow is closed via pressing the X on top right corner the equation will be printed to the console and then written to txtfiles/finalequation.txt.
Note that equation will not be written if the window is not closed appropriately.


## Caution:
By default the program will use predefined coefficients to draw a heart.

The the external coefficients made by Robert Wills:
https://www.youtube.com/watch?v=ACvXAjZE9jQ

To change to custom series that was inputted via option 1, in drawSeries.py, uncomment line 16, comment line 17.
It would look like this:

16 - theCoefficientList = cf.comLater(number_of_circles, win_width, win_height)   # the list of coefficients for each circle, n -> 0 to +/- incrementing n    -> c0, c1, c-1, c2, c-2
17 - #theCoefficientList = fn.cordListGenerate(-150) # precreated coefficients for a nice heart

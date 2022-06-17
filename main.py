# check if the user wants to draw shape or see the series
answer = int(input("Enter 1 if you want to draw an input shape.\n\nEnter 2 if you want to see the output series.\n\nEnter 3 if you want to quit.\n\n > "))
from sympy import im
import PosLister
import drawSeries

while answer != 3:
  if answer == 1:
    PosLister.ListThePoints()
  elif answer == 2:
    drawSeries.drawSeries()
  answer = int(input("Enter 1 if you want to draw an input shape.\n\nEnter 2 if you want to see the output series.\n\nEnter 3 if you want to quit.\n\n > "))
"""
This file is used to store the functions that read the coordinates and calculate the coefficients

"""




from math import ceil
from os.path import dirname

e, pi = 2.718281828459045, 3.14159265358979     # define absulute constants


def getCoordinates(winW, winH):
    winW, winH = winW // 2, winH // 2  # to remove the offset as pygame draws from left top corner

    # open and read from points.txt to text list
    with open(f"{dirname(__file__)}/txtfiles/points.txt", "r") as f:
        text = f.readlines()

    # translate to complex numbers in text list
    for i, el in enumerate(text):
        if i != len(text) -1: text[i] = int(el[:el.find(" ")]) - winW + (int(el[1 + el.find(" "):-1]) - winH) * 1j
        else: text[i] = int(el[:el.find(" ")]) - winW + (int(el[1 + el.find(" "):]) - winH) * 1j
    return text



def comLater(numberOfCircles, winW, winH):
    cordList = getCoordinates(winW, winH)
    if len(cordList) < numberOfCircles:
        numberOfCircles = len(cordList)
    coef = []
    
    for m in range(numberOfCircles):
        sum = 0
        circleN = ceil(m / 2) * ((e**((m+1) * pi * 1j)).real)# hack to give the pattern 0, 1, -1, 2, -2....
        for i in range(len(cordList)):    
            sum += cordList[i] * e**(2*pi * 1j * (i / len(cordList)) * circleN)
        sum /= len(cordList)
        coef.append(sum)
    return coef
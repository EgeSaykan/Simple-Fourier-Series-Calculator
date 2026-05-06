"""
This file is used to store the functions that read the coordinates and calculate the coefficients

"""




from math import ceil
from os.path import dirname
import numpy as np
import matplotlib.pyplot as plt

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
    numpy_array = np.array(text)
    real_parts = np.real(numpy_array)
    imag_parts = np.imag(numpy_array)
    max_real = np.max(np.abs(real_parts))
    max_imag = np.max(np.abs(imag_parts))
    real_parts = real_parts / max_real * winW*1.5 - winW * 0.6
    imag_parts = imag_parts / max_imag * winH - winH * 0.15
    # plot as dots instead of a connected line
    
    numpy_array = real_parts + 1j * imag_parts
    text = list(numpy_array)
    
    # Save visualization of points
    fig, ax = plt.subplots(figsize=(10, 10))
    coords = text[::-3]
    real_vals = [c.real for c in coords]
    imag_vals = [c.imag for c in coords]
    ax.plot(real_vals, imag_vals, 'b-', linewidth=0.5, alpha=0.7)
    ax.scatter(real_vals, imag_vals, c='red', s=1, alpha=0.5)
    ax.set_aspect('equal')
    ax.set_title('Point Path Visualization')
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    plt.savefig(f"{dirname(__file__)}/txtfiles/point_to_plot.png", dpi=100, bbox_inches='tight')
    plt.close()
    
    return text[::-1]



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
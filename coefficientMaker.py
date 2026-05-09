"""
This file is used to store the functions that read the coordinates and calculate the coefficients

"""




from math import ceil
from os.path import dirname
import numpy as np
import matplotlib.pyplot as plt
import re
import json

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
    real_parts = real_parts / max_real * winW*1.5 - winW * 0.5
    imag_parts = imag_parts / max_imag * winH - winH * 0.15
    # plot as dots instead of a connected line
    
    numpy_array = real_parts + 1j * imag_parts
    
    # Save visualization of points
    fig, ax = plt.subplots(figsize=(10, 10))
    coords = numpy_array[::-1]
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
    
    return numpy_array[::-1]

def read_coefficients_from_file():
    with open(f"{dirname(__file__)}/txtfiles/coefficients.json", "r") as f:
        data = json.load(f)
    coefficients = np.array([complex(c[0], c[1]) for c in data])
    return coefficients

# print(read_coefficients_from_file())

def comLater(numberOfCircles, winW, winH, saveToFile=True):
    cordList = getCoordinates(winW, winH)
    if len(cordList) < numberOfCircles:
        numberOfCircles = len(cordList)
    
    # Vectorized computation using numpy
    m_values = np.arange(numberOfCircles)
    circleN_values = np.ceil(m_values / 2) * ((e**((m_values + 1) * pi * 1j)).real)
    
    # Create index array for vectorized exponent calculation
    indices = np.arange(len(cordList))
    
    # Compute exponentials with shape (numberOfCircles, len(cordList))
    exponentials = e**(2*pi * 1j * (indices / len(cordList)) * circleN_values[:, np.newaxis])
    
    # Vectorized sum and averaging
    coef = np.sum(cordList * exponentials, axis=1) / len(cordList)

    if saveToFile:
        with open(f"{dirname(__file__)}\\txtfiles\\coefficients.json", "w") as f:
            json.dump([[float(c.real), float(c.imag)] for c in coef], f)

    
    
    return coef


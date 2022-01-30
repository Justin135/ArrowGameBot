# Import some modules
import cv2 # An image proccessing library
import pytesseract # an image to text library
import numpy as np # used for mathematics but can be used in image proccessing
import pyautogui
import time
import pyscreenshot
from PIL import Image
from copy import deepcopy

# Positions:
# Top Left: x=750, y=365
# Top Right: x=1165, y=365
# Bottom Left: x=750, y=794
# Bottom Right: x=1165, y=794
# End Button: x=945, y=845
# X for Give Up: x=1170, y=419
# No for Give Up: x=1063, y=543

# Configure the module
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.PAUSE = 0.01

NUM_GAMES = 1000 # Dictates how many rounds of the game are played.
PAUSE_BEFORE_GAME = 5  # Dictates how long to wait in seconds before the bot begins playing the game (in case you have to switch windows or something).
x_vals = [771, 840, 890, 955, 1015, 1060, 1120] # X values to screenshot.
y_vals = [367, 405, 435, 466, 503, 534, 570, 604, 638, 664, 702, 730, 768]
grid = [[0, 0, 0, 7, 0, 0, 0],
        [0, 0, 7, 0, 7, 0, 0],
        [0, 7, 0, 7, 0, 7, 0],
        [7, 0, 7, 0, 7, 0, 7],
        [0, 7, 0, 7, 0, 7, 0],
        [7, 0, 7, 0, 7, 0, 7],
        [0, 7, 0, 7, 0, 7, 0],
        [7, 0, 7, 0, 7, 0, 7],
        [0, 7, 0, 7, 0, 7, 0],
        [7, 0, 7, 0, 7, 0, 7],
        [0, 7, 0, 7, 0, 7, 0],
        [0, 0, 7, 0, 7, 0, 0],
        [0, 0, 0, 7, 0, 0, 0]]

grid2 = []
numTaps = 0

def setGrid():
    
    # Get the image.
    image = pyscreenshot.grab(bbox=(0, 0, 1920, 1080))
    pixel = image.load()
    
    # Get the first value.
    if sum(pixel[x_vals[3], y_vals[0]]) >= 245 and sum(pixel[x_vals[3], y_vals[0]]) <= 265: grid[0][3] = 2
    else: grid[0][3] = 1
    
    # Get the second row.
    for i in range(2):
        if sum(pixel[x_vals[2 + (2 * i)], y_vals[1]]) >= 245 and sum(pixel[x_vals[2 + (2 * i)], y_vals[1]]) <= 265: grid[1][2 + (2 * i)] = 2
        else: grid[1][2 + (2 * i)] = 1
    
    # Get the third row.
    for i in range(3):
        if sum(pixel[x_vals[1 + (2 * i)], y_vals[2]]) >= 245 and sum(pixel[x_vals[1 + (2 * i)], y_vals[2]]) <= 265: grid[2][1 + (2 * i)] = 2
        else: grid[2][1 + (2 * i)] = 1
    
    # Get the fourth, fifth, ..., tenth rows.
    for i in range(7):
        
        # Rows with four values.
        if i % 2 == 0:
            for j in range(4):
                if sum(pixel[x_vals[2 * j], y_vals[3 + i]]) >= 245 and sum(pixel[x_vals[2 * j], y_vals[3 + i]]) <= 265: grid[3 + i][2 * j] = 2
                else: grid[3 + i][2 * j] = 1
        
        # Rows with three values.
        else:
            for j in range(3):
                if sum(pixel[x_vals[(2 * j) + 1], y_vals[3 + i]]) >= 245 and sum(pixel[x_vals[(2 * j) + 1], y_vals[3 + i]]) <= 265: grid[3 + i][2 * j + 1] = 2
                else: grid[3 + i][2 * j + 1] = 1
    
    # Get the eleventh row.
    for i in range(3):
        if sum(pixel[x_vals[1 + (2 * i)], y_vals[10]]) >= 245 and sum(pixel[x_vals[1 + (2 * i)], y_vals[10]]) <= 265: grid[10][1 + (2 * i)] = 2
        else: grid[10][1 + (2 * i)] = 1
    
     # Get the twelfth row.
    for i in range(2):
        if sum(pixel[x_vals[2 + (2 * i)], y_vals[11]]) >= 245 and sum(pixel[x_vals[2 + (2 * i)], y_vals[11]]) <= 265: grid[11][2 + (2 * i)] = 2
        else: grid[11][2 + (2 * i)] = 1
    
    # Get the last value.
    if sum(pixel[x_vals[3], y_vals[12]]) >= 245 and sum(pixel[x_vals[3], y_vals[12]]) <= 265: grid[12][3] = 2
    else: grid[12][3] = 1

# Used to flip a value from 1 to 2 or vise versa (used for tapping a button).
def flip(value : int):
    
    if value == 1: return 2
    return 1


def tap(g, y : int, x : int, t : bool):
    
    global numTaps # Points to the global variable.
    if t:
        print(f"{y} {x}")
        pyautogui.moveTo(x_vals[x], y_vals[y])
        pyautogui.click(x_vals[x], y_vals[y])
        numTaps += 1
    
    g[y][x] = flip(g[y][x])
    
    if y > 1:
        g[y - 2][x] = flip(g[y - 2][x])
    if y < 11:
        g[y + 2][x] = flip(g[y + 2][x])
    
    if y != 0:
        if x != 0:
            g[y - 1][x - 1] = flip(g[y - 1][x - 1])
        if x != 6:
            g[y - 1][x + 1] = flip(g[y - 1][x + 1])
    
    if y != 12:
        if x != 0:
            g[y + 1][x - 1] = flip(g[y + 1][x - 1])
        if x != 6:
            g[y + 1][x + 1] = flip(g[y + 1][x + 1])

def propagate(g, actualTap):
    ## PROPAGATE
    if g[0][3] == 2: tap(g, 2, 3, actualTap)
    
    if g[1][2] == 2: tap(g, 3, 2, actualTap)
    if g[1][4] == 2: tap(g, 3, 4, actualTap)
    
    if g[2][1] == 2: tap(g, 4, 1, actualTap)
    if g[2][3] == 2: tap(g, 4, 3, actualTap)
    if g[2][5] == 2: tap(g, 4, 5, actualTap)
    
    for i in range(6):
        
        if i % 2 == 0:
            if g[3 + i][0] == 2: tap(g, 5 + i, 0, actualTap)
            if g[3 + i][2] == 2: tap(g, 5 + i, 2, actualTap)
            if g[3 + i][4] == 2: tap(g, 5 + i, 4, actualTap)
            if g[3 + i][6] == 2: tap(g, 5 + i, 6, actualTap)
        
        else:
            if g[3 + i][1] == 2: tap(g, 5 + i, 1, actualTap)
            if g[3 + i][3] == 2: tap(g, 5 + i, 3, actualTap)
            if g[3 + i][5] == 2: tap(g, 5 + i, 5, actualTap)
    
    if g[9][2] == 2: tap(g, 11, 2, actualTap)
    if g[9][4] == 2: tap(g, 11, 4, actualTap)
    
    if g[10][3] == 2: tap(g, 12, 3, actualTap)

def tap_end():
    pyautogui.moveTo(952, 882)
    pyautogui.click(952, 882)

# Play the game.
def play():
    
    global numTaps
    
    for i in range(NUM_GAMES):
        print(i)
        setGrid() # Get the grid values.
        grid2 = deepcopy(grid)
        numTaps = 0
        
        # Print the grid as a grid.
        for row in grid2:
            print(*row, sep=" ")
        
        print("\n\n")
        
        # PROPAGATE
        propagate(grid2, False)
        
        residue = str(grid2[9][0]) + str(grid2[10][1]) + str(grid2[11][2]) + str(grid2[12][3]) + str(grid2[11][4]) + str(grid2[10][5]) + str(grid2[9][6])
        print(residue)
        
        if residue == "1121211":
            tap(grid, 0, 3, True)
            tap(grid, 3, 6, True)
            #propagate(grid, True)
        elif residue == "1212121":
            tap(grid, 1, 4, True)
            tap(grid, 2, 5, True)
            #propagate(grid, True)
        elif residue == "1222221":
            tap(grid, 0, 3, True)
            tap(grid, 1, 4, True)
            tap(grid, 2, 1, True)
            tap(grid, 3, 6, True)
            #propagate(grid, True)
        elif residue == "2112112":
            tap(grid, 0, 3, True)
            tap(grid, 2, 5, True)
            #propagate(grid, True)
        elif residue == "2122212":
            tap(grid, 0, 3, True)
            #propagate(grid, True)
        elif residue == "2211122":
            tap(grid, 1, 4, True)
            tap(grid, 2, 5, True)
            tap(grid, 3, 6, True)
            #propagate(grid, True)
        elif residue == "2221222":
            tap(grid, 0, 3, True)
            tap(grid, 1, 2, True)
            tap(grid, 2, 5, True)
        
        propagate(grid, True)
        print(numTaps)
        if numTaps == 0:
            time.sleep(0.1)
            pyautogui.moveTo(952, 832)
            pyautogui.click(952, 832)
            continue
        
        tap_end()
        time.sleep(0.03)

time.sleep(PAUSE_BEFORE_GAME) # Pause before playing the game.
play() # Play the game.
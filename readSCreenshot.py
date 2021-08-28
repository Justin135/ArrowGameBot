# Import some modules
import cv2 # An image proccessing library
import pytesseract # an image to text library
import numpy as np # used for mathematics but can be used in image proccessing
import pyautogui
import time
import pyscreenshot

# Positions:
# Top Left: x=750, y=365
# Top Right: x=1165, y=365
# Bottom Left: x=750, y=794
# Bottom Right: x=1165, y=794
# End Button: x=945, y=845

# Configure the module
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

x_coords = [795, 897, 1000, 1104]
y_coords = [405, 510, 610, 715]
buttons = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

pyautogui.PAUSE = 0.005

# Increment the variable (also accounting for if the variable exceeds 4).
def increment(value : int):
    value += 1
    
    if value > 4:
        value = 1
    
    return value

def tap_button(x : int, y : int):
    pyautogui.moveTo(x_coords[x], y_coords[y], duration = 0.001)
    pyautogui.click(x_coords[x], y_coords[y])
    
    buttons[y][x] = increment(buttons[y][x])
    if y != 0: buttons[y - 1][x] = increment(buttons[y - 1][x])
    if y != 3: buttons[y + 1][x] = increment(buttons[y + 1][x])
    
    if x != 0:
        if y != 0: buttons[y - 1][x - 1] = increment(buttons[y - 1][x - 1])
        buttons[y][x - 1] = increment(buttons[y][x - 1])
        if y != 3: buttons[y + 1][x - 1] = increment(buttons[y + 1][x - 1])
    
    if x != 3:
        if y != 0: buttons[y - 1][x + 1] = increment(buttons[y - 1][x + 1])
        buttons[y][x + 1] = increment(buttons[y][x + 1])
        if y != 3: buttons[y + 1][x + 1] = increment(buttons[y + 1][x + 1])
    
    #print(buttons)

def tap_end():
    pyautogui.moveTo(945, 845, duration = 0.001)
    pyautogui.click(945, 845)

# Get all numbers from game.
def get_nums():
    for i in range(4):
        for j in range(4):
            image = pyscreenshot.grab(bbox=(x_coords[j], y_coords[i], x_coords[j] + 20, y_coords[i] + 40)) # Capture the button number.
            image.save("screenshots/" + str((i * 4) + j) + ".png") # Save to file.


#image = pyscreenshot.grab(bbox=(750, 365, 1165, 794)) # Capture the screen.
#image = pyscreenshot.grab(bbox=(795, 400, 820, 440)) # Capture the screen.
#image.save("screen.png") # To save the screenshot

for k in range(5):
    get_nums()
    # Get all the numbers and save them to the buttons 2d array.
    for i in range(4):
        
        for j in range(4):
            img = cv2.imread("screenshots/" + str((i * 4) + j) + ".png") # Read the image.
            buttons[i][j] = pytesseract.image_to_string(img, config="--psm 13")[0] # Gets the first number value.
            
            # Sometimes it'll recognize a 2 as something else.
            if buttons[i][j] == 'i':
                buttons[i][j] = 1
            
            # Sometimes it'll recognize a 2 as something else.
            if buttons[i][j] == 'q' or buttons[i][j] == 'Q':
                buttons[i][j] = 2
            
            # Sometimes it'll recognize a 3 as something else.
            if buttons[i][j] == 'g' or buttons[i][j] == 'g' or buttons[i][j] == '5' or buttons[i][j] == '8' or buttons[i][j] == 'a' or buttons[i][j] == 'B':
                buttons[i][j] = 3
            
            # Sometimes it'll recognize a 4 as something else.
            if buttons[i][j] == 'z' or buttons[i][j] == 'Z' or buttons[i][j] == 'A':
                buttons[i][j] = 4
            
            buttons[i][j] = int(buttons[i][j])
            print(buttons[i][j])


    for i in range(3):
        
        while(buttons[0 + i][0] != buttons[0 + i][1]):
            tap_button(2, 1 + i)

        while(buttons[0 + i][2] != buttons[0 + i][3]):
            tap_button(1, 1 + i)

        if buttons[0 + i][0] == 2:
            for j in range(3): tap_button(0, 1 + i)
        elif buttons[0 + i][0] == 3:
            for j in range(2): tap_button(0, 1 + i)
        elif buttons[0 + i][0] == 4:
            tap_button(0, 1 + i)

        if buttons[0 + i][3] == 2:
            for j in range(3): tap_button(3, 1 + i)
        elif buttons[0 + i][3] == 3:
            for j in range(2): tap_button(3, 1 + i)
        elif buttons[0 + i][3] == 4:
            tap_button(3, 1 + i)

    count = 0
    while(buttons[3][0] != buttons[3][1]):
        tap_button(2, 3)
        count += 1
    
    count = 4 - count
    for i in range(count):
        tap_button(2, 1)

    count = 4 - count
    for i in range(count):
        tap_button(2, 0)

    count = 0
    while(buttons[3][2] != buttons[3][3]):
        tap_button(1, 3)
        count += 1
    
    count = 4 - count
    for i in range(count):
        tap_button(1, 1)

    count = 4 - count
    for i in range(count):
        tap_button(1, 0)

    count = 0
    if buttons[3][0] == 2: count = 3
    elif buttons[3][0] == 3: count = 2
    elif buttons[3][0] == 4: count = 1

    if count != 0:
        for i in range(count):
            tap_button(0, 3)

        count = 4 - count
        for i in range(count):
            tap_button(0, 1)
        
        count = 4 - count
        for i in range(count):
            tap_button(0, 0)

    count = 0
    if buttons[3][3] == 2: count = 3
    elif buttons[3][3] == 3: count = 2
    elif buttons[3][3] == 4: count = 1

    if count != 0:
        for i in range(count):
            tap_button(3, 3)

        count = 4 - count
        for i in range(count):
            tap_button(3, 1)
        
        count = 4 - count
        for i in range(count):
            tap_button(3, 0)
    
    time.sleep(0.1)
    tap_end()
    pyautogui.moveTo(100, 100, duration=0)
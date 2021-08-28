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

# Configure the module
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

x_coords = [795, 897, 1000, 1104]
y_coords = [405, 510, 610, 715]

for i in range(4):
    
    for j in range(4):
        image = pyscreenshot.grab(bbox=(x_coords[j], y_coords[i], x_coords[j] + 20, y_coords[i] + 40)) # Capture the screen.
        image.save("screenshots/" + str((i * 4) + j) + ".png")

# image = pyscreenshot.grab(bbox=(750, 365, 1165, 794)) # Capture the screen.
image = pyscreenshot.grab(bbox=(795, 400, 820, 440)) # Capture the screen.
image.save("screen.png") # To save the screenshot
img = cv2.imread("screen.png")
a1 = pytesseract.image_to_string(img, config="--psm 13")[0] # Works for only one number.
print(a1)


"""

# Make the image grey
img = cv2.imread('your_img.png')
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)
kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
# Use OCR to read the text from the image
out_below = pytesseract.image_to_string(img)
# Print the text
print(out_below)
"""
# Import some modules
import cv2 # An image proccessing library
import pytesseract # an image to text library
import numpy as np # used for mathematics but can be used in image proccessing

# Configure the module
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Justin\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

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
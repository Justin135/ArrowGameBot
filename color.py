import pyautogui, time

def getCurrentPixelColor():
    x, y = pyautogui.position()
    
    # Get the pixel color at the current mouse position
    pixel_color = sum(pyautogui.pixel(500, 450))
    
    return pixel_color


start = time.time()
for i in range(37):
    color = getCurrentPixelColor()
    print(f"{i}: {color}")

end = time.time()

print(end - start)
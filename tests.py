import pyautogui, time

def getPos():
    print(pyautogui.position())

for i in range(1000):
    getPos()
    time.sleep(1.25)

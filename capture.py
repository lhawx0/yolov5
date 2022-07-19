import mss
import time
from win32api import GetAsyncKeyState
from datetime import datetime

with mss.mss() as sct:

    dimensions = sct.monitors[1]
    SQUARE_SIZE = 640

    monitor = {"top": int((dimensions['height'] / 2) - (SQUARE_SIZE / 2)),

               "left": int((dimensions['width'] / 2) - (SQUARE_SIZE / 2)),

               "width": SQUARE_SIZE,

               "height": SQUARE_SIZE}
    while(True):
        idx = 0
        if GetAsyncKeyState(0x14):
            sct_img = sct.grab(monitor)
            dt_string = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
            dt_string += str(idx)
            idx += 1
            output = "C:/Users/H.HUANG/Pictures/Screenshots/" + dt_string + ".png".format(**monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            time.sleep(0.2)
        elif GetAsyncKeyState(0x12):
            time.sleep(0.5)
            sct_img = sct.grab(monitor)
            dt_string = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
            dt_string += str(idx)
            idx += 1
            file_path = "C:/Users/H.HUANG/Pictures/Screenshots/" + dt_string + ".png"
            output = file_path.format(**monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        
        time.sleep(0.05)

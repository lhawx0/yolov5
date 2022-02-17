import math
from unittest import result
import mss
import numpy as np
import torch
import time
import win32api
model = torch.hub.load('C:/Users/H.Huang/yolov5', 'custom', path='C:/Users/H.Huang/yolov5/ballsv2.pt', source='local')


def modifier(distance):
    return 1 + 0.42 * pow(distance, 0.35)


def smooth_move(diffX, diffY):
    stepX, stepY = int(diffX / 50), int(diffY / 50)
    smooth_start = time.time()
    for _ in range(50):
        win32api.mouse_event(0x001, stepX, stepY)
    smooth_time = time.time() - smooth_start
    print("SMO %.6f " % smooth_time)


with mss.mss() as sct:

    # Use the first monitor, change to desired monitor number

    dimensions = sct.monitors[1]

    SQUARE_SIZE = 640

    # Part of the screen to capture

    monitor = {"top": int((dimensions['height'] / 2) - (SQUARE_SIZE / 2)),

               "left": int((dimensions['width'] / 2) - (SQUARE_SIZE / 2)),

               "width": SQUARE_SIZE,

               "height": SQUARE_SIZE}

    # output = "sct_monitor[1]_{top}x{left}_{width}x{height}.png".format(**monitor)

    while True:
        if win32api.GetAsyncKeyState(0x02):
            if win32api.GetAsyncKeyState(0x01):
                start_time = time.time()
                sct_img = sct.grab(monitor)

                # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                # print(output)

                BRGFrame = np.array(sct_img)
                RGBFrame = BRGFrame[:, :, [2, 1, 0]]
                capture_time = time.time() - start_time

                infer_time = time.time()
                results = model(RGBFrame, size=320)
                infer_end = time.time()
                model.conf = 0.8

                enemyNum = results.xyxy[0].shape[0]

                if enemyNum == 0:
                    pass
                else:
                    closest = 1000

                    for i in range(enemyNum):
                        x1 = float(results.xyxy[0][i, 0])
                        y1 = float(results.xyxy[0][i, 1])
                        x2 = float(results.xyxy[0][i, 2])
                        y2 = float(results.xyxy[0][i, 3])

                        centerX = (x2 - x1) / 2 + x1
                        centerY = (y2 - y1) / 2 + y1

                        distance = math.sqrt(((centerX - SQUARE_SIZE / 2) ** 2) + ((centerY - SQUARE_SIZE / 2) ** 2))

                        if distance < closest:
                            closest = distance
                            target = i

                    x1 = float(results.xyxy[0][target, 0])
                    y1 = float(results.xyxy[0][target, 1])
                    x2 = float(results.xyxy[0][target, 2])
                    y2 = float(results.xyxy[0][target, 3])

                    Xtarget = (x2 - x1) / 2 + x1
                    Ytarget = (y2 - y1) / 2 + y1

                    MODIFIER = modifier(distance)

                    diffX = int(MODIFIER * (Xtarget - SQUARE_SIZE / 2))
                    diffY = int(MODIFIER * (Ytarget - SQUARE_SIZE / 2))
                    calculate_time = time.time() - infer_end
                    if(distance >= 50):
                        smooth_move(diffX, diffY)
                    else:
                        win32api.mouse_event(0x001, diffX, diffY)

                    print("--- %.3f seconds ---" % (time.time() - start_time))
                    print("CAP %.3f " % capture_time +
                          "INF %.3f " % (infer_end - infer_time) +
                          "CAL %.3f " % calculate_time +
                          "MOV %0.3f" % (time.time() - start_time - capture_time - infer_end + infer_time - calculate_time))

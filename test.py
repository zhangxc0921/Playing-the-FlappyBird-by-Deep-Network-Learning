import time

import win32gui, win32con, win32api, win32ui
from win32clipboard import *
import cv2
import numpy as np
from PIL import Image
import pygame

class GameAssist:

    def __init__(self, wdname):
        """初始化"""

        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()
        # 窗口显示最前面
        win32gui.SetForegroundWindow(self.hwnd)

    def window_capture(self):  # 获取屏幕像素，返回黑白图
        hwnd = self.hwnd
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        rctA = win32gui.GetWindowRect(hwnd)
        w = rctA[2] - rctA[0]
        h = rctA[3] - rctA[1]
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (h, w, 4)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        Grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 先要转换为灰度图片
        ret, thresh = cv2.threshold(Grayimg, 30, 255, cv2.THRESH_BINARY)  # 这里的第二个参数要调，是阈值！！
        return thresh


if __name__ == "__main__":
    # wdname 为连连看窗口的名称，必须写完整
    wdname = u'Flappy Bird'
    demo = GameAssist(wdname)
    step = 0
    clock = pygame.time.Clock()
    while True:
        step += 1
        A = demo.window_capture()
        print(type(A))
        im = Image.fromarray(A)
        im.save(f'./img/test_{step}.jpg')
        clock.tick(30)
        print(step)

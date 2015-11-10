# -*- coding:utf-8 -*-
# http://stackoverflow.com/questions/1181464/controlling-mouse-with-python#1181464
import ctypes
import win32gui
import time
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event

def left_click(x, y, clicks=1):
    SetCursorPos(x, y)
    for i in range(clicks):
        mouse_event(2, 0, 0, 0, 0)
        mouse_event(4, 0, 0, 0, 0)
        mouse_event(2, 0, 0, 0, 0)
        mouse_event(4, 0, 0, 0, 0)
        #mouse_event(3, 0, 0, 0, 0)

left_click(141, 570) #left clicks at 200, 200 on your screen. Was able to send 10k clicks instantly.
# time.sleep(5)
# print(win32gui.GetCursorInfo())



# import win32api, win32con
# def click(x,y):
#     win32api.SetCursorPos((x,y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
# click(143, 574)
import time
import keyboard
import mouse
import pyautogui as pag

class MouseKeyboard(mouse.MouseAction, keyboard.KeyAction):

    # CTRL + 鼠标中键滚轮 = 实现放大缩小页面的功能
    def keyscroll(self, key):
        self.keypress(key)
        self.scroll("UP", 2)
        self.keyrelease(key)

    # SHIFT + 鼠标点击 鼠标移动 = 实现同时点击多个目标的功能
    def keyclick(self, key):
        self.keypress(key)
        self.click()
        self.vector_move((0, 20), "GYS")
        self.click()
        self.keyrelease(key)

    # 寻找鼠标位置
    def find_mouse(self):
        x, y = pag.position()
        mouse_pos = (x, y)
        return mouse_pos

    # 寻找控件位置
    def find_box(self, box):
        Jsontext = self.json
        for i in range(len(Jsontext)):
            if Jsontext[i]["ocr"].find(box) >= 0:
                return int(Jsontext[i]["x"]), int(Jsontext[i]["y"])
        return 0, 0

    # 移动到目标控件的位置，并点击
    def touch(self, box):
        x, y = self.find_box(box)
        box_pos = (x, y)
        mouse_pos = self.find_mouse()
        self.vector_v1tov2_abs(mouse_pos, box_pos, "GYS")
        self.click()

    # 完整的输入操作，先移动到输入框，再输入
    def input(self, box, key):
        self.touch(box)
        self.keyevent("LSHIFT")
        self.text(key)

    def connect(self, host, username, password):
        # open Filezilla
        self.click()
        self.vector_v1tov2_abs((1578, 28), (34, 436), 'GYS')
        self.double_click()
        # move to host
        self.vector_v1tov2_abs((34, 436), (74, 89), 'GYS')
        self.click()
        self.text(host)
        time.sleep(1)
        # move to username
        self.vector_v1tov2_abs((74, 89), (249, 86), 'GYS')
        self.click()
        self.text(username)
        time.sleep(1)
        # move to password
        self.vector_v1tov2_abs((249, 86), (457, 87), 'GYS')
        self.click()
        self.text(password)
        time.sleep(1)
        # move to quickconnect
        self.vector_v1tov2_abs((457, 87), (654, 88), 'GYS')
        self.click()

# -*- coding: utf-8 -*-

"""Keyboard input emulation module
"""

import time

# 发送数据
def send_data(t, op_data, sleep_time):
    n = t.write(bytes.fromhex(op_data))
    time.sleep(sleep_time) #发送到接收的时间，有待确定
    num = t.inWaiting()
    data = t.read(num)
    if num > 0:
        out_s = ''
        for i in range(0, len(data)):
            out_s = out_s + '{:02X}'.format(data[i]) + ' '
        print(out_s)
        
# 键盘指令
dict_keyboard = {
    'KEYBOARD': '57AB01050101',
    'KEYPRESS': '57AB01040102',
    'KEYRELEASE': '57AB01040103',
    'GETLIGHT': '57AB01030104',
    'SETLIGHT': '57AB01040105'
}

# 键盘键值
CODES = {
    'a': '04',
    'b': '05',
    'c': '06',
    'd': '07',
    'e': '08',
    'f': '09',
    'g': '0A',
    'h': '0B',
    'i': '0C',
    'j': '0D',
    'k': '0E',
    'l': '0F',
    'm': '10',
    'n': '11',
    'o': '12',
    'p': '13',
    'q': '14',
    'r': '15',
    's': '16',
    't': '17',
    'u': '18',
    'v': '19',
    'w': '1A',
    'x': '1B',
    'y': '1C',
    'z': '1D',

    'A': '04',
    'B': '05',
    'C': '06',
    'D': '07',
    'E': '08',
    'F': '09',
    'G': '0A',
    'H': '0B',
    'I': '0C',
    'J': '0D',
    'K': '0E',
    'L': '0F',
    'M': '10',
    'N': '11',
    'O': '12',
    'P': '13',
    'Q': '14',
    'R': '15',
    'S': '16',
    'T': '17',
    'U': '18',
    'V': '19',
    'W': '1A',
    'X': '1B',
    'Y': '1C',
    'Z': '1D',

    '1': '1E',
    '2': '1F',
    '3': '20',
    '4': '21',
    '5': '22',
    '6': '23',
    '7': '24',
    '8': '25',
    '9': '26',
    '0': '27',

    'ENTER': '28',
    'ESC': '29',
    'BACKSPACE': '2A',
    'TAB': '2B',
    'BLANKSPACE': '2C',
    ' ': '2C',
    '-': '2D',
    '=': '2E',
    '[': '2F',
    ']': '30',
    '\\': '31',
    ';': '33',
    "'": '34',
    '`': '35',
    ',': '36',
    '.': '37',
    '/': '38',
    'CAPSLOCK': '39',

    'F1': '3A',
    'F2': '3B',
    'F3': '3C',
    'F4': '3D',
    'F5': '3E',
    'F6': '3F',
    'F7': '40',
    'F8': '41',
    'F9': '42',
    'F10': '43',
    'F11': '44',
    'F12': '45',

    'PRINTSCREEN': '46',
    'SCROLLLOCK': '47',
    'PAUSE': '48',
    'INSERT': '49',
    'HOME': '4A',
    'PGUP': '4B',
    'DELETE': '4C',
    'END': '4D',
    'PGDN': '4E',
    'RARROW': '4F',
    'LARROW': '50',
    'DARROW': '51',
    'UARROW': '52',
    'NUMLOCK': '53',
    'NUMPAD_/': '54',
    'NUMPAD_*': '55',
    'NUMPAD_-': '56',
    'NUMPAD_+': '57',
    'NUMPAD_ENTER': '58',
    'NUMPAD_1': '59',
    'NUMPAD_2': '5A',
    'NUMPAD_3': '5B',
    'NUMPAD_4': '5C',
    'NUMPAD_5': '5D',
    'NUMPAD_6': '5E',
    'NUMPAD_7': '5F',
    'NUMPAD_8': '60',
    'NUMPAD_9': '61',
    'NUMPAD_0': '62',
    'NUMPAD_.': '63',

    'LCTRL': 'E0',
    'LSHIFT': 'E1',
    'LALT': 'E2',
    'LWINDOWS': 'E3',
    'RCTRL': 'E4',
    'RSHIFT': 'E5',
    'RALT': 'E6',
    'RWINDOWS': 'E7'

}

# 组合才能打出的键值
CODES_COMBINE = {
    '!': '1E',
    '@': '1F',
    '#': '20',
    '$': '21',
    '%': '22',
    '^': '23',
    '&': '24',
    '*': '25',
    '(': '26',
    ')': '27',
    '_': '2D',
    '+': '2E',
    '{': '2F',
    '}': '30',
    '|': '31',
    ':': '33',
    '"': '34',
    '~': '35',
    '<': '36',
    '>': '37',
    '?': '38',
    'NUMPAD_END': '59',
    'NUMPAD_DARROW': '5A',
    'NUMPAD_PGDN': '5B',
    'NUMPAD_LARROW': '5C',
    'NUMPAD_RARROW': '5E',
    'NUMPAD_HOME': '5F',
    'NUMPAD_UARROW': '60',
    'NUMPAD_PGUP': '61',
    'NUMPAD_INSERT': '62'

}

'''
命令格式：
text(hellpfagjaogen)
'''
class KeyAction(object):

    """Class that represents a single keyboard action
    It represents either a keyboard action (press or release or both) of a particular key.
    """

    def __init__(self, serial):
        self.s = serial
    # 输入内容
    def text(self, key, enter = False, interval = 0.25, **kwargs):
        self.setlight()
        for input_char in key:
            if input_char in CODES.keys():
                if input_char.isupper():
                    op_data = dict_keyboard["KEYBOARD"] + CODES["CAPSLOCK"] + "01"  # 切换大小写
                    send_data(self.s, op_data, 0)
                    op_data = dict_keyboard["KEYBOARD"] + CODES[input_char] + "05"
                    send_data(self.s, op_data, interval)
                    op_data = dict_keyboard["KEYBOARD"] + CODES["CAPSLOCK"] + "01"  # 切换大小写
                    send_data(self.s, op_data, 0)
                    time.sleep(interval)
                else:
                    op_data = dict_keyboard["KEYBOARD"] + CODES[input_char] + "05"
                    send_data(self.s, op_data, interval)
                    time.sleep(interval)
            elif input_char in CODES_COMBINE.keys():
                self.keypress("LSHIFT")
                op_data = dict_keyboard["KEYPRESS"] + CODES_COMBINE[key]  # 按下
                send_data(self.s, op_data, 0)
                op_data = dict_keyboard["KEYRELEASE"] + CODES_COMBINE[key]  # 按下
                send_data(self.s, op_data, 0)
                self.keyrelease("LSHIFT")
                time.sleep(interval)
            else:
                raise ValueError("Wrong move_type!")
        if enter:
            op_data = dict_keyboard["KEYBOARD"] + CODES["ENTER"] + "01"  # 切换大小写
            send_data(self.s, op_data, 0)
        time.sleep(2)

    # 键盘 按下单个功能键并释放
    def keyevent(self, key, **kwargs):
        op_data = dict_keyboard["KEYBOARD"] + CODES[key] + "02"
        send_data(self.s, op_data, 1)

    # 键盘按下与释放
    def keypress(self, key, **kwargs):
        op_data = dict_keyboard["KEYPRESS"] + CODES[key]  # 按下
        send_data(self.s, op_data, 0)

    def keyrelease(self, key, **kwargs):
        op_data = dict_keyboard["KEYRELEASE"] + CODES[key]  # 弹起
        send_data(self.s, op_data, 0)

    # 键盘 同时按下1，2，3个键
    def keydouble(self, key1, key2, **kwargs):
        self.keypress(key1)  # 按下1
        self.keypress(key2)  # 按下2
        self.keyrelease(key1)  # 按下1
        self.keyrelease(key2)  # 按下2
        time.sleep(1)

    def keytriple(self, key1, key2, key3, **kwargs):
        self.keypress(key1)  # 按下1
        self.keypress(key2)  # 按下2
        self.keypress(key3)  # 按下3
        self.keyrelease(key1)  # 按下1
        self.keyrelease(key2)  # 按下2
        self.keyrelease(key3)  # 按下3
        time.sleep(1)

    # 获取键盘灯状态
    def getlight(self):
        self.s.write(bytes.fromhex(dict_keyboard["GETLIGHT"]))
        time.sleep(1)
        num = self.s.inWaiting()  # 返回接收缓存中的字节数
        data = self.s.read(num)
        if num > 0:
            out_s = ''
            for i in range(0, len(data)):
                out_s = out_s + '{:02X}'.format(data[i]) + ' '
            print(out_s)
            #目标 NumLock on, CapsLock Off
            if out_s == '00':
                print("NumLock:off, CapsLock:off")
            elif out_s == '01':
                print("NumLock:on, CapsLock:off")
            elif out_s == '02':
                print("NumLock:off, CapsLock:on")
            else:
                print("NumLock:on, CapsLock:on")
                
    # 设置键盘灯状态
    def setlight(self):
        op_data = dict_keyboard["SETLIGHT"] + "01"
        send_data(self.s, op_data, 0)






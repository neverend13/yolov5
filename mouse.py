# GUI Application automation and testing library
# -*- coding: utf-8 -*-

"""Keyboard input emulation module
"""

import time
import keyboard
import pyautogui

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

# 鼠标指令
dict_mouse = {
    'LEFTRIGHT': '57AB01060205',
    'UPDOWN': '57AB01060206',
    'CLICK': '57AB01050201',
    'PRESS': '57AB01040202',
    'RELEASE': '57AB01040203',
    'LEFT': '01',
    'RIGHT': '02',
    'MID': '04',
    'UP': '57AB0104020401',
    'DOWN': '57AB01040204FF',
}

# 10进制转16进制
def hex_change(val):
    if val < 0:
        dirct = '00'  # 负数 左 上
        dist = '{:04x}'.format(int(hex(abs(val)), 16), 'x')  # 进制转换
    else:
        dirct = '01'
        dist = '{:04x}'.format(int(hex(abs(val)), 16), 'x')  # 进制转换
    hex_val = dirct + dist  # 直接是转换成的十六进制数，包括方向、数值
    return hex_val

#####################################################################################
# gys 公因数方法
# 获取两个数的最大公因数
def get_gongyinshu(num1, num2):
    # 如果一个方向移动距离为0，则返回非零值，作为移动距离，可能移动次数过多
    if num1 == 0:
        return num2
    if num2 == 0:
        return num1
    if num1 < num2:  # 判读两个整数的大小,目的为了将大的数作为除数,小的作为被除数
        num1, num2 = num2, num1  # 如果if条件满足,则进行值的交换
    vari = num1 % num2  # 对2个整数进行取余数
    while vari != 0:  # 判断余数是否为0, 如果不为0,则进入循环
        num1 = num2  # 重新进行赋值,进行下次计算
        num2 = vari
        vari = num1 % num2  # 对重新赋值后的两个整数取余数
        # 直到 vari2 等于0,得到最大公约数就退出循环
    return num2

def get_dist_sum_gys(total, dirct):
    total = int(total)
    list = []
    if dirct > 0:
        step = int(dirct / total)
    elif dirct < 0:
        step = int(dirct / total)
    else:
        step = 0
    print("each step: {} , total: {} ".format(step, total))
    for i in range(total):
        list_value = step
        # print(list_value)
        list.append(list_value)
    return list

#################################################################################3
# JXZ  较小值 两步走方法
def get_min(num1, num2):
    leave = 0  # 留下的
    if num1 > num2:
        leave = 1
        return num2, num1 - num2, leave
    else:
        return num1, num2 - num1, leave

def get_dist_sum_jxz(total_dist, dirct):
    list = []
    total_dist = int(total_dist)
    if dirct > 0:
        step = 1
    elif dirct < 0:
        step = -1
    else:
        step = 0
    #print("each step: {} , total: {} ".format(step, total_dist))
    for i in range(total_dist):
        list_value = step
        # print(list_value)
        list.append(list_value)
    return list
######################################################################################

class MouseAction(object):

    """Class that represents a single mouse action
    It represents either a keyboard action (press or release or both) of a particular key.
    """
    def __init__(self, serial, json):
        self.s = serial
        self.json = json

    def click(self, buttons = "LEFT", times = 1, duration = "02"):
        for scroll_time in range(int(times)):
            op_data = dict_mouse['CLICK'] + dict_mouse[buttons] + duration
            send_data(self.s, op_data, 0)
            time.sleep(0.5)
        time.sleep(2)

    def double_click(self, duration = "02"):
        op_data = dict_mouse['CLICK'] + dict_mouse["LEFT"] + duration
        send_data(self.s, op_data, 0)
        send_data(self.s, op_data, 0)
        time.sleep(5)  # 根据打开的软件不同，时间不同

    def press(self, buttons = "LEFT"):
        op_data = dict_mouse['PRESS'] + dict_mouse[buttons]
        send_data(self.s, op_data, 0)

    def release(self, buttons = "LEFT"):
        op_data = dict_mouse['RELEASE'] + dict_mouse[buttons]
        send_data(self.s, op_data, 0)

    # 鼠标 滚动 向上/向下 加次数
    def scroll(self, scroll_dirct, times = 1):
        for scroll_time in range(int(times)):
            op_data = dict_mouse[scroll_dirct]
            send_data(self.s, op_data, 0)
            time.sleep(0.5)
        time.sleep(1)

    # 矢量移动
    def vector_move(self, vector, move_type, **kwargs):

        dir_num1 = int(vector[0])  # 左右的总距离,-398
        dir_num2 = int(vector[1])  # 上下的总距离，76

        if move_type == 'GYS':
            step_gys = get_gongyinshu(abs(dir_num1), abs(dir_num2))  # 最大公约数
            data_num1 = get_dist_sum_gys(step_gys, dir_num1)
            data_num2 = get_dist_sum_gys(step_gys, dir_num2)

            for i in range(step_gys):
                op_data1 = dict_mouse['LEFTRIGHT'] + hex_change(data_num1[i])
                send_data(self.s, op_data1, 0.01)
                op_data2 = dict_mouse['UPDOWN'] + hex_change(data_num2[i])
                send_data(self.s, op_data2, 0.01)
                time.sleep(0.05)
            time.sleep(0.1)

        elif move_type == "JXZ":
            step_min, step_leave, leave = get_min(abs(dir_num1), abs(dir_num2))  # 先较小数移动

            print("step_min:{}, step_leave:{}, leave:{}".format(step_min, step_leave, leave))
            data_num1 = get_dist_sum_jxz(step_min, dir_num1)
            data_num2 = get_dist_sum_jxz(step_min, dir_num2)

            # 比较两个数取较小值，矢量的移动，上下左右单位移动值为1
            for i in range(step_min):
                op_data1 = dict_mouse['LEFTRIGHT'] + hex_change(data_num1[i])
                send_data(self.s, op_data1, 0.01)
                op_data2 = dict_mouse['UPDOWN'] + hex_change(data_num2[i])
                send_data(self.s, op_data2, 0.01)
            # 较大数剩余值的移动
            for j in range(step_leave):
                if leave == 1:
                    leave_data_num1 = get_dist_sum_jxz(step_leave, dir_num1)
                    op_data1 = dict_mouse['LEFTRIGHT'] + hex_change(leave_data_num1[j])
                    send_data(self.s, op_data1, 0.001)
                else:
                    leave_data_num2 = get_dist_sum_jxz(step_leave, dir_num2)
                    op_data2 = dict_mouse['UPDOWN'] + hex_change(leave_data_num2[j])
                    send_data(self.s, op_data2, 0.001)
            time.sleep(2)
        else:
            raise ValueError("Wrong move_type!")

    # 相对距离
    def vector_move_per(self, percentage, move_type, **kwargs):
        #  v(0.14,0.89)
        # 获取当前屏幕分辨率
        screenWidth, screenHeight = pyautogui.size()
        vector = (percentage[0] * screenWidth, percentage[1] * screenHeight)
        self.vector_move(vector, move_type)

    # v1 to v2 输入的是坐标，计算距离
    # 绝对距离 absolute coordinates (x, y)
    def vector_v1tov2_abs(self, v1, v2, move_type, **kwargs):
        # v1(1360,861) to v2(2069,353)
        vector = (v2[0] - v1[0], v2[1] - v1[1])
        self.vector_move(vector, move_type)

    # 相对距离 percentage of screen e.g.(0.5, 0.5) 输入的是坐标，计算距离
    def vector_v1tov2_per(self, v1, v2, move_type, **kwargs):
        # v1(0.4,0.34) to v2(0.14,0.89)
        # 获取当前屏幕分辨率
        screenWidth, screenHeight = pyautogui.size()
        dir_LR = (v2[0] - v1[0]) * screenWidth
        dir_UD = (v2[1] - v1[1]) * screenHeight
        vector = (dir_LR, dir_UD)
        self.vector_move(vector, move_type)

    def vector_pytween(self, v1, v2):
        pytween.getPointOnLine(v1[0], v1[1], v2[0], v2[1], 0.25)

    # 矢量拖动
    def vector_drag(self, v1, v2, move_type, **kwargs):
        self.press()
        time.sleep(1)
        self.vector_v1tov2_abs(v1, v2, move_type)
        self.release()



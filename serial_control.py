import pyautogui
import pyautogui as pag
import serial.tools.list_ports
from detect1 import run
import api

'''
serial_control.py
mouse.py
keyboard.py
将发送数据的函数放在mouse.keyboard文件中，然后传递串口名，即可实现单向调用（serial_control调用mouse,keyboard）
'''
# 串口检测
img = pyautogui.screenshot(region=[0, 0, 2160, 1440])  # x,y,w,h
img.save('data/gui/1.jpg')
port_list = list(serial.tools.list_ports.comports())
if len(port_list) == 0:
    print('无可用串口')
else:
    for i in range(0, len(port_list)):
        if port_list[i][1][0] == "U":
            port_label = port_list[i][0]
# 打开串口
t = serial.Serial(port_label, 115200)
print("可用串口为:", t.portstr)


# 读".txt"文件，获取输入数据
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename, 'r', encoding='UTF-8')
    except IOError:
        error = []
        return error
    content = file.readlines()
    for i in range(len(content)-1):
        content[i] = content[i][:len(content[i])-1]
    if len(content)!=1:
        content[i] = content[i][:len(content[i])]
    file.close()
    return content

# 读取指令
data_path = ".\data.txt"
data_all = text_read(data_path)  # 读完整数据
print(data_all)
data_len = len(data_all)

# 实例化鼠标和键盘

dataJsontest = run('best.pt', 'data/gui')
mk = api.MouseKeyboard(t,dataJsontest)

for i in range(data_len):
    data_get = data_all[i]
    print(data_get) #k.keyevent("ENTER")
    #op = data_get.split(',')
    if data_get != "":
        exec(data_get)

# 关闭串口
serial.Serial.close(t)

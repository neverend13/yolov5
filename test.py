from detecttree import run
import json
import pyautogui
import cv2


# img = pyautogui.screenshot(region=[0, 0, 2160, 1440])  # x,y,w,h
# img.save('data/gui/1.jpg')


def find_ocr(ocr, Jsontext):
    for i in range(len(Jsontext)):
        if Jsontext[i]["ocr"].find(ocr) >= 0:
            print(Jsontext[i]["x"])
            print(Jsontext[i]["y"])
            return Jsontext[i]["x"], Jsontext[i]["y"]
    return 0, 0

source = 'data/gui/1.jpg'
im = cv2.imread(source)
img = im[248:580,0:1104]
dataJsontest = run('runs/train/treeview/best.pt', 'data/gui/')
find_ocr("用户名", dataJsontest)

#print(json.dumps(dataJsontest, indent=4, ensure_ascii=False))

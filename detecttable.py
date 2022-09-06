import json
import os

import cv2
from aip import AipOcr

APP_ID = "25861491"
API_Key = "Z54zW5i5heoTCDkcNUO0OFsc"
Secret_Key = "lMEhnGCN52G6DcXYn7ZRV7oHLT7ZfviM"
aipOcr = AipOcr(APP_ID, API_Key, Secret_Key)


def runTable(directory_name, lurd):
    for filename in os.listdir(directory_name):
        im = cv2.imread(directory_name + "/" + filename)
        image = im[int(lurd[1]):int(lurd[3]), int(lurd[0]):int(lurd[2])]
        success, encoded_image = cv2.imencode(".png", image)
        # 将数组转为bytes
        img_bytes = encoded_image.tobytes()
        result = aipOcr.accurate(img_bytes)
        mywords = result["words_result"]
        tabledata = {}  # 用字典格式储存数据
        count = 0  # 记录会被储存的table GUI的个数
        for index in range(len(mywords)):
            left = mywords[index]['location']['left']
            top = mywords[index]['location']['top']
            width = mywords[index]['location']['width']
            height = mywords[index]['location']['height']
            ocr = mywords[index]["words"]
            if index == 0:
                x = saveOCR(left, width, top, height, lurd[0], lurd[1], ocr)
                tabledata['Table' + str(count)] = x
                count += 1
                continue;
            if left < mywords[index - 1]['location']['left'] and top - mywords[index - 1]['location']['top'] > 5:
                x = saveOCR(left, width, top, height, lurd[0], lurd[1], ocr)
                tabledata['Table' + str(count)] = x
                count += 1
            elif left - mywords[index - 1]['location']['left'] < 5 and top > mywords[index - 1]['location']['top']:
                x = saveOCR(left, width, top, height, lurd[0], lurd[1], ocr)
                tabledata['Table' + str(count)] = x
                count += 1
    return tabledata


def saveOCR(left, width, top, height, oldx, oldy, ocr):
    y = {'x': int(left + width / 2 + oldx), 'y': int(top + height / 2 + oldy),
         'w': int(width), 'h': int(height),
         'ocr': ocr}
    return y

import cv2
from detectconnect import run
import postData
from utils.torch_utils import select_device
from models.experimental import attempt_load, Ensemble
from models.yolo import Model


class Mes:
    """信息类中的每个对象主要有两个参数，mis_address与mis_json
        mis_address是图片储存的位置
        mis_json是返回给主机的包含GUI元素位置与OCR信息的json数据
        mis_type是获取数据的方式，先以detect为主"""

    def __init__(self, mis_type, mis_address, task_id, weightpath, model):
        self.mis_type = mis_type
        self.mis_address = mis_address
        self.task_id = task_id
        self.weightpath = weightpath
        self.model = model

    def getmeseasy(self):
        if self.mis_type == "detect":
            pictureResult = postData.post("http://192.168.1.141:8991/picture/post/", "python",
                                          {"host_name": "zcr", "task_type": "screen", "address": self.mis_address,
                                           "id": self.task_id}).json()
            if pictureResult.get('success'):
                mis_json = self.detect()
                return mis_json
            # postData.post("http://192.168.1.169:9001/detect_request", "python", {"id": self.task_id, "mes": mis_json})
        else:
            print("mes_type is not define")

    def detect(self):
        dataJson = run(self.weightpath, self.mis_address, self.model)
        return dataJson

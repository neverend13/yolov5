import os
import random
from utils.torch_utils import select_device
from models.experimental import attempt_load, Ensemble
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
import datetime
from mes import Mes
import postData

app = FastAPI()
address = 'D:\\pic\\'
weightpath = 'runs/train/filezilla/best.pt'


class Model:
    def __init__(self):
        self.half = False
        self.model = Ensemble()
        self.treemodel = Ensemble()

    def run(self):
        device = select_device(0)
        self.half &= device.type != 'cpu'
        self.model = attempt_load(weightpath, map_location=device)



class PostData(BaseModel):
    host_name: str
    task_type: str
    # call_type: str


loadmodel = Model()


# 在应用程序启动时使用FastAPI startup event调用全局类的初始化参数
@app.on_event('startup')
def init_model():
    loadmodel.run()
    return loadmodel


@app.get("/mes/get")
async def read_item(host_name: str, task_type: str):
    id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mes = Mes(task_type, address, id, weightpath,loadmodel.model)
    mes.getmeseasy()
    return {"zcr收到" + host_name + "！用" + task_type + "进行采集"}


@app.post("/mes/posteasy")
async def read_item(data: PostData):
    id = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    if data.host_name == "st":
        mes = Mes(data.task_type, address, id, weightpath,loadmodel.model)
        mis_json = mes.getmeseasy()
        os.remove(address + id + '.png')
        return mis_json
    else:
        return {'host_name is not define'}


@app.post("/mes/post")
async def read_item(data: PostData):
    id = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    if data.host_name == "st":
        mes = Mes(data.task_type, address, id, weightpath,loadmodel.model)
        mis_json = mes.getmeseasy()
        os.remove(address + id + '.png')
        return mis_json
    else:
        return {'host_name is not define'}
    # return {"zcr收到+" + data.host_name + "！用" + data.task_type + "进行采集!项目id" + time}
    # result = calculate_task_dispatch(data.task_name, [data.json_file, data.call_type])
    # # result = test_http(json_file, call_type)
    # return {"calculate_result": result}


if __name__ == "__main__":
    uvicorn.run(app='service:app', host='0.0.0.0', port=8992, reload=True, debug=True)
    # uvicorn.run(app='main:app', host='127.0.0.1', port=8999, reload=True, debug=True)++

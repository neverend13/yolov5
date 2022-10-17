import json
import requests

Python_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
SpringBoot_headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def post(url, server_type="Python", request_data=None):
    if request_data is None:
        request_data = {}
    headers = None
    query = "?"
    query += "host_name=zcr&host_module=detect"
    if server_type.lower() == "python":
        headers = Python_headers
        request_data = json.dumps(request_data)
    elif server_type.lower() == "springboot":
        headers = SpringBoot_headers
    else:
        print("server_type is not define!")
    response = requests.post(url=url+query, headers=headers, data=request_data)
    return response

def get(url, server_type="Python", request_data=None):
    if request_data is None:
        request_data = {}
    query = "?"
    headers = None
    for k, v in request_data.items():
        query += (k + "=" + v + "&")
    url += query
    if server_type.lower() == "python":
        headers = Python_headers
    elif server_type.lower() == "springboot":
        headers = SpringBoot_headers
    else:
        print("server_type is not define!")
    response = requests.get(url=url, headers=headers)
    return response


if __name__ == "__main__":
    #print(post("http://127.0.0.1:8888/post", "SpringBoot", {"name": "wwwqqq"}).text)
    #print(get("http://127.0.0.1:8888/", "SpringBoot", {"task_name": "wwwqqq", "json_file": "wwwqqq",
                                                       # "call_type": "wwwqqq", }).text)
    #print(post("http://192.168.1.169:9001//detect_request", "python", {"host_name": "wwwqqq","task_type":"photo"}).text)
    # print(post("http://192.168.1.141:8992/mes/post/", "python",
    #               {"host_name": "zcr", "task_type": "detect"}).text)
    mes = post("http://192.168.1.141:8991/picture/post/", "python",
         {"host_name": "zcr", "task_type": "screen", "address": 'D:\\pic\\',
          "id": "123"}).json()
    print(mes.get('success'))
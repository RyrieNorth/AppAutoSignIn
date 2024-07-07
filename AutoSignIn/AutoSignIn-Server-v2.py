import requests,json,logging

# 预定义 user tokens, user agents, user IDs, message APIs
api_tokens = [
  
]

user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307001d)"
]
user_ids = [
  
]

message_apis = [
  
]

# 设置小程序API，json信息
app_url = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/ComApi/PostObject"
headers = {
    "Host": "gzsx.qidisoft.cn",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "http://gzsx.qidisoft.cn/WXPlatGZSXStu/dist/index.html",
    "Accept-Encoding": "gzip, deflate",
}

# 记录日志
logging.basicConfig(filename='app.log', level=logging.ERROR)

# 将 user tokens, user agents, user IDs 打包为一个元组,并迭代循环
for api_token, user_agent, user_id, message_api in zip(api_tokens, user_agents, user_ids, message_apis):
    # Set the apitoken and user-agent headers
    headers["apitoken"] = api_token
    headers["User-Agent"] = user_agent

    # 将UserID传递进有效Payload(有效载荷)中
    payload = {
        "apiName": "gzsxWebApi.DoSignin",
        "UserID": user_id,
        "lat": "",
        "lng": "",
        "distance": "",
        "accuracy": "",
        "address": "",
        "type": 1,
        "locationStatus": "1",
        "signinStatus": "1",
        "remark": "",
        "fileJson": "[]"
    }

    # 发送请求，判断是否签到成功，若成功将签到成功信息推送至Server酱，不成功则发送错误信息提醒
    try:
        response = requests.post(url=app_url, json=payload, headers=headers)
        response.raise_for_status()
        js = response.json()
        if js.get("status") == "success":
            # Send a success message to the user
            user_mes_api = f"https://sctapi.ftqq.com/{message_api}title=今日的小程序签到已完成！！！"
            requests.get(url=user_mes_api)
        else:
            # Send an error message to the user
            user_mes_api = f"https://sctapi.ftqq.com/{message_api}title=今日的小程序签到失败，请检查是否配置正确！！！"

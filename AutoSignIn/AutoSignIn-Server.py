#!/usr/bin/python3 
import requests,json

##定义用户Tokens字典
ApiTokens = [
  
]

##定义UA代理字典
UserAgents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307001d)"
]

##定义UserID字典
UserIDs = [
  
]

##定义消息提示API字典
MessageAPIs = [
  
]

##设置小程序API，json信息
AppURL = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/ComApi/PostObject"

##将Tokens,User_IDs,Message_APIS打包为一个元组,并迭代循环
for Api_Tokens,User_IDs,Message_APIs in zip(ApiTokens,UserAgents,UserIDs,MessageAPIs):

    ##设置HTTP请求头
    Headers = {
        "Host": "gzsx.qidisoft.cn",
        "Connection": "keep-alive",
        "apitoken": f"{Api_Tokens}",
        "User-Agent": f"{User_Agents}",
        "Content-Type": "application/json;charset=UTF-8",
        "Referer": "http://gzsx.qidisoft.cn/WXPlatGZSXStu/dist/index.html",
        "Accept-Encoding": "gzip, deflate",
    }

    ##将UserID传递进有效Payload(有效载荷)中
    PayLoad = {
        "apiName":"gzsxWebApi.DoSignin",
        "UserID":f"{User_IDs}",
        "lat":"",
        "lng":"",
        "distance":"",
        "accuracy":"",
        "address":"",
        "type":1,
        "locationStatus":"1",
        "signinStatus":"1",
        "remark":"",
        "fileJson":"[]"
    }

    ##将字典转换为json字符串并请求
    Data = json.dumps(PayLoad)
    Res = requests.post(url=AppURL,data=Data,headers=Headers).text
    #print (Res)

    ##判断是否签到成功,若成功将签到成功信息推送至Server酱,不成功则发送错误信息提醒
    Js = json.loads(Res)
    if Js.get("status") == "success":
        ##print (Js.get("status"))
        UserMesApi = f"https://sctapi.ftqq.com/{Message_APIs}title=今日的小程序签到已完成！！！"
        Mes = requests.get(url=UserMesApi).text
        ##print (Mes)
    else:
        UserMesApi = f"https://sctapi.ftqq.com/{Message_APIs}title=今日的小程序签到失败，请检查是否配置正确！！！"
        Mes = requests.get(url=UserMesApi).text
        ##print (Mes)

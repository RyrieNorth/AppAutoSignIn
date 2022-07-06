##加载基本库
import requests
import json

##设置HTTP请求头(使用时请自行修改UA与APIToken)
headers = {
    "Host": "gzsx.qidisoft.cn",
    "Connection": "keep-alive",
    "apitoken": "", #Token在这
    "User-Agent": "", #UA在这
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "http://gzsx.qidisoft.cn/WXPlatGZSXStu/dist/index.html?v=202205201635",
    "Accept-Encoding": "gzip, deflate",
}

##设置小程序API，json信息
url = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/ComApi/PostObject"
payload = {}    #Location在这

##将字典转换为json字符串并请求
data = json.dumps(payload)
res = requests.post(url=url,data=data,headers=headers)

##输出结果
print (res.text)
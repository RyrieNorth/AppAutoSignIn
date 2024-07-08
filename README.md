# AppAutoSignIn
实习平台自动签到小工具，可以外挂云服务器使用
可以使用Server酱等第三方工具向手机发送消息

# AppAutoSignIn v2 版本优化部分逻辑
添加外挂云服务器预设

# AppAutoSignIn v3 版本改为命令行运行逻辑
登录：python autoSignIn-v3.py login -t 2 -u admin -p admin </br>
签到：python autoSignIn-v3.py signin

# release中有已编译好的版本
使用方式如下：
</br>
Windows:
</br>
autoSignIn-v3.exe login -t 2 -u admin -p admin
</br>
autoSignIn-v3.exe signin
</br>

Linux (Linux下需要对该文件添加执行权限, chmod +x autoSignIn-v3):
</br>
autoSignIn-v3 login -t 2 -u admin -p admin
</br>
autoSignIn-v3 signin
</br>
 
# 须知
pip install request

## 使用方式(v3版本不用往下看)
Step.1 </br>
安装Fiddler，然后一直无脑Next即可

Step.2 </br>
打开Fiddler，出现AppContainer Configuration </br>
选择NO即可 </br>

Step.3 </br>
打开Tools，选择Options，选择HTTPS </br>
勾选：Capture HTTPS CONNECTs </br>
勾选：Decrypt HTTPS traffic </br>
勾选：Ignore server certificates errors </br>

Step.4 </br>
选择Connections项 </br>
勾选：Allow remote computers to connect </br>
#这一步用于抓取接入终端的HTTP流量 </br>
#请确保防火墙有放行8888/tcp端口 </br>

Step.5 </br>
在手机的WIFI设置中设置代理服务器 </br>
将代理服务器IP地址设置为部署Fiddler服务器的计算机 </br>
并将8888端口填入 </br>
打开手机浏览器，输入服务器IP+端口下载证书 </br>
下载完证书后请手动安装证书，具体你是什么手机自己查一下 </br>
IQOO手机点击设置-->安全-->更多安全设置-->从手机存储安装-->CA证书-->仍然安装-->找到你下载的证书

Step.6 </br>
打开微信小程序 </br>
通过Fiddler视图检视去往小程序的流量 </br>
特征： </br>
Host为：gzsx.qidisoft.cn </br>
URL为：http://gzsx.qidisoft.cn/WXPlatGZSXStu/ComApi/PostObject(这个是小程序的API) </br>
点开任意缓存，选择Post视图的Headers，将自己的UA，apitoken填入到小程序中 </br>

Step.7 </br>
先点一次签到，获取Post地址缓存 </br>
特征： </br>
restapi.amap.com 下面那个就是 </br>
restapi.amap.com 是腾讯开放的地理位置获取API </br>
查看缓存中的TextView，复制填入到程序中

Step.8 </br>
运行脚本，即可签到成功


## 关于UA、Token与地理位置长什么样
这里有几个例子

UA：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090b13) XWEB/9185 Flue </br>

Token：vBsCYe3xxxx/xxxxx </br>

地理位置：{"apiName":"gzsxWebApi.DoSignin","UserID":"ADMxxxxxxxxx","lat":"xx.xxxx","lng":"xxx.xxxx","distance":"xxxx","accuracy":"xx","address":"xx省xx市xx区","type":1,"locationStatus":"2","signinStatus":"1","remark":"","fileJson":"[]"}

记得Token与Jsons不要填错，Token填错别人别人是不会感谢你的，地理位置填的时候不要异想天开，因为你填南极都可以(只要腾讯有)


## 相关网站：
查询地理位置：https://lbs.qq.com/getPoint/ </br>
Python之Post请求：https://zhuanlan.zhihu.com/p/140372568 </br>
HTTP-Header简介：http://c.biancheng.net/view/3293.html </br>
程序灵感：https://blog.csdn.net/qq_44639286/article/details/105763497 </br>

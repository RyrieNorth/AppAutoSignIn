import requests
import json
import logging
import argparse
import hashlib
import time
import os
import sys

# 设置日志配置
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 解析命令行参数
parser = argparse.ArgumentParser(description="User login and signin script.")
parser.add_argument(
    "options",
    choices=["login", "signin"],
    help="Operation to perform: 'login' or 'signin'.",
)
parser.add_argument("-t", type=int, metavar="usertype", help="Account usertype")
parser.add_argument("-u", type=str, metavar="username", help="Account username")
parser.add_argument("-p", type=str, metavar="password", help="Account password")

# URL 配置
validateCode = "031Okall2oG0Ld4Ua7ol2Danyr3Okalz"
login_api = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/WXUserBind/DoBind"
signin_api = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/ComApi/PostObject"
session_url = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/WXUtil/CheckAccess"
captcha_url = "http://gzsx.qidisoft.cn/WXPlatGZSXStu/Public/GetVcImg"
validateCode_url = f"http://gzsx.qidisoft.cn/WXPlatGZSXStu/WXOauth/Index/?returl=http%253A%252F%252Fgzsx.qidisoft.cn%252FWXPlatGZSXStu%252Fdist%252Findex.html%253Fv%253D20240227a%2523%252F&code={validateCode}&state=getwxouthcode"

# 请求头
headers = {
    "Host": "gzsx.qidisoft.cn",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090b13) XWEB/9185 Flue"
    ),
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://gzsx.qidisoft.cn",
    "Referer": "http://gzsx.qidisoft.cn/WXPlatGZSXStu/dist/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7",
}

# 保存登录信息文件路径
LOGIN_INFO_FILE = "login_info.json"


# 保存 JSON 数据到文件
def save_json_to_file(data, filename="response.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    logging.info(f"JSON 数据已保存到 {filename}")


# 对密码进行 md5 加密
def md5_encrypt(pwd):
    md5_enc = hashlib.md5()
    md5_enc.update(pwd.encode("utf-8"))
    return md5_enc.hexdigest()


# 获取 ASP.Net Session_id
def get_session_id(session):
    data = {
        "rawUrl": "http://gzsx.qidisoft.cn/WXPlatGZSXStu/dist/index.html?v=20240227a#/"
    }
    response = session.post(session_url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        sessionid = response_data.get("sessionid")
        session.cookies.set("ASP.NET_SessionId", sessionid, domain="gzsx.qidisoft.cn")
        logging.info(f"Session ID 获取成功: {sessionid}")
        return session.cookies
    logging.error(f"获取 Session ID 失败, 状态码: {response.status_code}")
    return None


# 获取验证码
def get_captcha(session, cookies):
    timestamp = int(time.time() * 1000)
    new_captcha_url = captcha_url + f"?t={timestamp}"
    response = session.get(new_captcha_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        new_cookies = session.cookies
        logging.info("验证码获取成功")
        return new_cookies
    logging.error(f"获取验证码失败, 状态码: {response.status_code}")
    return None


# 获取校验码
def get_validate_code(session, cookies):
    response = session.get(validateCode_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        new_cookies = session.cookies
        logging.info("校验码获取成功")
        return new_cookies
    logging.error(f"获取校验码失败, 状态码: {response.status_code}")
    return None


# 用户登录逻辑
def user_login(usertype, username, password):
    session = requests.Session()
    cookies = get_session_id(session)
    if not cookies:
        return None

    cookies = get_captcha(session, cookies)
    if not cookies:
        return None

    cookies = get_validate_code(session, cookies)
    if not cookies:
        return None

    encrypted_password = md5_encrypt(password)
    payload = {
        "UserType": f"{usertype}",
        "userId": f"{username}",
        "pwd": encrypted_password,
    }

    try:
        response = session.post(
            login_api, headers=headers, cookies=cookies, json=payload
        )
        response.raise_for_status()
        logging.info("登录请求成功")
        return response
    except requests.RequestException as e:
        logging.error(f"登录请求失败: {e}")
        return None


# 检查登录信息文件是否存在
def check_login_info():
    return os.path.exists(LOGIN_INFO_FILE)


# 从文件读取登录信息
def read_login_info():
    with open(LOGIN_INFO_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 保存登录信息到文件
def save_login_info(data):
    with open(LOGIN_INFO_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 用户签到逻辑
def user_signin():
    # 读取登录信息
    if check_login_info():
        login_info = read_login_info()
    else:
        logging.error("未找到登录信息文件，请先登录.")
        return None

    token = login_info.get("token")
    user_id = login_info.get("memo", {}).get("uid")

    if not token or not user_id:
        logging.error("登录信息文件不完整，请重新登录.")
        return None

    headers["apitoken"] = token

    payload = {
        "apiName": "gzsxWebApi.DoSignin",
        "UserID": user_id,
        "lat": "23.145182",
        "lng": "113.273506",
        "distance": "65.75",
        "accuracy": "15.0",
        "address": "广东省广州市越秀区麓景西路越秀区广州市信息技术职业学校(下塘西校区)",
        "type": 1,
        "locationStatus": "1",
        "signinStatus": "1",
        "remark": "",
        "fileJson": "[]",
    }

    response = requests.post(url=signin_api, data=json.dumps(payload), headers=headers)
    res_json = response.json()

    if res_json.get("status") == "success":
        logging.info("今日的小程序签到已完成！！！")
        return res_json
    else:
        logging.error(f"今日的小程序签到失败，请检查是否配置正确：{res_json}")
        return None


# 显示帮助信息
def show_help():
    help_message = """
使用方法:
    登录: python autoSignIn-v3.py login -t <usertype> -u <username> -p <password>
    签到: python autoSignIn-v3.py signin

示例:
    登录: python autoSignIn-v3.py login -t 2 -u admin -p admin
    签到: python autoSignIn-v3.py signin
"""
    print(help_message)


if __name__ == "__main__":
    args = parser.parse_args()

    # 参数校验
    if not args.options:
        logging.error("缺少操作参数 'options' (login 或 signin)")
        show_help()
        sys.exit(1)

    if args.options == "login":
        if not args.t or not args.u or not args.p:
            logging.error("缺少必要的参数 '-t', '-u' 或 '-p'")
            show_help()
            sys.exit(1)

        try:
            login_response = user_login(args.t, args.u, args.p)
            if not login_response:
                logging.error("网络错误, 请检查网络或服务器状态")
            else:
                login_response_json = login_response.json()
                if login_response_json.get("error"):
                    logging.error(f"登录失败: {login_response_json.get('msg')}")
                else:
                    account_name = login_response_json.get("name")
                    logging.info(f"用户 '{account_name}' 登录成功")
                    save_login_info(login_response_json)
        except Exception as e:
            logging.error(f"登录失败, 错误信息: {e}")

    elif args.options == "signin":
        try:
            signin_response = user_signin()
            if signin_response:
                logging.info("签到完成")
            else:
                logging.error("签到失败，请检查日志信息")
        except Exception as e:
            logging.error(f"签到失败, 错误信息: {e}")

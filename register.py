import requests
import time
import random
import string

from loguru import logger

requests.packages.urllib3.disable_warnings()

yescaptcha_client_key = ''


def reCaptchaV2():
    while True:
        json_data = {
            "clientKey": yescaptcha_client_key,
            "task":
                {
                    "type": "NoCaptchaTaskProxyless",
                    "websiteURL": "https://www.google.com/recaptcha/api2/reload",
                    "websiteKey": "6LdyCj0pAAAAAFvvSTRHYOzddUPMPcH232u7a9e0",
                    "isInvisible": False,
                }
        }
        response = requests.post(url='https://api.yescaptcha.com/createTask', json=json_data).json()
        if response['errorId'] != 0:
            raise ValueError(response)
        task_id = response['taskId']
        time.sleep(5)
        for _ in range(30):
            data = {"clientKey": yescaptcha_client_key, "taskId": task_id}
            response = requests.post(url='https://api.yescaptcha.com/getTaskResult', json=data).json()
            if response['status'] == 'ready':
                return response['solution']['gRecaptchaResponse']
            else:
                time.sleep(2)

def generate_random_string(length=6):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def register(refcode,password):
    session = requests.Session()

    rand_str = generate_random_string()
    email = f"{rand_str}@grassmail.com"
    recaptcha = reCaptchaV2()
    url = 'https://api.getgrass.io/auth/reguser?app=dashboard'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://app.getgrass.io",
        "referer": "https://app.getgrass.io/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
    }
    data = {
        "email": email,
        "password": password,
        "role":"seller",
        "referral":refcode,
        "username": f"{rand_str}",
        "recaptchaToken": recaptcha
    }
    response = session.post(url, headers=headers,json=data,verify=False).json()
    if response['status'] == 'success':
        user_id = response['data']['profile']['id']
        logger.info(f"{user_id}注册成功")
        with open('account.txt', 'a') as f:
            f.write(f"{email}---{password}----{user_id}\n")
    else:
        logger.error("注册失败")

if __name__ == '__main__':
    num = 100 # 注册数量
    password = '' # 密码
    refcode = '' # 邀请码
    for i in range(num):
        register(refcode, password)
        time.sleep(2)

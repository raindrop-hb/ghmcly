import requests
import json
import re
import time

'''
可直接部署在华为云函数流
函数执行入口填：index.main_handler
触发器用cron表达式：0 30 08 * * ?
每天8:30执行
设置项
'''
token = ('wechat632647-nXRFrCb98Eptg697iml3Z', 'wechat1307414-jtli0VTqt9ruZRBLy8XS')
# token,抓包，先喂养，参数里access-token就是token
push = '0' # 是否微信机器人推送，1为是，0为否，选择0则后面三项失效
corpid = 'ww0fc7f0b7cc'  # 企业ID
secret = 'j-F4DeIhMtbbB321PWHBp8tl_ii7zTga'  # 应用的凭证密钥
agentid = 1000 #应用id



def run_1(token):
    url = 'https://fw.qyfw168.cn/api/soft/anhui_mengchong/v1/user-goods/create'
    print(url)
    data = {"access-token": token, "pid": "tujS423"}
    print(data, type(data))
    url = "https://fw.qyfw168.cn/api/soft/anhui_mengchong/v1/user-goods/create"
    response = requests.post(url, data=data,
                             headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    res = json.loads(response.text)
    print(res)
    if res['status'] == 400:
        print("run_1,400")
        log = res['message']
        run_2(token, log)
    elif 'goods' in res:
        log = res['name']
        log = "领取" + log + "成功"
        run_2(token, log)
    elif res['status'] == 401:
        log = token+'token失效'
        print(push_a(log))


def run_2(token, log):
    time_1 = int(time.time())
    time_2 = time.localtime(time_1)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time_2)
    url = 'https://fw.qyfw168.cn/api/soft/anhui_mengchong/v1/user/view'
    data = {'access-token': token, 'pid': 'tujS423'}
    resp = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    id = json.loads(resp.text).get('id')
    nickname = json.loads(resp.text).get('nickname')
    mobile = json.loads(resp.text).get('mobile')
    mobile = str(mobile[0:3]) + '****' + str(mobile[7:])
    score = json.loads(resp.text).get('score')
    mengchong = json.loads(resp.text).get('mengchong')
    print(mengchong)
    mengchong['鸡蛋'] = mengchong.pop('1')
    mengchong['羊毛'] = mengchong.pop('2')
    mengchong['牛奶'] = mengchong.pop('3')
    mengchong['羽毛'] = mengchong.pop('4')
    mengchong['蝴蝶'] = mengchong.pop('5')
    s = '喂养信息:'
    for i in mengchong:
        s = s + '\n' + i + ':' + str(mengchong[i])
    log = "工商银行萌宠乐园执行任务\n----------raindrop----------\n" + now + "\n状态:" + log + "\nid=" + str(
        id) + "\n昵称:" + nickname + "\n手机号:" + mobile + "\n剩余能量" + str(score) + "\n" + s
    print(push_a(log))


def push_a(content):
    print(push)
    if push == '0':
        print('不推送')
    else:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + secret
        access_token = requests.get(url)
        access_token = json.loads(access_token.text)
        print(access_token, type(access_token))
        access_token = access_token.get("access_token")
        token = 'c8avSOlP-d5wLBuws4LmmsIjgmnCrUfPA16ftSCAJM4'
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        data = json.dumps({
            "touser": "@all",
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": content
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        })
        resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        return (json.loads(resp.text).get('errmsg'))


def main():
    for i in token:
        run_1(i)
        time.sleep(10)


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()

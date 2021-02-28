# -*- coding: utf-8 -*-
import time
import requests
import json
import os

apiID = os.environ['apiID']
class WeChat:
    def __init__(self):
        self.CORPID = os.environ["CORPID"]  # 企业ID，在管理后台获取
        # 自建应用的Secret，每个自建应用里都有单独的secret
        self.CORPSECRET = os.environ["CORPSECRET"]
        self.AGENTID = '1000005'  # 应用ID，在后台应用中获取
        self.TOUSER = '@all'  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        """
        调用接口返回登录信息access_token
        """
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        """
        将获取到的access_token保存到本地
        """
        try:
            with open('./tmp/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./tmp/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./tmp/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, title, Today, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
            self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "textcard",
            "agentid": self.AGENTID,
            "textcard": {
                "title": title,
                "description": '<div class=\"gray\">'+ Today + '</div> <div class=\"normal\">' + message+ '</div><div class=\"highlight\">请注意天气变化哦</div>',
                "url": "https://ivitan.com",
                "btntxt": "更多"
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]

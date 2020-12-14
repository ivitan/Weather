# -*- coding: UTF-8 -*-
from urllib.parse import urlencode
import requests
import os
 
def GetWeather(ct):
    # 天气接口
    url="https://tianqiapi.com/api"
    # 参数
    apiID = os.environ['apiID']
    appSecret = os.environ['appSecret']
    data={}
    data['version']='v6'
    data['appid']= apiID
    data['appsecret']= appSecret
    data['city']=ct
 
    # 将参数转换成url可用格式
    data=urlencode(data)
 
    # 最终的url请求
    request=url+'?'+data
 
    # 读取请求结果
    rep=requests.get(request)
 
    # 请求结果转换成json格式
    repJson = rep.json()
 
    tdate = repJson.get('date')
    week = repJson.get('week')
    city = repJson.get('city')
    wea = repJson.get('wea')
    tem1=repJson.get('tem1')
    tem2 =repJson.get('tem2')
    air=repJson.get('air_level')
    pm=repJson.get('air_pm25')



    text = week+','+wea
    weather = '- '+city+','+wea+'\n'+'- '+tem2+'℃ ~'+tem1+'℃'+'\n'+'- '+'空气质量：'+air+'\n'+'- '+'PM2.5：'+pm

    return(text,weather)
GetWeather('广州')
# Server 酱    

def SendWechat(title,message):
    # text 为推送 title,desp 为推送描述
    sckey = os.environ['SCKEY']
    url = 'https://sc.ftqq.com/'+sckey+'.send?text='+title+'&desp='+message
    requests.get(url)

def main():
    Weathers = GetWeather('广州')
    title = Weathers[0]
    message = Weathers[1]
    print(title,message)
    SendWechat(title,message)

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 10:00:56 2021

@author: 13567

File content: user logs in
"""

import requests
import json
from Model.models import UserInfo, AppInfo
from .constants import const
from .utils import response
from django.views.decorators.csrf import csrf_exempt

# md5 encryption
# @param:
#   v: string
def get_md5(v):
    import hashlib
    md5 = hashlib.md5()
    md5.update(v.encode('utf-8'))
    value = md5.hexdigest()
    return value

# save user's information in the database 
def saveUserInfo(req, res, userId):
    if UserInfo.objects.filter(openid=res['openid']):
        oldUserInfo = UserInfo.objects.get(openid=res['openid'])
        oldUserInfo.delete()
    userInfo = UserInfo(
        openid=res['openid'], 
        session_key=res['session_key'], 
        user_id=userId,
        nick_name=req['userinfo']['nick_name'],
        avatar_url=req['userinfo']['avatar_url'],
        city=req['userinfo']['city'],
        country=req['userinfo']['country'],
        gender=req['userinfo']['gender'],
        language=req['userinfo']['language'],
        province=req['userinfo']['province']
        )
    userInfo.save()
    return

# login main function
# req:
#   method: POST
#   params: code
#           userinfo
@csrf_exempt
def login(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     user_id: customized login status
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        code = req['code']
        appInfo = AppInfo.objects.get(id=1)
        # wechat request parameters
        qs = {
            'grant_type': 'authorization_code',
            'appid': appInfo.appid,
            'secret': appInfo.secret,
         	'js_code': code
        }
        res = requests.get(appInfo.wechat_url, params=qs).json()
        if 'session_key' in res.keys():
            userId = get_md5(res['session_key'])
            saveUserInfo(req, res, userId)
            meta['msg'] = "success"
            data['user_id'] = userId
            return response(meta, data, 200)
        else:
            meta['msg'] = "code is invalid"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
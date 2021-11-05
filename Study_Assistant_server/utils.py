# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 20:50:56 2021

@author: 13567

File content: utilities
"""
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from Model.models import UserInfo
import time
import json

# change the datetime form string to time stamp
# @params:
# dateTime: datetime form string
def dateTimeToTimeStamp(dateTime):
    timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = time.mktime(timeArray)
    return timeStamp

# # check login status 
# # last login time mast be within one day, or it needs logging in again
# # @params:
# # userId: customized login status
# def checkLoginStatus(userId):
#     if UserInfo.objects.filter(user_id=userId):
#         userInfo = UserInfo.objects.get(user_id=userId)
#         loginTimeStamp = dateTimeToTimeStamp(str(userInfo.login_time)[:-13])
#         nowTime = time.time()
#         # convert to day as unit
#         duration = (nowTime - loginTimeStamp - 8 * 3600) / (3600 * 24) 
#         if duration < 1:
#             return True
#     return False

# check login status (whether the user exists)
# @params:
# userId: customized login status
def checkLoginStatus(userId):
    if UserInfo.objects.filter(user_id=userId):
        return True
    return False

# response to the client
# @params:
# meta: response infomation
# data: response content
# status_code: status code
def response(meta, data, status_code):
    httpRes = {}
    httpRes['meta'] = meta
    httpRes['data'] = data
    if status_code == 200:
        return HttpResponse(json.dumps(httpRes), status=status_code)
    elif status_code == 400:
        return HttpResponseBadRequest(meta['msg'])
    else:
        return HttpResponseServerError(meta['msg'])
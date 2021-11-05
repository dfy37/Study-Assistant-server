# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 22:25:33 2021

@author: 13567

File content: collections of user
"""

import datetime, time, json
from Model.models import UserInfo, UserFavori, UserFavoriToken, Entry
from .utils import checkLoginStatus, response, dateTimeToTimeStamp
from django.views.decorators.csrf import csrf_exempt

# return collection list of the server to the client
# req:
#   method: POST
#   params: user_id
@csrf_exempt
def sync(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     collection_list:
    #         entry_id: entry id
    #         entry_title: entry title
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            userCollections = UserFavori.objects.filter(openid=userInfo.openid)
            collectionList = []
            for userCollection in userCollections:
                collection = {}
                collection['entry_id'] = userCollection.entry_id
                collection['entry_title'] = userCollection.entry_title
                collectionList.append(collection)
            collectionList.reverse()
            meta['msg'] = "success"
            data['collection_list'] = collectionList
            return response(meta, data, 200)
        else:
            meta['msg'] = "login timeout"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
    
# add user collection
# req:
#   method: PUT
#   params: user_id
#           entry_id
@csrf_exempt
def addEntry(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     status:
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        entryId = req['entry_id']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            if not UserFavori.objects.filter(openid=userInfo.openid, entry_id=entryId):
                entry = Entry.objects.get(id=entryId)
                userFavori = UserFavori(openid=userInfo.openid, entry_id=entryId, entry_title=entry.title)
                userFavori.save()
            meta['msg'] = "success"
            data['status'] = "collection_ok"
            return response(meta, data, 200)
        else:
            meta['msg'] = "login timeout"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
    
# delete user collection
# req:
#   method: DELETE
#   params: user_id
#           entry_id
@csrf_exempt
def delEntry(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     status:
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        entryId = req['entry_id']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            userFavori = UserFavori.objects.get(openid=userInfo.openid, entry_id=entryId)
            userFavori.delete()
            meta['msg'] = "success"
            data['status'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "login timeout"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
    
# justify whether the collection list of the server is the latest 
# req:
#   method: POST
#   params: user_id
#           token
@csrf_exempt
def islatest(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     need_update: whether need to update
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        clientToken = req['token']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            serverToken = UserFavoriToken.objects.get(openid=userInfo.openid)
            clientStamp = dateTimeToTimeStamp(clientToken)
            serverStamp = dateTimeToTimeStamp(serverToken.token)
            if clientStamp >= serverStamp:
                data['need_update']=False
            else:
                data['need_update']=True
            meta['msg'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "login timeout"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
    
# submit collection list of the client to the server
# req:
#   method: POST
#   params: user_id
#           user_collection
@csrf_exempt
def submit(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     updated: whether updating succeeds
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        collections = req['user_collection']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            
            # if UserFavoriToken.objects.filter(openid=userInfo.openid):
            #     userFavoriToken = UserFavoriToken.objects.get(openid=userInfo.openid)
            # else:
            #     userFavoriToken = UserFavoriToken(openid=userInfo.openid)
            # userFavoriToken.token = str(datetime.datetime.now())[:-7]
            # userFavoriToken.save()
            # data['token'] = userFavoriToken.token
            
            UserFavori.objects.filter(openid=userInfo.openid).delete()
            for collection in collections:
                userCollection = UserFavori(
                    openid=userInfo.openid, 
                    entry_id=collection['entry_id'], 
                    entry_title=collection['entry_title']
                    )
                userCollection.save()
            data['updated'] = True
            
            meta['msg'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "login timeout"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400) 
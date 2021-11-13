# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 22:52:44 2021

@author: 13567

File content: entry operations
"""

import json
from Model.models import Entry, UserInfo, UserFavori
from .utils import response, checkLoginStatus
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# add an entry
# req:
#   method: GET
#   params: keywords
@csrf_exempt
def entrySearch(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     result_list:
    #         entry_id:
    #         entry_title:
    meta={}
    data={}
    try:
        keyWords = request.GET['keywords']
        entries = Entry.objects.filter(Q(title__icontains=keyWords) | Q(content__icontains=keyWords) | \
                                       Q(proof__icontains=keyWords) | Q(remark__icontains=keyWords) | \
                                           Q(example__icontains=keyWords))
        resultList = []
        for entry in entries:
            result = {}
            result['entry_id'] = entry.id
            result['entry_title'] = entry.title
            resultList.append(result)
        data['result_list'] = resultList
        
        meta['msg'] = "success"
        return response(meta, data, 200)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)
    
# return the detail of an entry
# req:
#   method: GET
#   params: entry_id
#           user_id
@csrf_exempt
def entryDetail(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     entry_detail:
    #         id:
    #         title:
    #         content:
    #         proof:
    #         remark:
    #         example:
    #         source:
    #         chinese:
    #         author:
    #     is_collected: 
    meta={}
    data={}
    try:
        entryId = request.GET['entry_id']
        entry = Entry.objects.get(id=entryId)
        entryDetail = {}
        entryDetail['id'] = entry.id
        entryDetail['title'] = entry.title
        entryDetail['content'] = entry.content
        entryDetail['proof'] = entry.proof
        entryDetail['remark'] = entry.remark
        entryDetail['example'] = entry.example
        entryDetail['source'] = entry.source
        entryDetail['chinese'] = entry.chinese
        entryDetail['author'] = entry.author
        data['entry_detail'] = entryDetail
        data['is_collected'] = False
        
        if 'user_id' in request.GET:
            userId = request.GET['user_id']
            userInfo = UserInfo.objects.get(user_id=userId)
            if UserFavori.objects.filter(openid=userInfo.openid, entry_id=entryId):
                data['is_collected'] = True
        
        meta['msg'] = "success"
        return response(meta, data, 200)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)
    
# make a new entry
# req:
#   method: PUT
#   params: user_id
#           new_entry:
#               title
#               content
#               proof
#               remark
#               example
#               source
#               chinese
@csrf_exempt
def addEntry(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     status: success or fail
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        newEntry = req['new_entry']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            authorName = userInfo.nick_name
            entry = Entry(
                title=newEntry['title'], 
                content=newEntry['content'],
                proof=newEntry['proof'],
                remark=newEntry['remark'],
                example=newEntry['example'],
                source=newEntry['source'],
                chinese=newEntry['chinese'],
                author=authorName,
                )
            entry.save()
            
            meta['msg'] = "success"
            data['status'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "user doesn't exist"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)

# edit an entry
# req:
#   method: POST
#   params: user_id
#           entry_id
#           type
#           rawMD
@csrf_exempt
def editEntry(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     status: success or fail
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        entryId = req['entry_id']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            item = { req['type']:req['rawMD'] }
            Entry.objects.filter(id=entryId).update(**item)
                
            meta['msg'] = "success"
            data['status'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "user doesn't exist"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)
    
# get the id of the entry by the title
# req:
#   method: GET
#   params: title
@csrf_exempt
def getEntryId(request):
    # response to the wechat program
    # meta: 
    #     msg: message of response
    # data: 
    #     entry_id: 
    meta = {}
    data = {}
    try:
        entryTitle = request.GET['title']
        entry = Entry.objects.get(title=entryTitle)
        data['entry_id'] = entry.id        
        
        meta['msg'] = "success"
        return response(meta, data, 200)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)


# update an entry
# req:
#   method: POST
#   params: user_id
#           entry_id
#           entry
@csrf_exempt
def updateEntry(request):
    # response to the wechat program
    # meta:
    #     msg: message of response
    # data:
    #     status: success or fail
    meta = {}
    data = {}
    try:
        req = json.loads(request.body.decode())
        userId = req['user_id']
        entryId = req['entry_id']
        if checkLoginStatus(userId):
            userInfo = UserInfo.objects.get(user_id=userId)
            item = req['entry']
            Entry.objects.filter(id=entryId).update(**item)

            meta['msg'] = "success"
            data['status'] = "success"
            return response(meta, data, 200)
        else:
            meta['msg'] = "user doesn't exist"
            return response(meta, data, 500)
    except Exception as e:
        meta['msg'] = e
        return response(meta, data, 400)
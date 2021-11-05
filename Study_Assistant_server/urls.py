"""Study_Assistant_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import login, collection, entry

urlpatterns = [
    path('admin', admin.site.urls),
    
    path('login', login.login),
    
    # path('collection/islatest', collection.islatest),
    path('collection/submit', collection.submit),
    path('collection/sync', collection.sync),
    path('collection/addentry', collection.addEntry),
    path('collection/delentry', collection.delEntry),
    
    path('entry/entrysearch', entry.entrySearch),
    path('entry/entrydetail', entry.entryDetail),
    path('entry/addentry', entry.addEntry),
    path('entry/editentry', entry.editEntry),
    path('entry/getentryid', entry.getEntryId),
]



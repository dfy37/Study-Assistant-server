# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:17:46 2021

@author: 13567

File content: contants of the program
"""

class Const(object):
    class ConstError(TypeError):
        pass
    
    class ConstCaseError(ConstError):
        pass
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all supercase' % name)
            
        self.__dict__[name] = value
        
const = Const()

# code
const.CODE_SUCCESS = 200
const.CODE_SERVER_ERROR = 500
const.CODE_CLIENT_ERROR = 400

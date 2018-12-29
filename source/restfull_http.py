# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:29:16 2018

@author: EMV_AF
"""

import sys
import uuid
import time 
import requests 
import json
import numpy as np
import requests
import pandas as pd
from os import path
    

class restfull_http:
    def __init__(self, Authorization = "", staticPoint=""):
        self.Authorization = Authorization
        self.staticPoint = staticPoint

    def gett(self, DynamPoint):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        print(endPoint)
        r = requests.get(endPoint,headers = headers)
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)#(json_input)
        else:
            json_input = r.json()
            print("Error status", r.status_code)
            return(json_input)

    def postt(self, DynamPoint, dumps={}, params = {}):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        r = requests.post(endPoint, data = dumps, headers = headers, params=params )
        print("\nServer Responce:", r.text) 
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)#(json_input)
        else:
            json_input = r.json()
            print("Status Code: ", r.status_code)
            return(json_input)
          

    def putt(self, DynamPoint, dumps):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        response = requests.put(endPoint, data = dumps, headers = headers) 
        print("\nPut status:", response.status_code, response.text) 
        return(response.status_code)

    def patch(self, DynamPoint, dumps):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        response = requests.put(endPoint, data = dumps, headers = headers) 
        print("\nPut status:", response.status_code, response.text) 
        return(response.status_code)

    def deletee(self, DynamPoint, dumps = {}):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        r = requests.delete(endPoint, data=dumps, headers = headers)
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)
        else:
            json_input = r.json()
            print("Status Code: ", r.status_code)
            return(json_input)



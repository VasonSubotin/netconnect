# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 10:33:43 2018

@author: amank
CPLEX version of smart charging problem - focused on cap charging problem using python wrapper
"""

import cvxpy as cvx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import timeit
from datetime import datetime

from source.restfull_http import restfull_http
# this code is exact python replica of the OPL problem we defined for Cap charging in CPLEX

# constants:
#static_point = 'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Pro'




class get_data:
    
        
    def get_nodes_from_resource(self, static_point, resource_id):
        core_calls = restfull_http('', static_point)
        json = core_calls.gett('/resources/' + str(resource_id) + '/locations/')
        df = pd.DataFrame(json["nodes"])
        df["resource"] = json["resource_id"]
        df = df.pivot(index='resource', columns='node_id', values=['edge'])
        return(df)
    
    def get_nodes_from_resources(self, static_point, resource_id_list):
        df  = pd.DataFrame()
        for i in  resource_id_list:
            temp = self.get_nodes_from_resource(self, static_point, i)
            df  = df.append(temp)
        return(df)    

    def get_maxsoc_from_resource(self, static_point, resource_id):
        core_calls = restfull_http('', static_point)
        json = core_calls.gett('/resources/' + str(resource_id))
        df = {'soc_max':json["soc_max"]}
        df =pd.DataFrame(df, columns = ['soc_max'], index = ["soc_max"])
        df["resource_id"] = json["resource_id"]
        return(df) 
    
    def get_maxsoc_from_resources(self, static_point, resource_id_list):
        df  = pd.DataFrame()
        for i in  resource_id_list:
            temp = self.get_maxsoc_from_resource(self, static_point, i)
            df  = df.append(temp)
        df = df.set_index('resource_id')
        return(df)
        
    def get_currentsoc_from_resource(self, static_point, resource_id):
        core_calls = restfull_http('', static_point)
        json = core_calls.gett('/resources/' + str(resource_id)+'/state')
        df = {'soc':json["soc"]}
        df = pd.DataFrame(df, columns = ['soc'], index = ['soc'])
        df["resource_id"] = json["resource_id"]
        return(df) 
    
    def get_currentsoc_from_resources(self, static_point, resource_id_list):
        df  = pd.DataFrame()
        for i in  resource_id_list:
            temp = self.get_currentsoc_from_resource(self, static_point, i)
            df  = df.append(temp)
        df = df.set_index('resource_id')
        print(df)
        return(df)
        
    def get_data_from_file(self, filename = 'data/DataFile.xlsx'):
        data_file = filename
        
        #create xls object
        xls = pd.ExcelFile(data_file)
        
        #read prices
        df_prices= pd.read_excel(xls, 'Prices')
        prices = np.array(df_prices.iloc[1:6,0:4])
    
        df_current_soc= pd.read_excel(xls, 'CurrentSOC')
        current_soc = np.array(df_current_soc.iloc[1:6,0:4])
    
        #read nodes
        df_nodes= pd.read_excel(xls, 'Nodes')
        nodes = np.array(df_nodes.iloc[1:6,0:4])
    
        # read MSocs
        df_msoc= pd.read_excel(xls, 'MSoc')
        msoc = np.array(df_msoc["SOCmax"][1:6])
        return(prices,current_soc, nodes, msoc)

        






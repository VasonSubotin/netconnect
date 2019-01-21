# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:59:17 2019

@author: EMV_AF
"""

from datetime import datetime
import pandas as pd
import numpy as np
import random

class interval:
    def __init__(self):
        
        self.time_start = time_start
        self.location = location
        self.cost_of_charging = cost_of_charging
        self.price = price
        self.duration = duration
        self.energy = energy
        self.charge_rate = charge_rate
        self.interval_type = interval_type
        self.economic_savings = economic_savings
        self.co2_impact = co2_impact
        self.soc_achieved = soc_achieved      
        
        
    def dataframe_to_json(self):
        
        df = pd.DataFrame({'time_start': self.time_start,
                           'location': self.location,
                           'cost_of_charging': self.cost_of_charging,
                           "price": self.price,
                           "duration":self.duration, 
                           "energy": self.energy, 
                           "charge_rate":self.charge_rate, 
                           "interval_type" : self.interval_type, 
                           "economic_savings":self.economic_savings, 
                           "co2_impact":self.co2_impact, 
                           "soc_achieved":self.soc_achieved }, index=[1,2,3,4,5,6,7])
    
        return(df.to_json(orient='records'))
    



class schedule:
    #def __init__(self):
     #   pass
        #self.row_node = row_node
        #self.resource_id = resource_id
        #self.schedule_id = "aaa"
        #self.time_start = datetime.now()
        #self.savings = 22
        #self.intervals = self.make_intervals(self.row_node)
           

    def __list_random(ran):
        return(random.shuffle(ran))
    
    def make_intevals(self, energytoresource,  prices, locations, current_soc):
        #df = pd.DataFrame()
        schlist = []
        duration = list(np.random.randint(2000,14500,size=(4)))
        cost_of_charging = list(np.random.randint(10,2000,size=(4)))
        charge_rate = list(np.random.randint(10,450,size=(4)))
        #interval_type = self.__list_random(["CHR", "TOU", "DRV","WRK" ])
        interval_type = 'CHR'
        economic_savings = list(np.random.randint(1,10,size=(4)))
        co2_impact = list(np.random.randint(1,10,size=(4))) 
        soc_achieved = energytoresource.value + current_soc

        for index, resoure in enumerate(energytoresource.value.tolist()):
            df = pd.DataFrame()
            df["time_start"] = datetime.now()
            df["energy"] = resoure
            df["price"] = prices.tolist()[index]
            df["location"] = locations.values.tolist()[0]
            df["duration"] = duration
            df["cost_of_charging"] = cost_of_charging
            df["charge_rate"] = charge_rate
            df["interval_type"] = interval_type
            df["economic_savings"] = economic_savings
            df["co2_impact"] = co2_impact
            df["soc_achieved"] = soc_achieved.tolist()[index]
            df = df.to_json(orient='records')
            temp_dic = {"schedule_id": "guid","time_start" : "time_start", "savings":3.5, "intervals":df }

            
            schlist.append(temp_dic)
        print(schlist) 
        return(schlist)
        
    def make_schedule(self, intervals):
        intervals = intervals.to_json(orient='records')
       
        temp_dic = {"schedule_id": "guid","time_start" : "time_start", "savings":3.5, "intervals":intervals }
        print("scheduale", temp_dic)

    
        return(temp_dic)
    
    def make_intervals(self, row_node):
        for node in row_node:
            tempobj = interval
            tempobj.time_start = datetime.now()
            tempobj.location = "mocklocation"
            tempobj.cost_of_charging = 334
            tempobj.price = 3.4
            tempobj.duration = 45
            tempobj.energy = node
            tempobj.charge_rate = 433
            tempobj.interval_type = "DAM"
            tempobj.economic_savings = 22
            tempobj.co2_impact = 11
            tempobj.soc_achieved = 34
            interval_json = tempobj.dataframe_to_json(self)
            print(interval_json)
        return(interval_json)
        

    

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:59:17 2019

@author: EMV_AF
"""

from datetime import datetime
import pandas as pd
import numpy as np
import random
import json

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
          

    def __list_random(ran):
        return(random.shuffle(ran))
    
    def make_schedules(self, energytoresource,  prices, locations, current_soc):
        node__num = locations.shape[1]
        schlist = []
        duration = list(np.random.randint(2000,14500,size=(node__num)))
        cost_of_charging = list(np.random.randint(10,2000,size=(node__num)))
        charge_rate = list(np.random.randint(10,450,size=(node__num)))
        #interval_type = self.__list_random(["CHR", "TOU", "DRV","WRK" ])
        interval_type = 'CHR'
        economic_savings = list(np.random.randint(1, 10, size=(node__num)))
        co2_impact = list(np.random.randint(1, 10, size=(node__num))) 
        soc_achieved = energytoresource.value + current_soc

        for index, resoure in enumerate(energytoresource.value.tolist()):
            df = pd.DataFrame()
            df["energy"] = resoure
            df["time_start"] = str(datetime.now())
            df["price"] = prices.tolist()[index]
            df["location"] = locations.values.tolist()[0]
            df["duration"] = duration
            df["cost_of_charging"] = cost_of_charging
            df["charge_rate"] = charge_rate
            df["interval_type"] = interval_type
            df["economic_savings"] = economic_savings
            df["co2_impact"] = co2_impact
            df["soc_achieved"] = soc_achieved.tolist()[index]
            df = df.to_dict(orient = 'records')
            #df = df.to_json(orient='records')
            temp_dic = {"schedule_id": "guid","time_start" : str(datetime.now()), "savings":3.5, "intervals":df }
            temp_dic = json.dumps(temp_dic)
            schlist.append(temp_dic)
            
        print(schlist) 
        return(schlist)
        

    

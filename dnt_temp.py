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
from datetime import datetime
import random
from source.restfull_http import restfull_http
from data.get_data import get_data
from data.core import schedule
#from data.core import make_output
# this code is exact python replica of the OPL problem we defined for Cap charging in CPLEX

# constants:
#static_point = 'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Pro'



class cplex_model:
    
    def __init__(self, NumberOfResources = 5, NumberOfNodes = 4):
        self.NumberOfResources = NumberOfResources
        self.NumberOfNodes = NumberOfNodes

        
    def get_lp_solution(self, resources, locations, prices,current_soc, nodes, msoc):
        constraints = []

        NumberOfResources, NumberOfNodes = [nodes.shape[0], nodes.shape[1]]
        
              
        energytoresource = cvx.Variable((NumberOfResources, NumberOfNodes), nonneg=True)
    
        obj = cvx.Minimize(cvx.sum(cvx.multiply(energytoresource, prices)))
        
        # the resource must be charged with more or equal kWh to drive to the next location
        for r in range(0, NumberOfResources):
            for n in range(0, NumberOfNodes):
                        constraints += [(energytoresource[r, n] + current_soc[r,n] )  >= nodes[r,n]]
        
         
       # the total amount of energy charged acrossed all location shold be less than SOC max
        for r in range(0, NumberOfResources):
            constraints += [cvx.sum(energytoresource[r,:] ) == msoc[r]]
  
        
        #the total amount of energy charged at location shold be less than SOC max for the resources
        for r in range(0, NumberOfResources):
            for n in range(0, NumberOfNodes):
                constraints += [(energytoresource[r, n] + current_soc[r, n] )  <= msoc[r]]


 
        #form and solve the prblem 
        prob = cvx.Problem(obj, constraints)
        #exexuting the solver
        start1=datetime.now()
        #prob.solve(solver = cvx.EPSON, verbose=True)
        prob.solve(solver = cvx.CPLEX, verbose=True)
        stop1 = datetime.now()
        print('Time taken[seconds]  - datetime: ', (stop1 - start1).total_seconds())
        
        sch  = schedule
        intervals = sch.make_schedules(schedule, energytoresource,  prices, locations, current_soc)
        #result = sch.make_schedule(schedule, intervals)
        print("Hello")
        #json(df.to_json(orient='records'))
        return(intervals)
        #return(intervals, resources,locations,  energytoresource.value)
        
        
def main():
    
        
    #nodes = obj.get_nodes_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5]  )
    #msoc = obj.get_maxsoc_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5]  )
    #currentsoc = obj.get_currentsoc_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5])
    #print("\nNodes:\n", nodes)
    #print('\nMsoc\n', msoc)
    #print("\nCurrentsoc: \n", currentsoc)
    
    obj = cplex_model
    getdata = get_data
        
    #read data from the file
    #resources, locations, prices,current_soc, nodes, msoc = getdata.get_data_from_file(4, 'data/DataFile.xlsx')
    resources, locations, prices,current_soc, nodes, msoc = getdata.get_data_from_file(get_data, 4, 4, 'data/DataFile.xlsx')
        
    schedule = obj.get_lp_solution(cplex_model, resources, locations, prices,current_soc, nodes, msoc)
    #sch  = schedule
    #sch.row_node = [45,67,8]
    #sch.make_intervals(schedule, [45,67,8])
    
    #print("\nintervals:\n", intervals)

    #output = make_output
    #dat = output.dataframe_to_json(make_output, energytoresource)
    #print(dat)
    

if __name__=="__main__":
    main()






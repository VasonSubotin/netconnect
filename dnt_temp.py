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

from source.restfull_http import restfull_http
from data.get_data import get_data
# this code is exact python replica of the OPL problem we defined for Cap charging in CPLEX

# constants:
#static_point = 'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Pro'




class cplex_model:
    
    def __init__(self, NumberOfResources = 5, NumberOfNodes = 4):
        self.NumberOfResources = NumberOfResources
        self.NumberOfNodes = NumberOfNodes
        

        
    def get_lp_solution(self, NumberOfResources, NumberOfNodes):
        constraints = []
        getdata = get_data
        
        #read data from the file 
        prices,current_soc, nodes, msoc = getdata.get_data_from_file(getdata.get_data_from_file('data/DataFile.xlsx'))
    
        energytoresource = cvx.Variable((NumberOfResources,NumberOfNodes), nonneg=True)
    
        obj = cvx.Minimize(cvx.sum(cvx.multiply(energytoresource, prices)))
        
        # the resource must be charged with more or equal kWh to drive to the next location
        for r in range(0,NumberOfResources):
            for n in range(0, NumberOfNodes):
                        constraints += [(energytoresource[r, n] + current_soc[r,n] )  >= nodes[r,n]]
        
         
        # units can not be charged with less than max allowed SOC
        for r in range(0,NumberOfResources):
            for n in range(0, NumberOfNodes):
                        constraints += [(energytoresource[r, n] + current_soc[r,n] )  <= msoc[r]]
            
        
        # units must charge fully at last node
        for r in range(0, NumberOfResources):
            constraints += [(energytoresource[r, NumberOfNodes-1] + current_soc[r, NumberOfNodes-1] )  == msoc[r]]
        
        #form and solve the prblem 
        prob = cvx.Problem(obj, constraints)
        
        #exexuting the solver
        start1=datetime.now()
        prob.solve(solver = cvx.CPLEX, verbose=True)
        stop1=datetime.now()
        
        print('Time taken[seconds]  - datetime: ', (stop1 - start1).total_seconds())
        print(energytoresource.value)
        return(energytoresource.value)
        
        
def main():
    
    obj = get_data
    
    nodes = obj.get_nodes_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5]  )
    msoc = obj.get_maxsoc_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5]  )
    currentsoc = obj.get_currentsoc_from_resources(get_data,'https://ulefqvgdah.execute-api.us-west-1.amazonaws.com/Prod', [1,2,3,4,5])
    print("\nNodes:\n", nodes)
    print('\nMsoc\n', msoc)
    print("\nCurrentsoc: \n", currentsoc)
    
    obj = cplex_model
    energytoresource = obj.get_lp_solution(cplex_model,5,4)
    #print("\nSolution:\n",energytoresource)

if __name__=="__main__":
    main()






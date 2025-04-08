# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 06:37:20 2023

@author: cmpet
"""

import pandas as pd
import helper_functions as hf
import matplotlib.pyplot as plt
import numpy as np

##bring in data
demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
demands = demands.T
demands = demands.reset_index(drop=True)
demands = demands.drop(columns=2041)
failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)

##Create supply boolean table
supply_condition = (failure_durations == 0)

scenarios = [1, 2, 3, 4]

LD_UR_chng={}
MD_UR_chng={}
HD_UR_chng={}


for s in scenarios:
    UR = pd.read_csv('D:/Modeloutput/UR_f162_s' + str(s) + '.csv', index_col=0)
    columns2exclude = ['2019', '2020']
    UR = UR.drop(columns=columns2exclude)
    DC = pd.read_csv('D:/Modeloutput/DC_f162_s' + str(s) + '.csv', index_col=0)
    RC = pd.read_csv('D:/Modeloutput/RC_f162_s' + str(s) + '.csv', index_col=0)
    
    DC_condition = (DC >= 1)
    RC_condition = (RC >= 1.25)
    
    supply_condition.columns = DC_condition.columns
    combined_conditions = supply_condition & DC_condition & RC_condition
    
    UR_changes = UR.pct_change(axis=1)
    UR_filter = UR_changes[combined_conditions]
    
    LD_UR_chng[s], MD_UR_chng[s], HD_UR_chng[s] = hf.realization_3groups(UR_filter, realization_groupings)
    
def avg_pctchg(dictionary):
    avg={}
    for key, df in dictionary.items():
        avg[key] = df.mean(axis=1)
    return avg

LD_avgs = avg_pctchg(LD_UR_chng)
MD_avgs = avg_pctchg(MD_UR_chng)
HD_avgs = avg_pctchg(HD_UR_chng)

def final_avg(dictionary):
    avg_value={}
    for key, df, in dictionary.items():
        avg_value[key] = df.mean()
    return avg_value

LDavg = final_avg(LD_avgs)
MDavg = final_avg(MD_avgs)
HDavg = final_avg(HD_avgs)
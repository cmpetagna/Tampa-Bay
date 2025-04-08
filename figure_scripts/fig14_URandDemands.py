# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:46:11 2023

@author: cmpet
"""

import pandas as pd
import helper_functions as hf
import matplotlib.pyplot as plt

##bring in data
demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
demands = demands.T
demands = demands.reset_index(drop=True)
demands = demands.drop(columns=2041)
failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)

##Create supply boolean table
supply_condition = (failure_durations == 0)


scenarios = [4, 18, 19, 20]
LD_demands = {}
MD_demands = {}
HD_demands = {}
LD_URs = {}
MD_URs = {}
HD_URs = {}

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
    
    UR_filter = UR[combined_conditions]
    demands.columns = combined_conditions.columns
    demand_filter = demands[combined_conditions]
    
    LD_demands[s], MD_demands[s], HD_demands[s] = hf.realization_3groups(demand_filter, realization_groupings)
    LD_URs[s], MD_URs[s], HD_URs[s] = hf.realization_3groups(UR_filter, realization_groupings)
    
fig, axes = plt.subplots(3, 1, figsize=(12,8), sharex=True)
axes[0].scatter(HD_URs[4], HD_demands[4], color='darkorange', label='SOW Group 1')
axes[1].scatter(MD_URs[4], MD_demands[4], color='darkorange')
axes[2].scatter(LD_URs[4], LD_demands[4], color='darkorange')
axes[0].scatter(HD_URs[18], HD_demands[18], color='aqua', label='SOW Group 2')
axes[1].scatter(MD_URs[18], MD_demands[18], color='aqua')
axes[2].scatter(LD_URs[18], LD_demands[18], color='aqua')
axes[0].scatter(HD_URs[20], HD_demands[20], color='dodgerblue', label = 'SOW Group 3')
axes[1].scatter(MD_URs[20], MD_demands[20], color='dodgerblue')
axes[2].scatter(LD_URs[20], LD_demands[20], color='dodgerblue')
axes[0].scatter(HD_URs[19], HD_demands[19], color='navy', label = 'SOW Group 4')
axes[1].scatter(MD_URs[19], MD_demands[19], color='navy')
axes[2].scatter(LD_URs[19], LD_demands[19], color='navy')
axes[0].tick_params(axis='y', labelsize=12)
axes[1].tick_params(axis='y', labelsize=12)
axes[2].tick_params(axis='y', labelsize=12)
axes[2].tick_params(axis='x', labelsize=14)
axes[0].legend(loc=(.82, 0.5), fontsize=10)
plt.subplots_adjust(hspace=0.05)
fig.text(0.06,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=14)
fig.text(.97, 0.25, 'Low Demands', ha='center', va='center', fontsize=12, color='tomato')
fig.text(.98, 0.5, 'Medium Demands', ha='center', va='center', fontsize=12, color='purple')
fig.text(.97, 0.75, 'High Demands', ha='center', va='center', fontsize=12, color='forestgreen')
fig.text(0.5, .05, 'Uniform Rate $/kgal', ha='center', va='center', fontsize=14)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig14_scatterplot.png', bbox_inches= 'tight', dpi=900)
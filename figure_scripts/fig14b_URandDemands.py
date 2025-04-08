# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:46:11 2023

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


scenarios = [4, 19, 20, 21, 22]
LD_demands = {}
MD_demands = {}
HD_demands = {}
LD_URs = {}
MD_URs = {}
HD_URs = {}
LD_CC = {}
MD_CC = {}
HD_CC = {}

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
    LD_CC[s], MD_CC[s], HD_CC[s] = hf.realization_3groups(combined_conditions, realization_groupings)

def calc_dict_successrate(dictionary, combined_conditions):
    successrate = {}
    for df_name, df in dictionary.items():
        nan_sum = df.isna().sum()
        failurerate = nan_sum / len(df.index)
        successrate[df_name] = (1 - failurerate)
    color_dfs = {}
    for series_name, data_series in successrate.items():
        color_df = pd.DataFrame()
        for year, value in data_series.items():
            color_df[year] = [value] * len(df.index)
            color_df.index = df.index
            color_df = color_df[combined_conditions[series_name]]
        color_dfs[series_name] = color_df
    return color_dfs

# def color_dfs(dictionary, profile_length):
    color_dfs = {}
    for series_name, data_series in dictionary.items():
        color_df = pd.DataFrame()
        for year, value in data_series.items():
            color_df[year] = [value] * profile_length
        color_dfs[series_name] = color_df
    return color_dfs
        

LD_demands_SR = calc_dict_successrate(LD_demands, LD_CC)
MD_demands_SR = calc_dict_successrate(MD_demands, MD_CC)
HD_demands_SR = calc_dict_successrate(HD_demands, HD_CC)
LD_UR_SR = calc_dict_successrate(LD_URs, LD_CC)
MD_UR_SR = calc_dict_successrate(MD_URs, MD_CC)
HD_UR_SR = calc_dict_successrate(HD_URs, HD_CC)


    
fig, axes = plt.subplots(3, 5, figsize=(25,15), sharex=True)
for index, row in HD_demands_SR[4].iterrows():
    for column in HD_demands_SR[4].columns:
        axes[0, 0].scatter(HD_URs[4].loc[index, column], HD_demands[4].loc[index,column], c=HD_demands_SR[4].loc[index,column], cmap='RdYlGn')
for index, row in MD_demands_SR[4].iterrows():
    for column in MD_demands_SR[4].columns:
        axes[1, 0].scatter(MD_URs[4].loc[index, column], MD_demands[4].loc[index,column], c=MD_demands_SR[4].loc[index,column], cmap='RdYlGn')
for index, row in LD_demands_SR[4].iterrows():
    for column in LD_demands_SR[4].columns:
        axes[2, 0].scatter(LD_URs[4].loc[index, column], LD_demands[4].loc[index,column], c=LD_demands_SR[4].loc[index,column], cmap='RdYlGn')
axes[2, 0].scatter(LD_URs[4], LD_demands[4], color='darkorange')
axes[0, 1].scatter(HD_URs[22].values, HD_demands[22].values, c=HD_demands_SR[22].values, cmap='RdYlGn', marker='d', label='SOW Group X')
axes[1, 1].scatter(MD_URs[22], MD_demands[22], color='green', marker='d',)
axes[2, 1].scatter(LD_URs[22], LD_demands[22], color='green', marker='d',)
axes[0, 2].scatter(HD_URs[21].values, HD_demands[21].values, c=HD_demands_SR[21].values, cmap='RdYlGn', label='SOW Group 2')
axes[1, 2].scatter(MD_URs[21], MD_demands[21], color='aqua')
axes[2, 2].scatter(LD_URs[21], LD_demands[21], color='aqua')
axes[0, 3].scatter(HD_URs[20].values, HD_demands[20].values, c=HD_demands_SR[20].values, cmap='RdYlGn', label = 'SOW Group 3')
axes[1, 3].scatter(MD_URs[20], MD_demands[20], color='dodgerblue')
axes[2, 3].scatter(LD_URs[20], LD_demands[20], color='dodgerblue')
axes[0, 4].scatter(HD_URs[19].values, HD_demands[19].values, c=HD_demands_SR[19].values, cmap='RdYlGn', label = 'SOW Group 4')
axes[1, 4].scatter(MD_URs[19], MD_demands[19], color='navy')
axes[2, 4].scatter(LD_URs[19], LD_demands[19], color='navy')
# axes[0].tick_params(axis='y', labelsize=12)
# axes[1].tick_params(axis='y', labelsize=12)
# axes[2].tick_params(axis='y', labelsize=12)
# axes[2].tick_params(axis='x', labelsize=14)
# axes[0].legend(loc=(.82, 0.5), fontsize=10)
plt.subplots_adjust(hspace=0.05, wspace=0.05)
# fig.text(0.06,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=14)
# fig.text(.97, 0.25, 'Low Demands', ha='center', va='center', fontsize=12, color='tomato')
# fig.text(.98, 0.5, 'Medium Demands', ha='center', va='center', fontsize=12, color='purple')
# fig.text(.97, 0.75, 'High Demands', ha='center', va='center', fontsize=12, color='forestgreen')
# fig.text(0.5, .05, 'Uniform Rate $/kgal', ha='center', va='center', fontsize=14)
#plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig14_scatterplot.png', bbox_inches= 'tight', dpi=900)
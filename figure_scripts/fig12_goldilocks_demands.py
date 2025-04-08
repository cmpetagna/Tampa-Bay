# -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:55:40 2023
This version of the figure is just the realizations that successfully meet each metric every year (imo not that insightful)
@author: cmpet
"""

import numpy as np
import pandas as pd
#import financial_metrics_reliabilty_plots as fm
import helper_functions as hf
import demand_buckets as db
import matplotlib.pyplot as plt

shortfall_data = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
financial_data = 'D:/Modeloutput/'

#Looking for only realizations that have 0 critical shortfalls across all 20 years. Easiest way to do this is sum the shortfalls across the 20 years
#and then pick out the realizations whose sums are 0.
shortfall_data['shortfall sum'] = shortfall_data.sum(axis=1)

no_critical_shortfalls = shortfall_data[shortfall_data['shortfall sum'] == 0]
demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
demands = demands.iloc[:-1,:].T
demands = demands.reset_index()
demands = demands.iloc[:, 1:]

scenarios = [2,3,4]
success_demands = {}
UR_success = {}
UR = {}
for sim in scenarios:
    DC = pd.read_csv(financial_data + 'DC_f162_s' + str(sim) + '.csv', index_col=(0))
    RC = pd.read_csv(financial_data + 'RC_f162_s' + str(sim) + '.csv', index_col=(0))
    UR_data = pd.read_csv(financial_data + 'UR_f162_s' + str(sim) + '.csv', index_col=(0))
    UR_data = UR_data.iloc[:,2:]
    UR[sim] = UR_data
    
    DC_supply = DC[DC.index.isin(no_critical_shortfalls.index)]
    
    DC_success = (DC_supply >= 1).all(axis=1)
    DCandSupply_success = DC_supply[DC_success]
    
    RC_DC_supply = RC[RC.index.isin(DCandSupply_success.index)]
    RC_success = (RC_DC_supply >= 1.25).all(axis=1)
    RCDCandSupply_success = RC_DC_supply[RC_success]
    success_demands[sim] = demands[demands.index.isin(RCDCandSupply_success.index)]
    UR_success[sim] = UR_data[UR_data.index.isin(RCDCandSupply_success.index)]
    



##this figure includes the panel for demands and the uniform rate.
fig, ax = plt.subplots(2,3, figsize=(16,8))
for i in range(len(demands.iloc[:,0])):
    ax[0,0].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(demands.iloc[:,0])):
    ax[0,1].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(success_demands[3].iloc[:,0])):
    ax[0,1].plot(demands.columns, success_demands[3].iloc[i,:], c='gold')
for i in range(len(demands.iloc[:,0])):
    ax[0,2].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(success_demands[4].iloc[:,0])):
    ax[0,2].plot(demands.columns, success_demands[4].iloc[i,:], c='gold')
fig.text(0.5, 0.07, 'Fiscal Year', ha='center', va='center', fontsize=20)
fig.text(0.08, 0.71, 'Water Demand (MGD)', ha='center', va='center', rotation='vertical', fontsize=20)
fig.text(0.08, 0.3, 'Uniform Rate ($/kgal)', ha='center', va='center', rotation='vertical', fontsize=20)
ax[0,0].tick_params(bottom=False)
ax[0,1].tick_params(bottom=False)
ax[0,2].tick_params(bottom=False)
ax[0,0].set_xticklabels([])
ax[0,1].set_xticklabels([])
ax[0,2].set_xticklabels([])
fig.text(.25, 0.9, 'Policy B', ha='center', fontsize=20)
fig.text(.5, 0.9, 'Policy C', ha='center', fontsize=20)
fig.text(.78, 0.9, 'Policy D', ha='center', fontsize=20)

ax[1,0].fill_between(UR[2].columns,
np.max(UR[2]), 
np.min(UR[2]), 
color = 'grey', alpha = 0.4, linewidth = 2, edgecolor = 'grey')
ax[1,1].fill_between(UR[3].columns,
np.max(UR[3]), 
np.min(UR[3]), 
color = 'grey', alpha = 0.4, linewidth = 2, edgecolor = 'grey')
ax[1,1].fill_between(UR_success[3].columns,
np.max(UR_success[3]), 
np.min(UR_success[3]), 
color = 'gold', alpha = 0.6, linewidth = 2, edgecolor = 'gold')
ax[1,2].fill_between(UR[4].columns,
np.max(UR[4]), 
np.min(UR[4]), 
color = 'grey', alpha = 0.4, linewidth = 2, edgecolor = 'grey')
ax[1,2].fill_between(UR_success[4].columns,
np.max(UR_success[4]), 
np.min(UR_success[4]), 
color = 'gold', alpha = 0.6, linewidth = 2, edgecolor = 'gold')
ax[1,0].set_ylim((2.5, 4.5))
ax[1,1].set_ylim((2.5, 4.5))
ax[1,2].set_ylim((2.5, 4.5))
ax[1,0].tick_params('y', labelsize=14)
ax[1,1].tick_params('y', labelsize=14)
ax[1,2].tick_params('y', labelsize=14)
ax[0,0].tick_params('y', labelsize=14)
ax[0,1].tick_params('y', labelsize=14)
ax[0,2].tick_params('y', labelsize=14)
ax[1,0].set_xticks(['2021']+[str(x) for x in range(2025,2041, 5)])
ax[1,1].set_xticks(['2021']+[str(x) for x in range(2025,2041, 5)])
ax[1,2].set_xticks(['2021']+[str(x) for x in range(2025,2041, 5)])
ax[1,0].set_xticklabels(['2021']+[str(x) for x in range(2025,2041, 5)], fontsize=14)
ax[1,1].set_xticklabels(['2021']+[str(x) for x in range(2025,2041, 5)], fontsize=14)
ax[1,2].set_xticklabels(['2021']+[str(x) for x in range(2025,2041, 5)], fontsize=14)
ax[0,2].plot([], [], c='lightgrey', label='All 1,000 Realizations')
ax[0,2].plot([], [], c='gold', label='All Goals Met Every Year')
ax[0,2].legend(loc = (0.06,0.77), fontsize=12)
plt.subplots_adjust(hspace=0.08, wspace=0.15)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig12_GoldilocksZone_2.png', bbox_inches= 'tight', dpi=900)

##Just the panel that includes the demand goldilocks zone
# fig, ax = plt.subplots(1,3, figsize=(15,7), sharey=True, sharex=True)
# for i in range(len(demands.iloc[:,0])):
#     ax[0].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
# for i in range(len(demands.iloc[:,0])):
#     ax[1].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
# for i in range(len(success_demands[3].iloc[:,0])):
#     ax[1].plot(demands.columns, success_demands[3].iloc[i,:], c='gold')
# for i in range(len(demands.iloc[:,0])):
#     ax[2].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
# for i in range(len(success_demands[4].iloc[:,0])):
#     ax[2].plot(demands.columns, success_demands[4].iloc[i,:], c='gold')
# ax[2].plot([], [], c='lightgrey', label='All 1,000 Realizations')
# ax[2].plot([], [], c='gold', label='Realizations with All Goals\nMet Every Year')
# ax[2].legend(loc = (0.075,0.8), fontsize=14)
# fig.text(0.5, 0.05, 'Fiscal Year', ha='center', va='center', fontsize=20)
# fig.text(0.08, 0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='vertical', fontsize=20)
# ax[2].set_xlim([2021, 2040])
# ax[0].set_ylim([160, 250])
# ax[1].set_ylim([160, 250])
# ax[2].set_ylim([160, 250])
# ax[2].set_xticks([2025, 2030, 2035, 2040])
# ax[0].set_xticklabels([2025, 2030, 2035, 2040], fontsize=14)
# ax[1].set_xticklabels([2025, 2030, 2035, 2040], fontsize=14)
# ax[2].set_xticklabels([2025, 2030, 2035, 2040], fontsize=14)
# ax[0].set_yticklabels([''] + [170, 180, 190, 200, 210, 220, 230, 240] + [''], fontsize=14)
# # ax[1].set_yticklabels([''] + [170, 180, 190, 200, 210, 220, 230, 240] + [''], fontsize=14)
# # ax[2].set_yticklabels([''] + [170, 180, 190, 200, 210, 220, 230, 240] + [''], fontsize=14)
# fig.text(.25, 0.9, 'Uniform Rate Annual\nIncrease Cap of 2%', ha='center', fontsize=16)
# fig.text(.5, 0.9, 'Uniform Rate Annual\nIncrease Cap of 3%', ha='center', fontsize=16)
# fig.text(.78, 0.9, 'Uniform Rate Annual\nIncrease Cap of 4%', ha='center', fontsize=16)
# plt.subplots_adjust(wspace=0.08)
# #plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig12_GoldilocksZone_1.png', bbox_inches= 'tight', dpi=900)

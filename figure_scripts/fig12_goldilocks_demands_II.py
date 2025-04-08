# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:38:58 2023

@author: cmpet
"""


import numpy as np
import pandas as pd
#import financial_metrics_reliabilty_plots as fm
import helper_functions as hf
import demand_buckets as db
import matplotlib.pyplot as plt

realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)
failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
demands = demands.iloc[:-1,:].T
demands = demands.reset_index()
demands = demands.iloc[:, 1:]

def annual_supply_reliability(failure_durations):
    realizations_wo_shortfall = []
    for year in range(0, len(failure_durations.columns)):
        realizations_wo_shortfall.append((failure_durations.iloc[:,year] == 0).sum())
    realizations_wo_shortfall = np.array((realizations_wo_shortfall))
    success_by_year = (realizations_wo_shortfall/len(failure_durations.index))
    return success_by_year

successful_supply_reliability = annual_supply_reliability(failure_durations)



simulation_list = [1, 2, 3, 4]
filtered_success_demands={}
filtered_success_UR={}

for sim in simulation_list:
    DC = pd.read_csv('D:/Modeloutput/DC_f162_s' + str(sim) + '.csv', index_col=0)
    RC = pd.read_csv('D:/Modeloutput/RC_f162_s' + str(sim) + '.csv', index_col=0)
    UR = pd.read_csv('D:/Modeloutput/UR_f162_s' + str(sim) + '.csv', index_col=0)
    #UR.reset_index(inplace=True)
    UR = UR.iloc[:, 2:]
    UR.columns=demands.columns
    #UR_data[sim] = UR
    #UR_pctchange = UR.pct_change(axis=1)

    def annual_financial_reliability(metric_data, metric):
        realizations_wo_failure = []
        for year in range(0, len(metric_data.columns)):
            realizations_wo_failure.append((metric_data.iloc[:, year] >= metric).sum())
        realizations_wo_failure = np.array((realizations_wo_failure))
        success_by_year = (realizations_wo_failure/len(metric_data.index))
        return success_by_year

    success_DC = annual_financial_reliability(DC, 1)
    success_RC = annual_financial_reliability(RC, 1.25)

    all_three_success = np.zeros((len(failure_durations.index),len(failure_durations.columns)))
    all_three_success = pd.DataFrame(all_three_success, columns=demands.columns)
    for i in range(0,len(all_three_success.columns)):
        for j in range(0,len(all_three_success.index)):
            all_three_success.iloc[j,i] = (failure_durations.iloc[j,i] == 0) & (DC.iloc[j,i] >= 1) & (RC.iloc[j,i] >= 1.25)
            
    #success_demands = pd.concat([demands, all_three_success], axis=1)
    filtered_success_demands[sim] = demands[all_three_success]
    #success_UR = pd.concat([UR, all_three_success], axis=1)
    #filtered_success_UR[sim] = UR.iloc[:,:] * all_three_success.iloc[:,:]
    filtered_success_UR[sim] = UR[all_three_success]

for key, df in filtered_success_demands.items():
    filtered_success_demands[key] = df.apply(np.ma.masked_invalid)




##this figure includes the panel for demands and the uniform rate.
fig, ax = plt.subplots(2,3, figsize=(16,8))
#for i in range(len(demands.iloc[:,0])):
#    ax[0,0].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(filtered_success_demands[2].iloc[:,0])):
    ax[0,0].scatter(filtered_success_demands[2].columns, filtered_success_demands[2].iloc[i,:], c='black', alpha=.1)
#ax[0,0].fill_between(filtered_success_demands[2].columns, np.max(filtered_success_demands[2]), np.min(filtered_success_demands[2]), color='gold', alpha=0.4, linewidth=2, edgecolor='gold')
#for i in range(len(demands.iloc[:,0])):
#    ax[0,1].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(filtered_success_demands[3].iloc[:,0])):
    ax[0,1].scatter(filtered_success_demands[3].columns, filtered_success_demands[3].iloc[i,:], c='gold')
#for i in range(len(success_demands[3].iloc[:,0])):
#    ax[0,1].plot(demands.columns, success_demands[3].iloc[i,:], c='gold')
#for i in range(len(demands.iloc[:,0])):
#    ax[0,2].plot(demands.columns, demands.iloc[i,:], c='lightgrey')
for i in range(len(filtered_success_demands[4].iloc[:,0])):
    ax[0,2].scatter(filtered_success_demands[4].columns, filtered_success_demands[4].iloc[i,:], c='gold')
#for i in range(len(success_demands[4].iloc[:,0])):
#    ax[0,2].plot(demands.columns, success_demands[4].iloc[i,:], c='gold')
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
#ax[1,1].fill_between(UR_success[3].columns,
#np.max(UR_success[3]), 
#np.min(UR_success[3]), 
#color = 'gold', alpha = 0.6, linewidth = 2, edgecolor = 'gold')
ax[1,2].fill_between(UR[4].columns,
np.max(UR[4]), 
np.min(UR[4]), 
color = 'grey', alpha = 0.4, linewidth = 2, edgecolor = 'grey')
#ax[1,2].fill_between(UR_success[4].columns,
#np.max(UR_success[4]), 
#np.min(UR_success[4]), 
#color = 'gold', alpha = 0.6, linewidth = 2, edgecolor = 'gold')
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
#plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig12_GoldilocksZone_2.png', bbox_inches= 'tight', dpi=900)

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

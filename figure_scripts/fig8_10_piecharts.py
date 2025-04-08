# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:46:40 2023
pie chart figures for all metrics. supply and financial
@author: cmpet
"""

import pandas as pd
import numpy as np
#import demand_buckets as buckets
import helper_functions as hf
#from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
#import matplotlib as mpl
import seaborn as sns
sns.set
#from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap

##bringing in the slack variable table
failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
#failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162_no_sch.csv', header=None)

#demand realization groupings
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)


low_demands_reliability, med_demands_reliability, high_demands_reliability = hf.realization_3groups(failure_durations, realization_groupings)

#successful realizations each year for supply reliability.
def annual_supply_reliability(failure_durations):
    realizations_wo_shortfall = []
    for year in range(0, len(failure_durations.columns)):
        realizations_wo_shortfall.append((failure_durations.iloc[:,year] == 0).sum())
    realizations_wo_shortfall = np.array((realizations_wo_shortfall))
    success_by_year = (realizations_wo_shortfall/len(failure_durations.index)) * 100
    return success_by_year

LD_successful_supply_reliability = annual_supply_reliability(low_demands_reliability)
MD_successful_supply_reliability = annual_supply_reliability(med_demands_reliability)
HD_successful_supply_reliability = annual_supply_reliability(high_demands_reliability)

simulation_list = [1]

#pulling the covenant and uniform rate data
for sim in simulation_list:
    DC = pd.read_csv('D:/Modeloutput/DC_f162_s' + str(sim) + '.csv', index_col=0)
    RC = pd.read_csv('D:/Modeloutput/RC_f162_s' + str(sim) + '.csv', index_col=0)
    UR = pd.read_csv('D:/Modeloutput/UR_f162_s' + str(sim) + '.csv', index_col=0)
    UR = UR.iloc[:, 2:]
    UR_pctchange = UR.pct_change(axis=1)

low_demand_DC, med_demand_DC, high_demand_DC = hf.realization_3groups(DC, realization_groupings)
low_demand_RC, med_demand_RC, high_demand_RC = hf.realization_3groups(RC, realization_groupings)

#percent of financially (either debt or rate covenant) in each year.
def annual_financial_reliability(metric_data, metric):
    realizations_wo_failure = []
    for year in range(0, len(metric_data.columns)):
        realizations_wo_failure.append((metric_data.iloc[:, year] >= metric).sum())
    realizations_wo_failure = np.array((realizations_wo_failure))
    success_by_year = (realizations_wo_failure/len(metric_data.index)) * 100
    return success_by_year

LD_success_DC = annual_financial_reliability(low_demand_DC, 1)
MD_success_DC = annual_financial_reliability(med_demand_DC, 1)
HD_success_DC = annual_financial_reliability(high_demand_DC, 1)

LD_success_RC = annual_financial_reliability(low_demand_RC, 1.25)
MD_success_RC = annual_financial_reliability(med_demand_RC, 1.25)
HD_success_RC = annual_financial_reliability(high_demand_RC, 1.25)

#realizations that meet all three metrics table 0 for fail 1 for succuess.
all_three_success = np.zeros((len(failure_durations.index),len(failure_durations.columns)))
all_three_success = pd.DataFrame(all_three_success)
for i in range(0,len(all_three_success.columns)):
    for j in range(0,len(all_three_success.index)):
        all_three_success.iloc[j,i] = (failure_durations.iloc[j,i] == 0) & (DC.iloc[j,i] >= 1) & (RC.iloc[j,i] >= 1.25)

low_demand_success, med_demand_success, high_demand_success = hf.realization_3groups(all_three_success, realization_groupings)

#percent of all realizations which successfully meet all metrics
def all_metric_success(data):
    realizations_true = []
    for year in range(0, len(data.columns)):
        realizations_true.append((data.iloc[:, year] == True).sum())
    realizations_true = np.array(realizations_true)
    success_by_year = (realizations_true/len(data.index)) * 100
    return success_by_year

LD_success = all_metric_success(low_demand_success)
MD_success = all_metric_success(med_demand_success)
HD_success = all_metric_success(high_demand_success)

years = [x for x in range(2021, 2041)]


###PIE Charts

fig2, axes = plt.subplots(12, 20, figsize=(30,20))
colors = ['dimgrey', 'red']
# row_labels = [
#     'Supply\nReliability',
#     'Debt\nCovenant',
#     'Rate\nCovenant',
#     'All\nGoals Met',
#     'Supply\nReliability',
#     'Debt\nCovenant',
#     'Rate\nCovenant',
#     'All\nGoals Met',
#     'Supply\nReliability',
#     'Debt\nCovenant',
#     'Rate\nCovenant',
#     'All\nGoals Met']

# for i, label in enumerate(row_labels[:12]):
#     axes[i, 0].set_ylabel(label, rotation=90)
#     #axes[i, 0].tick_params(axis='y', labelrotation=90)

for year in range(0, 20):
    axes[0, year].pie([HD_successful_supply_reliability[year], (100-HD_successful_supply_reliability[year])], colors=colors)
    axes[1, year].pie([HD_success_DC[year], (100-HD_success_DC[year])], colors=colors)
    axes[2, year].pie([HD_success_RC[year], (100-HD_success_RC[year])], colors=colors)
    axes[3, year].pie([HD_success[year], (100-HD_success[year])], colors=colors)
    axes[4, year].pie([MD_successful_supply_reliability[year], (100-MD_successful_supply_reliability[year])], colors=colors)
    axes[5, year].pie([MD_success_DC[year], (100-MD_success_DC[year])], colors=colors)
    axes[6, year].pie([MD_success_RC[year], (100-MD_success_RC[year])], colors=colors)
    axes[7, year].pie([MD_success[year], (100-MD_success[year])], colors=colors)
    axes[8, year].pie([LD_successful_supply_reliability[year], (100-LD_successful_supply_reliability[year])], colors=colors)
    axes[9, year].pie([LD_success_DC[year], (100-LD_success_DC[year])], colors=colors)
    axes[10, year].pie([LD_success_RC[year], (100-LD_success_RC[year])], colors=colors)
    axes[11, year].pie([LD_success[year], (100-LD_success[year])], colors=colors)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig8_1pctUR.png', bbox_inches= 'tight', dpi=900)

# fig3, axes = plt.subplots(3, 20, figsize=(30,5))
# colors= ['dimgrey', 'red']
# for year in range(0, 20):
#     axes[0, year].pie([LD_success[year], (100-LD_success[year])], colors=colors)
#     axes[1, year].pie([MD_success[year], (100-MD_success[year])], colors=colors)
#     axes[2, year].pie([HD_success[year], (100-HD_success[year])], colors=colors)

# # ##Uniform rate ranges
# # low_demands_UR, med_demands_UR, high_demands_UR = hf.realization_3groups(UR, realization_groupings)
# # fig3, axes= plt.subplots(1,1)
# # axes.fill_between(years,
# # np.max(med_demands_UR, axis = 0), 
# # np.min(med_demands_UR, axis = 0), 
# # color = 'purple', 
# # alpha = 0.4,  linewidth = 2,
# # edgecolor = 'purple')
# # axes.set_ylim((2.5, 6.5))
# # #axes.set_xticks([str(x) for x in years])
# # #axes.set_xticklabels([str(x) for x in years])
# # axes.set_ylabel('$/kgal')
# # #axes.set_title('Uniform Rate')
# # plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/EWRI/7p_UR_LD.png', bbox_inches= 'tight', dpi=900)

####rates of success displayed as plots
# fig, axes = plt.subplots(3, 1, figsize=(10,7), sharex=True, sharey=True)
# #axes[0].plot(years, LD_successful_supply_reliability, linestyle = 'dashdot', color = 'tomato', linewidth=3)
# #axes[0].plot(years, LD_success_DC, linestyle = 'dashed', color = 'tomato', linewidth=3)
# axes[0].plot(years, LD_success_RC, linestyle = 'dotted', color = 'tomato', linewidth=3)
# #axes[0].plot(years, LD_success, linestyle = 'solid', color = 'tomato', linewidth=3)
# #axes[1].plot(years, MD_successful_supply_reliability, linestyle = 'dashdot', color = 'purple', linewidth=3)
# #axes[1].plot(years, MD_success_DC, linestyle = 'dashed', color = 'purple', linewidth=3)
# axes[1].plot(years, MD_success_RC, linestyle = 'dotted', color = 'purple', linewidth=3)
# #axes[1].plot(years, MD_success, linestyle = 'solid', color = 'purple', linewidth=3)
# #axes[2].plot(years, HD_successful_supply_reliability, color = 'forestgreen', linestyle = 'dashdot', linewidth=3)
# #axes[2].plot(years, HD_success_DC, linestyle = 'dashed', color = 'forestgreen', linewidth=3)
# axes[2].plot(years, HD_success_RC, linestyle = 'dotted', color = 'forestgreen', linewidth=3)
# #axes[2].plot(years, HD_success, linestyle = 'solid', color = 'forestgreen', linewidth=3)
# axes[0].set_ylim(0,110)
# #axes[0].grid(True)
# axes[1].set_ylim(0,110)
# #axes[1].grid(True)
# axes[2].set_ylim(0,110)
# #axes[2].grid(True)
# axes[2].set_xticks(years)
# axes[2].set_xticklabels([str(x) for x in range(2021, 2041)], rotation=90)

# demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
# demands = demands.iloc[:-1,:].T
# demands = demands.reset_index()
# demands = demands.iloc[:, 1:]
# low_demands, med_demands, high_demands = hf.realization_3groups(demands, realization_groupings)
# min_demands = np.min(demands, axis=0)
# max_demands = np.max(demands, axis=0)

# demands_array = demands.to_numpy()
# years = [float(x) for x in range(2021,2041)]
# fig, ax = plt.subplots(figsize=(20,15))
# #ax.fill_between(years, np.max(med_demands, axis=0), np.min(med_demands, axis=0), color = 'gold', linewidth=2, edgecolor = 'gold')
# for i in range(len(demands_array[:, 0])):
#     ax.plot(years, demands_array[i, :], c='lightgrey', alpha=0.2)
# ax.plot(years, min_demands, color = 'dimgrey', linewidth=3, linestyle= ':')
# ax.plot(years, max_demands, color = 'dimgrey', linewidth=3, linestyle= ':')
# #ax.plot(years, test, color = 'gold', linewidth=5, linestyle = 'dashed')
# ax.fill_between(years, np.max(med_demands, axis=0), np.min(med_demands, axis=0), color = 'gold', linewidth=2, edgecolor = 'gold')
# ax.set_ylabel('Demands (MGD)', fontsize=28)
# ax.set_yticklabels([0, 170, 180, 190, 200, 210, 220, 230, 240], fontsize=28)
# # ax.set_xticks([str(x) for x in range(2021, 2041, 1)])
# # ax.set_xticklabels([str(x) for x in range(2021, 2041, 1)], rotation = 90, fontsize = 20)
# # plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/EWRI/3p_demand_range_LD_wline.png', bbox_inches= 'tight', dpi=900)
# # test=np.max(med_demands, axis=0)
# # test2=np.max(med_demands, axis=0)
# # decrease = ((test - test2)/test) * 100
# # decreasemean = decrease.mean()
# # testgrowth = test.pct_change()
# # test2growth = test2.pct_change()
# # decgrowth = ((testgrowth - test2growth)/testgrowth)
# # decgrowthmean=decgrowth.mean()
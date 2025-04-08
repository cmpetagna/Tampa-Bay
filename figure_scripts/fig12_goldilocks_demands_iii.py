# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:46:11 2023
Final Goldilocks Zone Figure
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
LD_demands = {}
MD_demands = {}
HD_demands = {}

LD_URs = {}
MD_URs = {}
HD_URs = {}

LD_CC = {}
MD_CC = {}
HD_CC = {}

LD_UR_total = {}
MD_UR_total = {}
HD_UR_total = {}

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
    demands.columns = combined_conditions.columns
    
    UR_filter = UR[combined_conditions]
    demand_filter = demands[combined_conditions]
    
    LD_UR_total[s], MD_UR_total[s], HD_UR_total[s] = hf.realization_3groups(UR, realization_groupings)
    LD_demands[s], MD_demands[s], HD_demands[s] = hf.realization_3groups(demand_filter, realization_groupings)
    LD_URs[s], MD_URs[s], HD_URs[s] = hf.realization_3groups(UR_filter, realization_groupings)
    LD_CC[s], MD_CC[s], HD_CC[s] = hf.realization_3groups(combined_conditions, realization_groupings)

LD_demands_total, MD_demands_total, HD_demands_total = hf.realization_3groups(demands, realization_groupings)

preproject_years = [str(x) for x in range(2021, 2028)]
postproject_years = [str(x) for x in range(2028,2041)]
fig, axes = plt.subplots(3, 4, figsize=(30,20), sharey=True, sharex='col')
axes[0,0].scatter(HD_UR_total[1], HD_demands_total, color='lightgrey', )
axes[0,0].scatter(HD_URs[1].loc[:,preproject_years], HD_demands[1].loc[:,preproject_years], color='darkgoldenrod')
axes[0,0].scatter(HD_URs[1].loc[:,postproject_years], HD_demands[1].loc[:,postproject_years], color='gold')
axes[1,0].scatter(MD_UR_total[1], MD_demands_total, color='lightgrey')
axes[1,0].scatter(MD_URs[1].loc[:,preproject_years], MD_demands[1].loc[:,preproject_years], color='darkgoldenrod')
axes[1,0].scatter(MD_URs[1].loc[:,postproject_years], MD_demands[1].loc[:,postproject_years], color='gold')
axes[2,0].scatter(LD_UR_total[1], LD_demands_total, color='lightgrey', marker='.')
axes[2,0].scatter(LD_URs[1].loc[:,preproject_years], LD_demands[1].loc[:,preproject_years], color='darkgoldenrod')
axes[2,0].scatter(LD_URs[1].loc[:,postproject_years], LD_demands[1].loc[:,postproject_years], color='gold')
axes[0,1].scatter(HD_UR_total[2], HD_demands_total, color='lightgrey')
axes[0,1].scatter(HD_URs[2].loc[:,preproject_years], HD_demands[2].loc[:,preproject_years], color='darkgoldenrod')
axes[0,1].scatter(HD_URs[2].loc[:,postproject_years], HD_demands[2].loc[:,postproject_years], color='gold')
axes[1,1].scatter(MD_UR_total[2], MD_demands_total, color='lightgrey')
axes[1,1].scatter(MD_URs[2].loc[:,preproject_years], MD_demands[2].loc[:,preproject_years], color='darkgoldenrod')
axes[1,1].scatter(MD_URs[2].loc[:,postproject_years], MD_demands[2].loc[:,postproject_years], color='gold')
axes[2,1].scatter(LD_UR_total[2], LD_demands_total, color='lightgrey')
axes[2,1].scatter(LD_URs[2].loc[:,preproject_years], LD_demands[2].loc[:,preproject_years], color='darkgoldenrod')
axes[2,1].scatter(LD_URs[2].loc[:,postproject_years], LD_demands[2].loc[:,postproject_years], color='gold')
axes[0,2].scatter(HD_UR_total[3], HD_demands_total, color='lightgrey')
axes[0,2].scatter(HD_URs[3].loc[:,preproject_years], HD_demands[3].loc[:,preproject_years], color='darkgoldenrod')
axes[0,2].scatter(HD_URs[3].loc[:,postproject_years], HD_demands[3].loc[:,postproject_years], color='gold')
axes[1,2].scatter(MD_UR_total[3], MD_demands_total, color='lightgrey')
axes[1,2].scatter(MD_URs[3].loc[:,preproject_years], MD_demands[3].loc[:,preproject_years], color='darkgoldenrod')
axes[1,2].scatter(MD_URs[3].loc[:,postproject_years], MD_demands[3].loc[:,postproject_years], color='gold')
axes[2,2].scatter(LD_UR_total[3], LD_demands_total, color='lightgrey')
axes[2,2].scatter(LD_URs[3].loc[:,preproject_years], LD_demands[3].loc[:,preproject_years], color='darkgoldenrod')
axes[2,2].scatter(LD_URs[3].loc[:,postproject_years], LD_demands[3].loc[:,postproject_years], color='gold')
axes[0,3].scatter(HD_UR_total[4], HD_demands_total, color='lightgrey', label='Unsuccessful Year')
axes[0,3].scatter(HD_URs[4].loc[:,preproject_years], HD_demands[4].loc[:,preproject_years], color='darkgoldenrod', label='All Goals Met Before \'28 Supply Project')
axes[0,3].scatter(HD_URs[4].loc[:,postproject_years], HD_demands[4].loc[:,postproject_years], color='gold', label='All Goals Met After \'28 Supply Project')
axes[1,3].scatter(MD_UR_total[4], MD_demands_total, color='lightgrey')
axes[1,3].scatter(MD_URs[4].loc[:,preproject_years], MD_demands[4].loc[:,preproject_years], color='darkgoldenrod')
axes[1,3].scatter(MD_URs[4].loc[:,postproject_years], MD_demands[4].loc[:,postproject_years], color='gold')
axes[2,3].scatter(LD_UR_total[4], LD_demands_total, color='lightgrey')
axes[2,3].scatter(LD_URs[4].loc[:,preproject_years], LD_demands[4].loc[:,preproject_years], color='darkgoldenrod')
axes[2,3].scatter(LD_URs[4].loc[:,postproject_years], LD_demands[4].loc[:,postproject_years], color='gold')
axes[0,0].tick_params(axis='y', labelsize=24)
axes[1,0].tick_params(axis='y', labelsize=24)
axes[2,2].set_xticks([2.6, 3.0, 3.4, 3.8, 4.2])
axes[2,3].set_xticks([2.6, 3.0, 3.4, 3.8, 4.2])
axes[2,0].tick_params(axis='y', labelsize=24)
axes[2,0].tick_params(axis='x', labelsize=24)
axes[2,1].tick_params(axis='x', labelsize=24)
axes[2,2].tick_params(axis='x', labelsize=24)
axes[2,3].tick_params(axis='x', labelsize=24)
lines, labels = axes[0,3].get_legend_handles_labels()
fig.legend(lines, labels, loc=(.1, 0.02), mode='justify', ncol=3, markerscale=7, fontsize=24, frameon=False)
#plt.legend(loc='best', markerscale=2)
plt.subplots_adjust(hspace=0.05, wspace=0.05)
fig.text(0.09,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=28,  weight='bold')
fig.text(.935, 0.25, 'Low\nDemands', ha='center', va='center', fontsize=28, color='tomato')
fig.text(.935, 0.5, 'Medium\nDemands', ha='center', va='center', fontsize=28, color='purple')
fig.text(.935, 0.75, 'High\nDemands', ha='center', va='center', fontsize=28, color='forestgreen')
fig.text(0.5, 0.09, 'Volumetric Rate $/kgal', ha='center', va='center', fontsize=28,  weight='bold')
fig.text(.2, .9, r'Policy A ($\leq$1%)', ha='center', va='center', fontsize=28, weight='bold')
fig.text(.4, .9, r'Policy B ($\leq$2%)', ha='center', va='center', fontsize=28, weight='bold')
fig.text(.6, .9, r'Policy C ($\leq$3%)', ha='center', va='center', fontsize=28, weight='bold')
fig.text(.8, .9, r'Policy D ($\leq$4%)', ha='center', va='center', fontsize=28, weight='bold')
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig12_goldilocks_ptIII.png', bbox_inches= 'tight', dpi=400)

# fig2, axes = plt.subplots(1, 1, figsize=(8,8))
# axes.scatter(HD_UR_total[1], HD_demands_total, color='lightgrey', )
# axes.scatter(HD_URs[1].loc[:,preproject_years], HD_demands[1].loc[:,preproject_years], color='darkgoldenrod')
# axes.scatter(HD_URs[1].loc[:,postproject_years], HD_demands[1].loc[:,postproject_years], color='gold')
# axes.set_yticks([180, 200, 220, 240])
# axes.tick_params(axis='y', labelsize=24)
# axes.tick_params(axis='x', labelsize=24)
# fig2.text(.5, .9, r'Policy A ($\leq$1%)', ha='center', va='center', fontsize=24, weight='bold')
# fig2.text(0.01,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=24,  weight='bold')
# fig2.text(0.5, 0.03, 'Volumetric Rate $/kgal', ha='center', va='center', fontsize=24,  weight='bold')
# plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig12_goldilocks_HD_A.png', bbox_inches= 'tight', dpi=400)

# fig3, axes = plt.subplots(1, 1, figsize=(8,8))
# axes.scatter(LD_UR_total[4], LD_demands_total, color='lightgrey')
# axes.scatter(LD_URs[4].loc[:,preproject_years], LD_demands[4].loc[:,preproject_years], color='darkgoldenrod')
# axes.scatter(LD_URs[4].loc[:,postproject_years], LD_demands[4].loc[:,postproject_years], color='gold')
# axes.set_yticks([180, 200, 220, 240])
# axes.set_xticks([2.6, 3.0, 3.4, 3.8, 4.2])
# axes.tick_params(axis='y', labelsize=24)
# axes.tick_params(axis='x', labelsize=24)
# fig3.text(.5, .9, r'Policy D ($\leq$4%)', ha='center', va='center', fontsize=24, weight='bold')
# fig3.text(0.01,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=24,  weight='bold')
# fig3.text(0.5, 0.03, 'Volumetric Rate $/kgal', ha='center', va='center', fontsize=24,  weight='bold')
# plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig12_goldilocks_LD_D.png', bbox_inches= 'tight', dpi=400)

# fig3, axes = plt.subplots(1, 2, figsize=(15,8), sharey=True, sharex=True)
# axes[0].scatter(MD_UR_total[2], MD_demands_total, color='lightgrey')
# axes[0].scatter(MD_URs[2].loc[:,preproject_years], MD_demands[2].loc[:,preproject_years], color='darkgoldenrod')
# axes[0].scatter(MD_URs[2].loc[:,postproject_years], MD_demands[2].loc[:,postproject_years], color='gold')
# axes[1].scatter(MD_UR_total[3], MD_demands_total, color='lightgrey')
# axes[1].scatter(MD_URs[3].loc[:,preproject_years], MD_demands[3].loc[:,preproject_years], color='darkgoldenrod')
# axes[1].scatter(MD_URs[3].loc[:,postproject_years], MD_demands[3].loc[:,postproject_years], color='gold')
# axes[0].set_ylim(180,240)
# axes[0].set_yticks([180, 200, 220, 240])
# #axes[0].set_ylabel([180, 200, 220, 240])
# axes[0].set_xticks([2.6, 3.0, 3.4, 3.8])
# axes[1].set_xticks([2.6, 3.0, 3.4, 3.8])
# axes[0].tick_params(axis='y', labelsize=24)
# axes[0].tick_params(axis='x', labelsize=24)
# axes[1].tick_params(axis='x', labelsize=24)
# fig3.text(.3, .9, r'Policy B ($\leq$2%)', ha='center', va='center', fontsize=24, weight='bold')
# fig3.text(.7, .9, r'Policy C ($\leq$3%)', ha='center', va='center', fontsize=24, weight='bold')
# fig3.text(0.05,0.5, 'Water Demand (MGD)', ha='center', va='center', rotation='90',fontsize=24,  weight='bold')
# fig3.text(0.5, 0.03, 'Volumetric Rate $/kgal', ha='center', va='center', fontsize=24,  weight='bold')
# plt.subplots_adjust(wspace=0.05)
# plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig12_goldilocks_best.png', bbox_inches= 'tight', dpi=400)
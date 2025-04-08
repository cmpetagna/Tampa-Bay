# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:59:26 2023
Compares the success of different uniform rate policies against all the metrics.
@author: cmpet
"""

import pandas as pd
import numpy as np
#import demand_buckets as buckets
import helper_functions as hf
#from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
#import matplotlib as mpl
# import seaborn as sns
# sns.set
#from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap

realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)


failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
low_demands_reliability, med_demands_reliability, high_demands_reliability = hf.realization_3groups(failure_durations, realization_groupings)

#probably should have put this function in the helper function script instead of repeating it 4 times.
def annual_supply_reliability(failure_durations):
    realizations_wo_shortfall = []
    for year in range(0, len(failure_durations.columns)):
        realizations_wo_shortfall.append((failure_durations.iloc[:,year] == 0).sum())
    realizations_wo_shortfall = np.array((realizations_wo_shortfall))
    success_by_year = ((realizations_wo_shortfall/len(failure_durations.index)) * 100)
    return success_by_year

LD_successful_supply_reliability = annual_supply_reliability(low_demands_reliability)
MD_successful_supply_reliability = annual_supply_reliability(med_demands_reliability)
HD_successful_supply_reliability = annual_supply_reliability(high_demands_reliability)

LD_success = {}
MD_success = {}
HD_success = {}

simulation_list = [1, 2, 3, 4]

for sim in simulation_list:
    DC = pd.read_csv('D:/Modeloutput/DC_f162_s' + str(sim) + '.csv', index_col=0)
    RC = pd.read_csv('D:/Modeloutput/RC_f162_s' + str(sim) + '.csv', index_col=0)
    UR = pd.read_csv('D:/Modeloutput/UR_f162_s' + str(sim) + '.csv', index_col=0)
    UR = UR.iloc[:, 2:]
    UR_pctchange = UR.pct_change(axis=1)

    low_demand_DC, med_demand_DC, high_demand_DC = hf.realization_3groups(DC, realization_groupings)
    low_demand_RC, med_demand_RC, high_demand_RC = hf.realization_3groups(RC, realization_groupings)

#financial reliability
    def annual_financial_reliability(metric_data, metric):
        realizations_wo_failure = []
        for year in range(0, len(metric_data.columns)):
            realizations_wo_failure.append((metric_data.iloc[:, year] >= metric).sum())
        realizations_wo_failure = np.array((realizations_wo_failure))
        success_by_year = (realizations_wo_failure/len(metric_data.index))
        return success_by_year

    LD_success_DC = annual_financial_reliability(low_demand_DC, 1)
    MD_success_DC = annual_financial_reliability(med_demand_DC, 1)
    HD_success_DC = annual_financial_reliability(high_demand_DC, 1)

    LD_success_RC = annual_financial_reliability(low_demand_RC, 1.25)
    MD_success_RC = annual_financial_reliability(med_demand_RC, 1.25)
    HD_success_RC = annual_financial_reliability(high_demand_RC, 1.25)

    all_three_success = np.zeros((len(failure_durations.index),len(failure_durations.columns)))
    all_three_success = pd.DataFrame(all_three_success)
    for i in range(0,len(all_three_success.columns)):
        for j in range(0,len(all_three_success.index)):
            all_three_success.iloc[j,i] = (failure_durations.iloc[j,i] == 0) & (DC.iloc[j,i] >= 1) & (RC.iloc[j,i] >= 1.25)

    low_demand_success, med_demand_success, high_demand_success = hf.realization_3groups(all_three_success, realization_groupings)


    def all_metric_success(data):
        realizations_true = []
        for year in range(0, len(data.columns)):
            realizations_true.append((data.iloc[:, year] == True).sum())
        realizations_true = np.array(realizations_true)
        success_by_year = ((realizations_true/len(data.index)) * 100)
        return success_by_year

    LD_success[sim] = all_metric_success(low_demand_success)
    MD_success[sim] = all_metric_success(med_demand_success)
    HD_success[sim] = all_metric_success(high_demand_success)

years = [x for x in range(2021, 2041)]

fig, axes = plt.subplots(3, 1, figsize=(10,7), sharex=True, sharey=True)
axes[0].plot(years, HD_success[1], color = 'slategrey', alpha = 0.25, linewidth=7, label=r'Policy A ($\leq$1%)')
axes[0].plot(years, HD_success[2], color = 'slategrey', alpha=0.5, linewidth=5, label=r'Policy B ($\leq$2%)')
axes[0].plot(years, HD_success[3], color = 'slategrey', alpha=0.8, linewidth=3, label=r'Policy C ($\leq$3%)')
axes[0].plot(years, HD_success[4], color = 'slategrey', linewidth=1, label=r'Policy D ($\leq$4%)')
axes[0].plot(years, HD_successful_supply_reliability, color = 'black', linestyle = 'dashed', linewidth=1, label='Supply Reliability\nof Demand Grouping')
# axes[1].plot(years, MD_success[1], color = 'slategrey', alpha = 0.25, linewidth=7)
# axes[1].plot(years, MD_success[2], color = 'slategrey', alpha=0.5, linewidth=5)
axes[1].plot(years, MD_success[3], color = 'slategrey', alpha=0.8, linewidth=3)
# axes[1].plot(years, MD_success[4], color = 'slategrey', linewidth=1)
axes[1].plot(years, MD_successful_supply_reliability, color = 'black', linestyle = 'dashed', linewidth=1)
axes[2].plot(years, LD_success[1], color = 'slategrey', alpha = 0.25, linewidth=7)
axes[2].plot(years, LD_success[2], color = 'slategrey', alpha=0.5, linewidth=5)
axes[2].plot(years, LD_success[3], color = 'slategrey', alpha=0.8, linewidth=3)
axes[2].plot(years, LD_success[4], color = 'slategrey', linewidth=2)
axes[2].plot(years, LD_successful_supply_reliability, color = 'black', linestyle = 'dashed', linewidth=1)
axes[0].set_ylim(0,110)
#axes[0].grid(True)
axes[1].set_ylim(0,110)
#axes[1].grid(True)
axes[2].set_ylim(0,110)
#axes[2].grid(True)
axes[2].set_xticks(years)
axes[2].set_xticklabels([str(x) for x in range(2021, 2041)], rotation=90)
fig.text(0.06, 0.5, 'Percent of Realizations Meeting All Performance Goals', ha='center', va='center', rotation='90', fontsize=14)
fig.text(0.5, 0.035, 'Fiscal Year', ha='center', va='center', fontsize=14)
fig.text(.97, 0.75, 'High Demands', ha='center', va='center', fontsize=12, color='forestgreen')
fig.text(.98, 0.5, 'Medium Demands', ha='center', va='center', fontsize=12, color='purple')
fig.text(.97, 0.25, 'Low Demands', ha='center', va='center', fontsize=12, color='tomato') 
axes[0].legend(loc=(.77, 0.38), fontsize=7.5)
plt.subplots_adjust(hspace=0.07)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig9_Change_in_allgoals_MD_C.png', bbox_inches= 'tight', dpi=900)

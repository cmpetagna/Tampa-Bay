# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 20:52:59 2023
This is a retired figure - did not end up in final thesis/manuscript
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

#This was me looking at how different realization demand groupings impacted the results
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/demands_3grp_quant.csv', index_col=0)
#realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_avg_growthrate.csv', index_col=0)
#realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)
#realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandmax.csv', index_col=0)

simulation_list = [1]

#Organizing the rate covenant and debt covenants of the realizations into their demand groupings
for sim in simulation_list:
    DC = pd.read_csv('D:/Modeloutput/DC_f162_s' + str(sim) + '.csv', index_col=0)
    RC = pd.read_csv('D:/Modeloutput/RC_f162_s' + str(sim) + '.csv', index_col=0)
    UR = pd.read_csv('D:/Modeloutput/UR_f162_s' + str(sim) + '.csv', index_col=0)
    UR = UR.iloc[:, 2:]
    UR_pctchange = UR.pct_change(axis=1)

low_demand_DC, med_demand_DC, high_demand_DC = hf.realization_3groups(DC, realization_groupings)
low_demand_RC, med_demand_RC, high_demand_RC = hf.realization_3groups(RC, realization_groupings)

#percent of realizations that meet the covenant threshold each year
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

years = [x for x in range(2021, 2041)]

# fig, axes = plt.subplots(3, 1, figsize=(10,7), sharex=True, sharey=True)
# #axes[0].plot(years, LD_success_DC, linestyle = 'dashed', color = 'tomato', linewidth=3)
# axes[0].plot(years, LD_success_RC, linestyle = 'dotted', color = 'tomato', linewidth=3)
# #axes[1].plot(years, MD_success_DC, linestyle = 'dashed', color = 'purple', linewidth=3)
# axes[1].plot(years, MD_success_RC, linestyle = 'dotted', color = 'purple', linewidth=3)
# #axes[2].plot(years, HD_success_DC, linestyle = 'dashed', color = 'forestgreen', linewidth=3)
# axes[2].plot(years, HD_success_RC, linestyle = 'dotted', color = 'forestgreen', linewidth=3)
# axes[0].set_ylim(0,110)
# #axes[0].grid(True)
# axes[1].set_ylim(0,110)
# #axes[1].grid(True)
# axes[2].set_ylim(0,110)
# #axes[2].grid(True)
# axes[2].set_xticks(years)
# axes[2].set_xticklabels([str(x) for x in range(2021, 2041)], rotation=90)

fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True, sharey=True)
axs[0].boxplot(low_demand_DC, positions=years)
axs[0].plot(years, ([1] * len(years)), color='red')
axs0 = axs[0].twinx()
axs0.plot(years, LD_success_DC, linestyle = 'dotted', color = 'tomato', linewidth=3)
axs[1].boxplot(med_demand_DC, positions=years)
axs[1].plot(years, ([1] * len(years)), color='red')
axs1 = axs[1].twinx()
axs1.plot(years, MD_success_DC, linestyle = 'dotted', color = 'purple', linewidth=3)
axs[2].boxplot(high_demand_DC, positions=years)
axs[2].plot(years, ([1] * len(years)), color='red')
axs2 = axs[2].twinx()
axs2.plot(years, HD_success_DC, linestyle = 'dotted', color = 'forestgreen', linewidth=3)
#fig.text(0.02, 0.5, 'Debt Covenant', va='center', rotation='vertical')
#fig.text(0.98, 0.5, 'Covenant Success Rate (%)', va='center', rotation='vertical')
plt.subplots_adjust(hspace=0)
plt.tight_layout()

fig2, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True, sharey=True)
axs[0].boxplot(low_demand_RC, positions=years)
axs[0].plot(years, ([1.25] * len(years)), color='red')
axs0 = axs[0].twinx()
axs0.plot(years, LD_success_RC, linestyle = 'dashed', color = 'tomato', linewidth=3)
axs[1].boxplot(med_demand_RC, positions=years)
axs[1].plot(years, ([1.25] * len(years)), color='red')
axs1 = axs[1].twinx()
axs1.plot(years, MD_success_RC, linestyle = 'dashed', color = 'purple', linewidth=3)
axs[2].boxplot(high_demand_RC, positions=years)
axs[2].plot(years, ([1.25] * len(years)), color='red')
axs2 = axs[2].twinx()
axs2.plot(years, HD_success_RC, linestyle = 'dashed', color = 'forestgreen', linewidth=3)
#fig2.text(0.02, 0.5, 'Debt Covenant', va='center', rotation='vertical')
#fig2.text(0.98, 0.5, 'Covenant Success Rate (%)', va='center', rotation='vertical')
plt.subplots_adjust(hspace=0)
plt.tight_layout()

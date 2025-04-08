# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:42:15 2023
supply pie chart success
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


#slack variable file
failure_durations = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/Reliability/Runs_162_160/Severity/failure_durations_30_day_run162.csv', header=None)
#The three "demand" grouings of the realizations
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)

low_demands_reliability, med_demands_reliability, high_demands_reliability = hf.realization_3groups(failure_durations, realization_groupings)

#number of realizations in a year that do not have a supply shortfall
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

#supply pie chart figure
years = [x for x in range(2021, 2041)]
fig2, axes = plt.subplots(3, 21)
colors = ['dimgrey', 'red']
whitecolors = ['white', 'white']
axes[0, 20].pie([100, 0], colors=whitecolors)
axes[1,20].pie([100, 0], colors=whitecolors)
axes[2, 20].pie([100, 0], colors=whitecolors)
axes[0, 20].text(0.5, 0.5, 'High Demands', ha='left', va='center', fontsize=8, color='forestgreen')
axes[1,20].text(0.5, 0.5, 'Medium Demands', ha='left', va='center', fontsize=8, color='purple')
axes[2, 20].text(0.5, 0.5, 'Low Demands', ha='left', va='center', fontsize=9, color='tomato')
for year in range(0, 20):
    axes[0, year].pie([HD_successful_supply_reliability[year], (100-HD_successful_supply_reliability[year])], colors=colors, radius=1.3)
    axes[1, year].pie([MD_successful_supply_reliability[year], (100-MD_successful_supply_reliability[year])], colors=colors, radius=1.3)
    axes[2, year].pie([LD_successful_supply_reliability[year], (100-LD_successful_supply_reliability[year])], colors=colors, radius=1.3)
for i, year in enumerate(years[:20]):
    axes[2, i].set_xlabel(str(year), rotation=90)
arrow_props = dict(arrowstyle='->', color='black')
plt.annotate('Supply Projects\nAdded to System', xy=(0.28, 0.65), xycoords='figure fraction',
             xytext=(0.42, 0.75), textcoords='figure fraction',
             ha='center', arrowprops=arrow_props)
plt.subplots_adjust(hspace=-0.8)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig6_supply_reliability.png', bbox_inches= 'tight', dpi=900)

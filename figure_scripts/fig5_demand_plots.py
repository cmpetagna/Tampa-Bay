# -*- coding: utf-8 -*-
"""
Created on Thu May 11 07:09:59 2023

@author: cmpet
"""

import numpy as np
import pandas as pd
#import financial_metrics_reliabilty_plots as fm
import helper_functions as hf
import demand_buckets as db
import matplotlib.pyplot as plt
import seaborn as sns
#import financial_plots_by_demand as demandplt
#sns.set()

# demand_3groups_histo = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/demands_3grp_histo.csv', index_col=0)
# demand_3groups_quant = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/demands_3grp_quant.csv', index_col=0)

#demand_3groups = demand_3groups.add(1)
demands = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/demand_analysis/annual_avg_demands_WY.csv', index_col=0)
demands = demands.iloc[:-1,:].T
demands = demands.reset_index()
demands = demands.iloc[:, 1:]

##Evaluating the realizations based on their overall percent change
demands_pct_change = demands.pct_change(axis=1)
demands_pct_change['average'] = demands_pct_change.mean(axis=1)
first_cutoff = np.quantile(demands_pct_change['average'], 0.3333)
second_cutoff = np.quantile(demands_pct_change['average'], 0.6666)
demand_growth_groups = db.buckets_3(demands_pct_change['average'], first_cutoff, second_cutoff)

##Evaluating the realizations based on the difference between the first year and the second year:
demand_group_analysis = demands[[2021, 2040]].copy()
demand_group_analysis['first_last_difference'] = demand_group_analysis[2040] - demand_group_analysis[2021]
demand_group_analysis['growth_rate_average'] = pd.Series(demands_pct_change['average'])
demand_group_analysis['max_demand'] = demands.max(axis=1)
demand_group_analysis['percent_difference'] = demand_group_analysis['first_last_difference'] / demand_group_analysis[2021]
demand_group_analysis['average_demand'] = demands.mean(axis=1)
first_third2021 = np.quantile(demand_group_analysis[2021], 0.3333)
second_third2021 = np.quantile(demand_group_analysis[2021], 0.6666)
first_third2040 = np.quantile(demand_group_analysis[2040], 0.3333)
second_third2040 = np.quantile(demand_group_analysis[2040], 0.6666)
first_third_difference = np.quantile(demand_group_analysis['first_last_difference'], 0.3333)
second_third_difference = np.quantile(demand_group_analysis['first_last_difference'], 0.6666)
first_third_growth = np.quantile(demand_group_analysis['growth_rate_average'], 0.3333)
second_third_growth = np.quantile(demand_group_analysis['growth_rate_average'], 0.6666)
first_third_max = np.quantile(demand_group_analysis['max_demand'], 0.3333)
second_third_max = np.quantile(demand_group_analysis['max_demand'], 0.6666)
first_third_pctchange = np.quantile(demand_group_analysis['percent_difference'], 0.3333)
second_third_pctchange = np.quantile(demand_group_analysis['percent_difference'], 0.6666)
first_third_avg = np.quantile(demand_group_analysis['average_demand'], 0.3333)
second_third_avg = np.quantile(demand_group_analysis['average_demand'], 0.6666)
demand_growth_groups = db.buckets_3(demand_group_analysis['average_demand'], first_third_avg, second_third_avg)
##Just breaking the demands up by the difference between the first and last 



low_demands, med_demands, high_demands = hf.realization_3groups(demands, demand_growth_groups)

low_demand_metrics = hf.group_metrics(low_demands)
med_demand_metrics = hf.group_metrics(med_demands)
high_demand_metrics = hf.group_metrics(high_demands)

low_demand_metrics = np.asarray(low_demand_metrics, dtype=float)
med_demand_metrics = np.asarray(med_demand_metrics, dtype=float)
high_demand_metrics = np.asarray(high_demand_metrics, dtype=float)
max_LD=low_demand_metrics[3]
min_LD=low_demand_metrics[2]
min_LD.dtype


demands_array = demands.to_numpy()

fig, ax = plt.subplots(figsize=(15,10))
for i in range(len(low_demands.iloc[:, 0])):
    ax.plot(demands.columns, low_demands.iloc[i, :], c='tomato', )
#To add a legend plot just one realization and label - do this for high and medium demands
ax.plot([], [], c='tomato', label= 'Low Demands')
for i in range(len(high_demands.iloc[:, 0])):
    ax.plot(demands.columns, high_demands.iloc[i, :], c='forestgreen')
ax.plot([], [], c='forestgreen', label= 'High Demands')
for i in range(len(med_demands.iloc[:, 0])):
    ax.plot(demands.columns, med_demands.iloc[i, :], c='purple')
ax.plot([], [], c='purple', label= 'Medium Demands')
handles, labels = plt.gca().get_legend_handles_labels()
order = [1, 2, 0]
plt.legend([handles[i] for i in order], [labels[i] for i in order], fontsize=18)    
#ax.legend(loc = (0.075,0.85), fontsize=20)
ax.set_xlabel('Fiscal Year', fontsize=24, weight='bold')
ax.set_ylabel('Water Demand (MGD)', fontsize=24, weight='bold')
pad = 25
ax.xaxis.labelpad = pad
ax.yaxis.labelpad = pad
ax.set_xlim([2021, 2040])
ax.set_ylim([160, 250])
ax.set_xticks([2021, 2025, 2030, 2035, 2040])
ax.set_xticklabels([2021, 2025, 2030, 2035, 2040], fontsize=20)
ax.set_yticklabels([''] + [170, 180, 190, 200, 210, 220, 230, 240] + [''], fontsize=20)
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig5_demandgropuings.png', bbox_inches= 'tight', dpi=900)


##This version of the demands figure shades between the min/max of each gropuing.

# years = [float(x) for x in range(2021,2041)]
# fig, ax = plt.subplots(figsize=(20,15))
# # for i in range(len(demands_array[:, 0])):
# #     ax.plot(demands.columns, demands_array[i, :], c='lightgrey')
# ax.plot(years, low_demand_metrics[1], color = 'tomato', linewidth=6, linestyle= ':')
# ax.fill_between(years, low_demand_metrics[3], low_demand_metrics[2], color = 'tomato', linewidth=2, alpha=0.4, edgecolor = 'tomato')
# #ax.plot(demands.columns, low_demand_metrics[3], color = 'tomato', linewidth=6)
# ax.plot(years, med_demand_metrics[1], color = 'purple', linewidth=6, linestyle= ':')
# ax.fill_between(years, med_demand_metrics[3], med_demand_metrics[2], color = 'purple', linewidth=2, alpha=0.4, edgecolor = 'purple')
# #ax.plot(demands.columns, med_demand_metrics[3], color = 'darkorange', linewidth=6)
# ax.plot(demands.columns, high_demand_metrics[1], color = 'forestgreen', linewidth=6, linestyle= ':')
# ax.fill_between(years, high_demand_metrics[3], high_demand_metrics[2], color = 'forestgreen', linewidth=2, alpha=0.4, edgecolor = 'forestgreen')
# #ax.plot(demands.columns, high_demand_metrics[3], color = 'forestgreen', linewidth=6)
# ax.set_xticks([str(x) for x in range(2021, 2041, 1)])
# ax.set_xticklabels([str(x) for x in range(2021, 2041, 1)], rotation = 90, fontsize = 20)



##Below is old work I didn't want to delete (Just in case) It also creates different tables if needed.

# ##Experimenting with new grouping:
# low_demand_conditions = demand_group_analysis[2021] <= first_third2021
# low_demand_conditions2 = (demand_group_analysis[2021] > first_third2021) & (demand_group_analysis[2021] <= second_third2021) & (demand_group_analysis['growth_rate_average'] <= first_third_growth)
# med_demand_conditions = (demand_group_analysis[2021] > first_third2021) & (demand_group_analysis[2021] <= second_third2021)
# #med_demand_conditions2 = (demand_group_analysis[2040] > first_third2040) & (demand_group_analysis[2040] <= second_third2040)
# high_demand_conditions = demand_group_analysis[2021] > second_third2021
# high_demand_conditions2 = (demand_group_analysis[2021] > first_third2021) & (demand_group_analysis[2021] <= second_third2021) & (demand_group_analysis['growth_rate_average'] > second_third_growth)

# # low_demands = demand_group_analysis[low_demand_conditions & low_demand_conditions2].index.tolist()
# # med_demands = demand_group_analysis[med_demand_conditions & med_demand_conditions2].index.tolist()
# # high_demands = demand_group_analysis[high_demand_conditions & high_demand_conditions2].index.tolist()
# # demand_groupings = pd.concat([pd.Series(low_demands), pd.Series(med_demands), pd.Series(high_demands)], axis=1)

##Create tables of the demand groupings:
# demand_growth_groups_growthrate = db.buckets_3(demand_group_analysis['growth_rate_average'], first_third_growth, second_third_growth)
# demand_growth_groups_growthrate.to_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_avg_growthrate.csv')
# demand_growth_groups_demandaverage = db.buckets_3(demand_group_analysis['average_demand'], first_third_avg, second_third_avg)
# demand_growth_groups_demandaverage.to_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv')
# demand_growth_groups_demandmax = db.buckets_3(demand_group_analysis['max_demand'], first_third_max, second_third_max)
# demand_growth_groups_demandmax.to_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandmax.csv')


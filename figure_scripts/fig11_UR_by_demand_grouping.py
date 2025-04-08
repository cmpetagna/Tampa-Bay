# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:11:44 2023
Compares the range of the uniform rate against the various realization groupings.
@author: cmpet
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as hf
data_path = 'D:/Modeloutput'

# plot data across simulations/evaluations and all realizations
realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/demands_3grp_quant.csv', index_col=0)

low_demand_UR ={}
med_demand_UR ={}
high_demand_UR ={}
for run_id in [162]:
    for sim in [1, 2, 3, 4]:
        # read data
        ur_data = pd.read_csv(data_path + '/UR_f' + str(run_id) + '_s' + str(sim) + '.csv', index_col = 0)
        ur_data = ur_data.iloc[:,2:]
        low_demand_UR[sim], med_demand_UR[sim], high_demand_UR[sim] = hf.realization_3groups(ur_data, realization_groupings)
        
        # trim to start/end on same years
        min_year = np.max([float(min(ur_data.columns))])
        max_year = np.min([float(max(ur_data.columns))])
        
        col_range = [str(x) for x in range(int(min_year),int(max_year+1))]
        ur_data = ur_data[col_range]
                
        # make plot
fig, ax = plt.subplots(1,4, figsize = (20,7), sharey=True)
ax[0].fill_between(ur_data.columns,
                       np.max(high_demand_UR[1], axis = 0), 
                       np.min(high_demand_UR[1], axis = 0), 
                       color = 'forestgreen', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'forestgreen',
                       label='High Demands')
ax[0].fill_between(ur_data.columns,
                       np.max(med_demand_UR[1], axis = 0), 
                       np.min(med_demand_UR[1], axis = 0), 
                       color = 'purple', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'purple',
                       label='Medium Demands')
ax[0].fill_between(ur_data.columns,
                       np.max(low_demand_UR[1], axis = 0), 
                       np.min(low_demand_UR[1], axis = 0), 
                       color = 'tomato', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'tomato',
                       label='Low Demands')
ax[1].fill_between(ur_data.columns,
                       np.max(high_demand_UR[2], axis = 0), 
                       np.min(high_demand_UR[2], axis = 0), 
                       color = 'forestgreen', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'forestgreen',
                       label='High Demands')
ax[1].fill_between(ur_data.columns,
                       np.max(med_demand_UR[2], axis = 0), 
                       np.min(med_demand_UR[2], axis = 0), 
                       color = 'purple', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'purple',
                       label='Medium Demands')
ax[1].fill_between(ur_data.columns,
                       np.max(low_demand_UR[2], axis = 0), 
                       np.min(low_demand_UR[2], axis = 0), 
                       color = 'tomato', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'tomato',
                       label='Low Demands')
ax[2].fill_between(ur_data.columns,
                       np.max(high_demand_UR[3], axis = 0), 
                       np.min(high_demand_UR[3], axis = 0), 
                       color = 'forestgreen', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'forestgreen',
                       label='High Demands')
ax[2].fill_between(ur_data.columns,
                       np.max(med_demand_UR[3], axis = 0), 
                       np.min(med_demand_UR[3], axis = 0), 
                       color = 'purple', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'purple',
                       label='Medium Demands')
ax[2].fill_between(ur_data.columns,
                       np.max(low_demand_UR[3], axis = 0), 
                       np.min(low_demand_UR[3], axis = 0), 
                       color = 'tomato', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'tomato',
                       label='Low Demands')
ax[3].fill_between(ur_data.columns,
                       np.max(high_demand_UR[4], axis = 0), 
                       np.min(high_demand_UR[4], axis = 0), 
                       color = 'forestgreen', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'forestgreen',
                       label='High Demands')
ax[3].fill_between(ur_data.columns,
                       np.max(med_demand_UR[4], axis = 0), 
                       np.min(med_demand_UR[4], axis = 0), 
                       color = 'purple', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'purple',
                       label='Medium Demands')
ax[3].fill_between(ur_data.columns,
                       np.max(low_demand_UR[4], axis = 0), 
                       np.min(low_demand_UR[4], axis = 0), 
                       color = 'tomato', 
                       alpha = 0.4,  linewidth = 2,
                       edgecolor = 'tomato',
                       label='Low Demands')
        
ax[0].set_ylim((2.5,4.5))
                
ax[0].set_xticks(['2021', '2025', '2030', '2035', '2040'])
ax[0].set_xticklabels(['2021', '2025', '2030', '2035', '2040'], fontsize=16.5)
ax[1].set_xticks(['2021', '2025', '2030', '2035', '2040'])
ax[1].set_xticklabels(['2021', '2025', '2030', '2035', '2040'], fontsize=16.5)
ax[2].set_xticks(['2021', '2025', '2030', '2035', '2040'])
ax[2].set_xticklabels(['2021', '2025', '2030', '2035', '2040'], fontsize=16.5)
ax[3].set_xticks(['2021', '2025', '2030', '2035', '2040'])
ax[3].set_xticklabels(['2021', '2025', '2030', '2035', '2040'], fontsize=16.5)
ax[0].tick_params(axis='y', labelsize=18)
fig.text(0.5, 0.05, 'Fiscal Year', ha='center', va='center',fontsize=24)
fig.text(0.07, 0.5,'$/kgal', ha='center', va='center', rotation='90', fontsize=24)
fig.text(.2, .9, 'Policy A (1%)', ha='center', va='center', fontsize = 22)
fig.text(.4, .9, 'Policy B (2%)', ha='center', va='center', fontsize = 22)
fig.text(.6, .9, 'Policy C (3%)', ha='center', va='center', fontsize = 22)
fig.text(.8, .9, 'Policy D (4%)', ha='center', va='center', fontsize = 22)
ax[0].legend(loc = (0.1,0.7), fontsize=14)
plt.subplots_adjust(wspace=0.1)

plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig11_differences_in_UR_2panel_3per.png', bbox_inches= 'tight', dpi = 900)
        

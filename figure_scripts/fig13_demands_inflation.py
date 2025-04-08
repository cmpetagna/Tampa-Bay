# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:33:13 2023
Plots the average annual percent change of the uniform rate against the inflation rate
@author: cmpet
"""

import numpy as np
import pandas as pd
#import financial_metrics_reliabilty_plots as fm
import helper_functions as hf
import demand_buckets as db
import matplotlib.pyplot as plt


UR_SOW2 = pd.read_csv('D:/Modeloutput/UR_f162_s15.csv', index_col=0)
UR_SOW3 = pd.read_csv('D:/Modeloutput/UR_f162_s17.csv', index_col=0)
UR_SOW4 = pd.read_csv('D:/Modeloutput/UR_f162_s16.csv', index_col=0)

UR_SOW2 = UR_SOW2.iloc[:, 2:]
UR_SOW3 = UR_SOW3.iloc[:, 2:]
UR_SOW4 = UR_SOW4.iloc[:, 2:]

UR_SOW2_pc = UR_SOW2.pct_change(axis=1)
UR_SOW3_pc = UR_SOW3.pct_change(axis=1)
UR_SOW4_pc = UR_SOW4.pct_change(axis=1)

UR_SOW2_pc['mean'] = UR_SOW2_pc.mean(axis=1)
UR_SOW3_pc['mean'] = UR_SOW3_pc.mean(axis=1)
UR_SOW4_pc['mean'] = UR_SOW4_pc.mean(axis=1)

UR_SOW2_pc.loc['annual mean'] = UR_SOW2_pc.mean()
UR_SOW3_pc.loc['annual mean'] = UR_SOW3_pc.mean()
UR_SOW4_pc.loc['annual mean'] = UR_SOW4_pc.mean()

UR_SOW2_10yearavg = UR_SOW2_pc.iloc[-1,:11].mean()
UR_SOW3_10yearavg = UR_SOW3_pc.iloc[-1,:11].mean()
UR_SOW4_10yearavg = UR_SOW4_pc.iloc[-1,:11].mean()

UR_SOW2_plot = list(UR_SOW2_pc.iloc[-1,1:-1])
UR_SOW3_plot = list(UR_SOW3_pc.iloc[-1,1:-1])
UR_SOW4_plot = list(UR_SOW4_pc.iloc[-1,1:-1])

UR_SOW3_r = pd.read_csv('D:/Modeloutput/UR_f162_s20.csv', index_col=0)
UR_SOW4_r = pd.read_csv('D:/Modeloutput/UR_f162_s19.csv', index_col=0)

UR_SOW3_r = UR_SOW3_r.iloc[:, 2:]
UR_SOW4_r = UR_SOW4_r.iloc[:, 2:]

UR_SOW3_pc_r = UR_SOW3_r.pct_change(axis=1)
UR_SOW4_pc_r = UR_SOW4_r.pct_change(axis=1)

UR_SOW3_pc_r['mean'] = UR_SOW3_pc_r.mean(axis=1)
UR_SOW4_pc_r['mean'] = UR_SOW4_pc_r.mean(axis=1)

UR_SOW3_pc_r.loc['annual mean'] = UR_SOW3_pc_r.mean()
UR_SOW4_pc_r.loc['annual mean'] = UR_SOW4_pc_r.mean()

UR_SOW3_plot_r = list(UR_SOW3_pc_r.iloc[-1,1:-1])
UR_SOW4_plot_r = list(UR_SOW4_pc_r.iloc[-1,1:-1])

inflation = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Code/TampaBayWater/FinancialModeling/inflation_scenarios.csv', header=None)

SOW234_inflation = inflation.iloc[-1,:-1]
inflation_years = [x for x in range(2022, 2041)]

fig, ax = plt.subplots(figsize=(13,7))
#ax.plot(inflation_years, UR_SOW2_plot, color='aqua', linewidth=4, label='SOW Group 2 Uniform Rate Change')
ax.plot(inflation_years, UR_SOW3_plot, color='aqua', linewidth=3, label='Scenario 2 - no rate cap')
ax.plot(inflation_years, UR_SOW4_plot, color='dodgerblue', linewidth=2, label='Scenario 3 - no rate cap')
ax.plot(inflation_years, UR_SOW3_plot_r, color='aqua', linewidth=3, linestyle = 'dotted', label='Scenario 2 - 5.5% rate cap')
ax.plot(inflation_years, UR_SOW4_plot_r, color='dodgerblue', linewidth=2, linestyle = 'dotted', label='Scenario 3 - 6.5% rate cap')
ax2 = ax.twinx()
ax2.plot(inflation_years, SOW234_inflation, color = 'firebrick', linewidth=2.5, label='Inflation Rate')
ax.set_xticks(inflation_years)
ax.set_xticklabels(inflation_years, rotation=90, fontsize=18)
ax.tick_params(axis='y', labelsize=14)
ax.set_yticks((-0.05, 0, 0.05, 0.1, 0.15, 0.20, 0.25))
ax.set_yticklabels([-5, 0, 5, 10, 15, 20, 25], fontsize=18)
ax2.set_yticks((-0.05, 0, 0.05, 0.1, 0.15, 0.20, 0.25))
ax2.set_yticklabels([-5, 0, 5, 10, 15, 20, 25], fontsize=18)
ax.legend(loc=(0.6, .75), fontsize=14, frameon=False)
ax2.legend(loc=(0.6, .68), fontsize=14, frameon=False)
ax.set_xlabel('Fiscal Year', fontsize =18, weight='bold')
ax.set_ylabel('Average Annual % Change of Volumetric Rate', fontsize=18, weight='bold')
fig.text(0.94, 0.25, 'Annual Rate of Inflation', fontsize=18, weight='bold', rotation='270')
#ax2.set_position([ax.get_position().x0, ax.get_position().y0,
#                  ax.get_position().width, ax.get_position().height])
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/thesis/thesis_figures/fig13_URchange_inflation.png', bbox_inches= 'tight', dpi=900)


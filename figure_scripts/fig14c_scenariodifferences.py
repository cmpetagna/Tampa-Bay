# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:40:42 2023
Displays the difference in Uniform Rate for high inflation/interest rate scenarios
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

scenarios = [4, 19, 20, 21, 22]

LD_UR_chng={}
MD_UR_chng={}
HD_UR_chng={}


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
    
    #UR_changes = UR.pct_change(axis=1)
    UR_filter = UR[combined_conditions]
    
    LD_UR_chng[s], MD_UR_chng[s], HD_UR_chng[s] = hf.realization_3groups(UR_filter, realization_groupings)
    
count = UR_filter.isna().sum()
UR_filter.loc['success_rate'] = 1 - (count/len(UR_filter))

def assessment(dictionary):
    annual_avg={}
    success_rate={}
    for key, df in dictionary.items():
        annual_avg[key] = df.mean()
        count = df.isna().sum()
        success_rate[key] = 1 - (count/(len(df)))
    return annual_avg, success_rate

LD_avg, LD_success = assessment(LD_UR_chng)
MD_avg, MD_success = assessment(MD_UR_chng)
HD_avg, HD_success = assessment(HD_UR_chng)

##difference between the 4%s
LD4_S2_avg = LD_avg[22] - LD_avg[4]
LD4_S3_avg = LD_avg[21] - LD_avg[4]
LD4_success_S2 = LD_success[22] - LD_success[4]
LD4_success_S3 = LD_success[21] - LD_success[4]
MD4_S2_avg = MD_avg[22] - MD_avg[4]
MD4_S3_avg = MD_avg[21] - MD_avg[4]
MD4_success_S2 = MD_success[22] - MD_success[4]
MD4_success_S3 = MD_success[21] - MD_success[4]
HD4_S2_avg = HD_avg[22] - HD_avg[4]
HD4_S3_avg = HD_avg[21] - HD_avg[4]
HD4_success_S2 = HD_success[22] - HD_success[4]
HD4_success_S3 = HD_success[21] - HD_success[4]

years = [x for x in range(2026,2037)]


##difference between 4% and the higher amounts
LD5_S2_avg = LD_avg[20] - LD_avg[4]
LD6_S3_avg = LD_avg[19] - LD_avg[4]
LD5_success_S2 = LD_success[20] - LD_success[4]
LD6_success_S3 = LD_success[19] - LD_success[4]
MD5_S2_avg = MD_avg[20] - MD_avg[4]
MD6_S3_avg = MD_avg[19] - MD_avg[4]
MD5_success_S2 = MD_success[20] - MD_success[4]
MD6_success_S3 = MD_success[19] - MD_success[4]
HD5_S2_avg = HD_avg[20] - HD_avg[4]
HD6_S3_avg = HD_avg[19] - HD_avg[4]
HD5_success_S2 = HD_success[20] - HD_success[4]
HD6_success_S3 = HD_success[19] - HD_success[4]


S2_rateOFsuccess4 = pd.DataFrame({'Years':years, 'HD4':HD4_success_S2[5:16], 'MD4':MD4_success_S2[5:16], 'LD4':LD4_success_S2[5:16]})
S2_rateOFsuccess = pd.DataFrame({'Years':years, 'HD5':HD5_success_S2[5:16], 'MD5':MD5_success_S2[5:16], 'LD5':LD5_success_S2[5:16]})
S2_dfs = [S2_rateOFsuccess4, S2_rateOFsuccess]
S3_rateOFsuccess4 = pd.DataFrame({'Years':years, 'HD4':HD4_success_S3[5:16], 'MD4':MD4_success_S3[5:16], 'LD4':LD4_success_S3[5:16]})
S3_rateOFsuccess = pd.DataFrame({'Years':years, 'HD6':HD6_success_S3[5:16], 'MD6':MD6_success_S3[5:16], 'LD6':LD6_success_S3[5:16]})
S3_dfs = [S3_rateOFsuccess4, S3_rateOFsuccess]

S2_rates4 = pd.DataFrame({'Years':years, 'HD4':HD4_S2_avg[5:16], 'MD4':MD4_S2_avg[5:16], 'LD4':LD4_S2_avg[5:16]})
S2_rates = pd.DataFrame({'Years':years, 'HD5':HD5_S2_avg[5:16], 'MD5':MD5_S2_avg[5:16], 'LD5':LD5_S2_avg[5:16]})
S3_rates4 = pd.DataFrame({'Years':years, 'HD4':HD4_S3_avg[5:16], 'MD4':MD4_S3_avg[5:16], 'LD4':LD4_S3_avg[5:16]})
S3_rates = pd.DataFrame({'Years':years, 'HD6':HD6_S3_avg[5:16], 'MD6':MD6_S3_avg[5:16], 'LD6':LD6_S3_avg[5:16]})
S2p_dfs = [S2_rates4, S2_rates]
S3p_dfs = [S3_rates4, S3_rates]

bar_width= 0.35
x = S2_rateOFsuccess4['Years']

fig, axes = plt.subplots(3, 2, figsize=(25,20), sharey=True, sharex=True)
##Plots
for i in range(3):
    for j in range (2):
        ax = axes[i, j]
        ax.bar((x - bar_width/2), S2_dfs[j].iloc[:,(i+1)], bar_width, color = 'aqua', label='Scenario 2 Rate of Success Difference')
        ax.bar((x + bar_width/2), S3_dfs[j].iloc[:,(i+1)], bar_width, color = 'dodgerblue', label='Scenario 3 Rate of Success Difference')
        ax.set_ylim(-1, 1.25)
        ax2 = ax.twinx()
        ax2.plot(x, S2p_dfs[j].iloc[:,(i+1)], color = 'aqua', linewidth = 3, linestyle = 'dashed', label='Scenario 2 Volumetric Rate Difference')
        ax2.plot(x, S3p_dfs[j].iloc[:,(i+1)], color = 'dodgerblue', linewidth = 3, linestyle = 'dashed', label='Scenario 3 Volumetric Rate Difference')
        ax2.set_ylim(-1,1.25)
        if j == 1:
            ax2.tick_params(axis='y', labelsize=24)
        else:
            ax2.set_yticks([])
        if i == 0 and j == 0:
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc=(.03, 0.67), fontsize = 18, frameon=False)
axes[2,0].set_xticks(years)
axes[2,1].set_xticks(years)
axes[2,0].tick_params(axis='x', labelsize=24, rotation=90)
axes[2,1].tick_params(axis='x', labelsize=24, rotation=90)
axes[0,0].tick_params(axis='y', labelsize=24)
axes[1,0].tick_params(axis='y', labelsize=24)
axes[2,0].tick_params(axis='y', labelsize=24)
#axes[0,0].legend(loc=(.1, 0.67), fontsize=18, frameon=False)

plt.subplots_adjust(hspace=0.05, wspace=0.02)
fig.text(0.06,0.5, 'Difference in Success Rate of Meeting All Performance Goals (%)\nfrom Scenario 1 - Policy D', ha='center', va='center', rotation='90',fontsize=28, weight='bold')
fig.text(0.95,0.5, 'Difference in Volumetric Rate ($) from Scenario 1 - Policy D', ha='center', va='center', rotation='270',fontsize=28, weight='bold')
fig.text(0.3,0.9, '$\leq$4%' + ' Annual Increase\nApplied to Scenarios 2 & 3', ha='center', va='center', fontsize=24, weight='bold')
fig.text(0.7,0.9, '$\leq$5.5%' + ' Annual Increase Applied to Scenario 2\nand' + '$\leq$6.5%' + ' Annual Increase Applied to Scenario 3', ha='center', va='center', fontsize=24, weight='bold')
fig.text(0.5,0.05, 'Fiscal Years', ha='center', va='center', fontsize=28, weight='bold')
fig.text(1, 0.25, 'Low\nDemands', ha='center', va='center', fontsize=28, color='tomato')
fig.text(1, 0.5, 'Medium\nDemands', ha='center', va='center', fontsize=28, color='purple')
fig.text(1, 0.75, 'High\nDemands', ha='center', va='center', fontsize=28, color='forestgreen')
plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig15_macroecon_results.png', bbox_inches= 'tight', dpi=500)


# #axes2[0,0] = axes[0,0].twinx()
# axes[0,0].plot(years, HD_4difference_price['Scenario 2 Avgerage Rate difference'],  color = 'aqua', linewidth = 3, linestyle = 'dashed', label='Scenario 2 Price')
# axes[0,0].plot(years, HD_4difference_price['Scenario 3 Avgerage Rate difference'],  color ='dodgerblue', linewidth = 3, linestyle = 'dashed', label='Scenario 3 Price')
# axes[1,0].plot(years, MD_4difference_price['Scenario 2 Avgerage Rate difference'], color = 'aqua', linewidth = 3, linestyle = 'dashed')
# axes[1,0].plot(years, MD_4difference_price['Scenario 3 Avgerage Rate difference'], color ='dodgerblue', linewidth = 3, linestyle = 'dashed')
# axes[2,0].plot(years, LD_4difference_price['Scenario 2 Avgerage Rate difference'], color = 'aqua', linewidth = 3, linestyle = 'dashed')
# axes[2,0].plot(years, LD_4difference_price['Scenario 3 Avgerage Rate difference'], color ='dodgerblue', linewidth = 3, linestyle = 'dashed')
# axes[0,1].plot(years, HD_difference_price['Scenario 2 Avgerage Rate difference'], color = 'aqua', linewidth = 3, linestyle = 'dashed')
# axes[0,1].plot(years, HD_difference_price['Scenario 3 Avgerage Rate difference'], color ='dodgerblue', linewidth = 3, linestyle = 'dashed')
# axes[1,1].plot(years, MD_difference_price['Scenario 2 Avgerage Rate difference'], color = 'aqua', linewidth = 3, linestyle = 'dashed')
# axes[1,1].plot(years, MD_difference_price['Scenario 3 Avgerage Rate difference'], color ='dodgerblue', linewidth = 3, linestyle = 'dashed')
# axes[2,1].plot(years, LD_difference_price['Scenario 2 Avgerage Rate difference'], color = 'aqua', linewidth = 3, linestyle = 'dashed')
# axes[2,1].plot(years, LD_difference_price['Scenario 3 Avgerage Rate difference'], color ='dodgerblue', linewidth = 3, linestyle = 'dashed')



# LD_4difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':LD4_success_S2[5:16], 'Scenario 3 Rate of Success Difference':LD4_success_S3[5:16]})
# LD_4difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':LD4_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':LD4_S3_avg[5:16]})
# MD_4difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':MD4_success_S2[5:16], 'Scenario 3 Rate of Success Difference':MD4_success_S3[5:16]})
# MD_4difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':MD4_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':MD4_S3_avg[5:16]})
# HD_4difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':HD4_success_S2[5:16], 'Scenario 3 Rate of Success Difference':HD4_success_S3[5:16]})
# HD_4difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':HD4_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':HD4_S3_avg[5:16]})

# LD_difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':LD5_success_S2[5:16], 'Scenario 3 Rate of Success Difference':LD6_success_S3[5:16]})
# LD_difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':LD5_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':LD6_S3_avg[5:16]})
# MD_difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':MD5_success_S2[5:16], 'Scenario 3 Rate of Success Difference':MD6_success_S3[5:16]})
# MD_difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':MD5_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':MD6_S3_avg[5:16]})
# HD_difference = pd.DataFrame({'Years':years, 'Scenario 2 Rate of Success Difference':HD5_success_S2[5:16], 'Scenario 3 Rate of Success Difference':HD6_success_S3[5:16]})
# HD_difference_price = pd.DataFrame({'Years':years, 'Scenario 2 Avgerage Rate difference':HD5_S2_avg[5:16], 'Scenario 3 Avgerage Rate difference':HD6_S3_avg[5:16]})

# axes[0,0].bar((x - bar_width/2), HD_4difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua', label='Scenario 2 Rate of Success')
# axes[0,0].bar((x + bar_width/2), HD_4difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue', label='Scenario 3 Rate of Success')
# axes[1,0].bar((x - bar_width/2), MD_4difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua')
# axes[1,0].bar((x + bar_width/2), MD_4difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue')
# axes[2,0].bar((x - bar_width/2), LD_4difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua')
# axes[2,0].bar((x + bar_width/2), LD_4difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue')
# axes[0,1].bar((x - bar_width/2), HD_difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua')
# axes[0,1].bar((x + bar_width/2), HD_difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue')
# axes[1,1].bar((x - bar_width/2), MD_difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua')
# axes[1,1].bar((x + bar_width/2), MD_difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue')
# axes[2,1].bar((x - bar_width/2), LD_difference['Scenario 2 Rate of Success Difference'], bar_width, color = 'aqua')
# axes[2,1].bar((x + bar_width/2), LD_difference['Scenario 3 Rate of Success Difference'], bar_width, color ='dodgerblue')
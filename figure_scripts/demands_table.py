# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 16:14:56 2023

@author: cmpet
"""


import pandas as pd
#import financial_metrics_reliabilty_plots as fm
import helper_functions as hf


UR_SOW1_P4 = pd.read_csv('D:/Modeloutput/UR_f162_s4.csv', index_col=0)

UR_SOW1_P4 = UR_SOW1_P4.iloc[:, 2:]

realization_groupings = pd.read_csv('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/Analysis/realization_groupings/thirds_demandavg.csv', index_col=0)

LD_URs, MD_URs, HD_URs = hf.realization_3groups(UR_SOW1_P4, realization_groupings)

HD_URs.loc['annual average'] = HD_URs.mean()
MD_URs.loc['annual average'] = MD_URs.mean()
LD_URs.loc['annual average'] = LD_URs.mean()
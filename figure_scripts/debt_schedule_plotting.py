# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:08:28 2022

@author: cmpet
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set()
data_path = 'D:/'
#data_path = 'F:/MonteCarlo_Project/Cornell_UNC/board_meeting_model_outputs' #vgrid pathway

for run_id in [162]:
    sim_list = [1, 20, 19]; bond_colors = ['orchid', 'mediumvioletred', 'deeppink', 'palevioletred', 'crimson']; sim_type = ['Scenario 1', 'Scenario 2', 'Scenario 3']
    #add additional total debt colors for additional simulation runs
    total_debt_colors = ['crimson', 'aqua', 'dodgerblue']
    high_interest_inflation = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f' + str(run_id) + '_s8_r1.csv')
    
    total_debt_comparison = pd.DataFrame(columns = sim_type)
    for index, sim in enumerate(sim_list):
        #bring the debt service tables in - if only looking at how the initial bonds are set up you only need to bring in the first realization (the same for each realization)
        debt_service_data_names = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, nrows = 2)
        debt_service_data = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, index_col = 0, skiprows = 2)
        existing_debt = pd.read_excel(data_path + 'input_data/budget_data/Current_Future_BondIssues.xlsx', sheet_name = 'FutureDSTotals', usecols = ['Total'])
        
        # debt_service_data_names = pd.read_csv(data_path + '/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, nrows = 2) #vgrid pathways
        # debt_service_data = pd.read_csv(data_path + '/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, index_col = 0, skiprows = 2) #vgrid pathways
        # existing_debt = pd.read_excel('F:/MonteCarlo_Project/Cornell_UNC/financial_model_input_data/model_input_data/Current_Future_BondIssues.xlsx', sheet_name = 'FutureDSTotals', usecols = ['Total']) #vgrid pathway
        
        existing_debt = existing_debt.squeeze()
        existing_debt = existing_debt.iloc[1:]
        Fiscal_Year = debt_service_data.iloc[1:,0]
        Bond_2023_totals = debt_service_data.iloc[1:, 4].fillna(0)
        Bond_2_totals = debt_service_data.iloc[1:, 9].fillna(0)
        Bond_3_totals = debt_service_data.iloc[1:, 14].fillna(0)
        Bond_4_totals = debt_service_data.iloc[1:, 19].fillna(0)
        
        #Stack the Bond payments ontop of one another
        debtBYbondFIG = plt.figure(figsize = (12,7))
        plt.bar(Fiscal_Year, existing_debt, color = bond_colors[0], label = 'Existing Debt')
        plt.bar(Fiscal_Year, Bond_2023_totals, bottom = existing_debt, color = bond_colors[1], label = '2023 Bond')
        plt.bar(Fiscal_Year, Bond_2_totals, bottom= existing_debt + Bond_2023_totals, color = bond_colors[2], label = '2025 Bond')
        plt.bar(Fiscal_Year, Bond_3_totals, bottom = existing_debt + Bond_2023_totals + Bond_2_totals, color = bond_colors[3], label = '2027 Bond')
        plt.bar(Fiscal_Year, Bond_4_totals, bottom =existing_debt + Bond_2023_totals + Bond_2_totals + Bond_3_totals, color = bond_colors[4], label = '2029 Bond')
        
        #ax = debtBYbondFIG.add_axes()
        plt.xticks(np.arange(min(Fiscal_Year), max(Fiscal_Year) + 1, 1), rotation = 90, fontsize = 18)
        plt.ylim(0, 160000000)
        plt.yticks(ticks = [20000000, 40000000, 60000000, 80000000, 100000000, 120000000, 140000000, 160000000], labels = [20, 40, 60, 80, 100, 120, 140, 160], fontsize=18)
        plt.ylabel('Annual Debt Service ($100 Million)', fontsize = 20, weight='bold')
        plt.xlabel('Fiscal Year', fontsize = 20, weight='bold')
        plt.legend(fontsize=14, frameon=False)
        #plt.savefig(data_path + '/figures/bond_debt_service_f' + str(run_id) + '_s' + str(sim) + '.png', bbox_inches= 'tight', dpi = 800)
        # plt.savefig(data_path + '/bond_debt_service_f' + str(run_id) + '_s' + str(sim) + '.png', bbox_inches= 'tight', dpi = 800) #vgrid pathway
        #plt.show()
        
        total_debt_service = existing_debt + Bond_2023_totals + Bond_2_totals + Bond_3_totals + Bond_4_totals
        # TotalDebtFig = plt.figure(figsize = (15,8))
        # plt.bar(Fiscal_Year, total_debt_service, color = total_debt_colors[index], label = sim_type[index])
        # plt.ylim(0, 140000000)
        # plt.xticks(np.arange(min(Fiscal_Year), max(Fiscal_Year) + 1, 1), rotation = 90, fontsize = 14)
        #plt.legend()
        #plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig4a_' + str(sim) + '.png', bbox_inches= 'tight', dpi = 900)
        #plt.savefig(data_path + '/total_debt_service_by_sim_f' + str(run_id) + '_s' + str(sim) + '.png', bbox_inches = 'tight', dpi =800) #vgrid pathway
        
        total_debt_comparison[sim_type[index]] = total_debt_service
    
    
    AllTotalDebtFig = plt.figure(figsize = (12,7))
    plt.bar(Fiscal_Year, total_debt_comparison.iloc[:,2], color = total_debt_colors[2], label = sim_type[2])
    plt.bar(Fiscal_Year, total_debt_comparison.iloc[:,1], hatch='o', color= 'none', edgecolor = total_debt_colors[1], linewidth=2, label = sim_type[1])
    plt.bar(Fiscal_Year, total_debt_comparison.iloc[:,0], hatch='x', color= 'none', edgecolor= total_debt_colors[0], linewidth=2, label = sim_type[0])
    plt.ylim(0, 160000000)
    plt.yticks(ticks = [20000000, 40000000, 60000000, 80000000, 100000000, 120000000, 140000000, 160000000], labels = [20, 40, 60, 80, 100, 120, 140, 160], fontsize=18)
    #plt.yticks([])
    plt.xticks(np.arange(min(Fiscal_Year), max(Fiscal_Year) + 1, 1), rotation = 90, fontsize = 18)
    plt.ylabel('Annual Debt Service ($100 Million)', fontsize = 20, weight='bold')
    plt.xlabel('Fiscal Year', fontsize = 20, weight='bold')
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [2, 1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], fontsize=14, markerscale=7, frameon=False)
    #plt.savefig('C:/Users/cmpet/OneDrive/Documents/UNC Chapel Hill/TBW/figures/thesis_figures/fig4b.png', bbox_inches= 'tight', dpi = 900)
    #plt.savefig(data_path + '/total_bond_debt_service_f' + str(run_id) + '.png', bbox_inches= 'tight', dpi = 800) #vgrid pathway
    
    
    #Cumulative sum of debt:
debt_service_data_names = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f162_s0_r1.csv', header = None, nrows = 2)
debt_service_data = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f162_s0_r1.csv', header = None, index_col = 0, skiprows = 2)
high_debt_service_data = pd.read_csv(data_path + 'Modeloutput/debt_service_schedule_f162_s8_r1.csv', header = None, index_col = 0, skiprows = 2)
existing_debt = pd.read_excel(data_path + 'input_data/budget_data/Current_Future_BondIssues.xlsx', sheet_name = 'FutureDSTotals', usecols = ['Total'])
        
# debt_service_data_names = pd.read_csv(data_path + '/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, nrows = 2) #vgrid pathways
# debt_service_data = pd.read_csv(data_path + '/debt_service_schedule_f' + str(run_id) + '_s' + str(sim) + '_r1.csv', header = None, index_col = 0, skiprows = 2) #vgrid pathways
# existing_debt = pd.read_excel('F:/MonteCarlo_Project/Cornell_UNC/financial_model_input_data/model_input_data/Current_Future_BondIssues.xlsx', sheet_name = 'FutureDSTotals', usecols = ['Total']) #vgrid pathway
        
# existing_debt = existing_debt.squeeze()
# Fiscal_Year = debt_service_data.iloc[:,0]
# Bond_2023_totals = debt_service_data.iloc[:, 4].fillna(0)
# Bond_2_totals = debt_service_data.iloc[:, 9].fillna(0)
# Bond_3_totals = debt_service_data.iloc[:, 14].fillna(0)
# Bond_4_totals = debt_service_data.iloc[:, 19].fillna(0)
# high_2023 = high_debt_service_data.iloc[:, 4].fillna(0)
# high_2025 = high_debt_service_data.iloc[:, 9].fillna(0)
# high_2027 = high_debt_service_data.iloc[:, 14].fillna(0)
# high_2029 = high_debt_service_data.iloc[:, 19].fillna(0)
# high_total = existing_debt + high_2023 + high_2025 + high_2027 + high_2029
        
# #Stack the Bond payments ontop of one another
# debtBYbondFIG = plt.figure(figsize = (15,8))
# plt.bar(Fiscal_Year, high_total, hatch='x', color= 'none', edgecolor= 'darkorange', linewidth=2)
# plt.bar(Fiscal_Year, existing_debt, color = bond_colors[0])
# plt.bar(Fiscal_Year, Bond_2023_totals, bottom = existing_debt, color = bond_colors[1])
# plt.bar(Fiscal_Year, Bond_2_totals, bottom= existing_debt + Bond_2023_totals, color = bond_colors[2])
# plt.bar(Fiscal_Year, Bond_3_totals, bottom = existing_debt + Bond_2023_totals + Bond_2_totals, color = bond_colors[3])
# plt.bar(Fiscal_Year, Bond_4_totals, bottom =existing_debt + Bond_2023_totals + Bond_2_totals + Bond_3_totals, color = bond_colors[4])


        
# #ax = debtBYbondFIG.add_axes()
# plt.xticks(np.arange(min(Fiscal_Year), max(Fiscal_Year) + 1, 1), rotation = 90, fontsize = 14)
# plt.ylim(0, 160000000)
# #plt.ylabel('Debt Service ($100 Million)', fontsize = 14)
# #plt.xlabel()
# plt.legend()
    
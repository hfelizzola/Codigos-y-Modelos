#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:26:31 2024

@author: hfelizzola
"""

#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from cleaning_rural_roads import clean_data
from summary_rural_roads import deviation_summary
from summary_rural_roads import hplot_cost_deviation, vplot_cost_deviation
plt.rcParams['figure.dpi'] = 200

#%%
datos = pd.read_csv("https://raw.githubusercontent.com/NicolasArrietaC/Cost-and-Time-Deviation-in-Colombian-Rural-Roads_extended_version/master/data/collected_obra_data_v2.csv")
datos.head()

#%% Clean data
df = clean_data(datos)

#%% Summary statis for cost deviation
dev_cost_data = df.loc[df['COST_DEVIATION_FREC'] > 0]['COST_DEVIATION_ORIG'].copy()
dev_cost_summary = pd.DataFrame({
    'Estadística':['N', 'Frequency', 'Frequency Cost Deviation (%)', 'Average Magnitude Deviation (%)', 
                   'Min Magnitude Deviation (%)', 'Max Magnitude Deviation (%)', 'Standard Deviation Magnitude',
                   'Coefficient of Variation'],
    'Valor': [df.shape[0], 
              df['COST_DEVIATION_FREC'].sum(), 
              df['COST_DEVIATION_FREC'].mean()*100, 
              dev_cost_data.mean()*100,
              dev_cost_data.min()*100,
              dev_cost_data.max()*100,
              dev_cost_data.std()*100,
              (dev_cost_data.std()/dev_cost_data.mean())*100]
})
print(dev_cost_summary)
print(dev_cost_data.describe())

# Crear histograma
plt.hist(dev_cost_data, edgecolor='black', bins=np.arange(0, 1.1, 0.1), color='lightgrey')
plt.xticks(np.arange(0, 1.1, 0.1))
plt.gca().set_xticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_xticks()])
plt.xlabel('Magnitude of cost deviation (%)')
plt.ylabel('Number of projects')
plt.show()

#%% Cost deviation analysis by contract value range
# Summary of cost deviation by contract value range
cost_dev_value = deviation_summary(df, aggregate_var='CONTRACT_VALUE_RANGE',
                                   frequency_var='COST_DEVIATION_FREC',
                                   magnitude_var='COST_DEVIATION_ORIG')
print(cost_dev_value)

# Plot cost deviation summary
hplot_cost_deviation(cost_dev_value, 'CONTRACT_VALUE_RANGE_', 'COST_DEVIATION_FREC_MEAN', 'COST_DEVIATION_ORIG_MEAN', 
                    'Contract Value Range (Millions of COP)', 'Cost Deviation (%)')

#%% Cost deviation analysis by type of process
cost_dev_process = deviation_summary(df, aggregate_var='PROCESS_TYPE_MOD',
                                   frequency_var='COST_DEVIATION_FREC',
                                   magnitude_var='COST_DEVIATION_ORIG')
print(cost_dev_process)

vplot_cost_deviation(cost_dev_process, 'COST_DEVIATION_FREC_MEAN', 'COST_DEVIATION_ORIG_MEAN', 'PROCESS_TYPE_MOD_', 
                    'Cost Deviation (%)','Process Type')


#%% Cost deviation analysis by type of project
cost_dev_type_project = deviation_summary(df, aggregate_var='TYPE_WORK',
                                   frequency_var='COST_DEVIATION_FREC',
                                   magnitude_var='COST_DEVIATION_ORIG')
print(cost_dev_type_project)

vplot_cost_deviation(cost_dev_type_project, 'COST_DEVIATION_FREC_MEAN', 'COST_DEVIATION_ORIG_MEAN', 'TYPE_WORK_', 
                    'Cost Deviation (%)','Type of Project')




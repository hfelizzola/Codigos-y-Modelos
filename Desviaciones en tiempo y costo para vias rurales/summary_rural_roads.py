#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:22:03 2024

@author: hfelizzola
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats




def deviation_summary(df, cost_var, duration_var, aggregate_var, frequency_var, magnitude_var):
    # Grouping and aggregating with custom column names
    summary_table = df.groupby(aggregate_var, observed=False).agg({
        cost_var:      [('MEAN','mean')],
        duration_var:  [('MEAN','mean')],   
        aggregate_var: [('N', 'size'),
                        ('Percent',(lambda x: len(x)/df.shape[0]))],  # Change name of size column
        frequency_var: [('COUNT', 'sum'), ('MEAN', 'mean')],  # Change names of sum and mean columns
        magnitude_var: [
            ('MEAN', lambda x: np.mean(x[x >= 0]))  # Custom aggregation only for values > 0, and change column name
        ]
    })
    summary_table.reset_index(inplace=True)
    summary_table.columns = ['_'.join(col).strip() for col in summary_table.columns.values]
    
    return summary_table


def hplot_cost_deviation(data, x_column, y1_column, y2_column, x_label, y_label, title=None):
    sns.pointplot(data=data, x=x_column, y=y1_column, color='orange', label='Frequency', markers='o', linestyles='-')
    sns.pointplot(data=data, x=x_column, y=y2_column, color='blue', label='Magnitude', markers='^', linestyles='--')
    
    # Improve legibility and aesthetics
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.legend(title='Type of Deviation', title_fontsize='13', labelspacing=1.2)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    
    # Enhance layout and display settings
    plt.grid(True)
    plt.gcf().set_size_inches(10, 6)
    plt.show()
    
def vplot_cost_deviation(data, x1_column, x2_column, y_column, x_label, y_label, title=None):
    sns.pointplot(data=data, x=x1_column, y=y_column, color='orange', label='Frequency', markers='o', linestyles='-')
    sns.pointplot(data=data, x=x2_column, y=y_column, color='blue', label='Magnitude', markers='^', linestyles='--')
    
    # Improve legibility and aesthetics
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.legend(title='Type of Deviation', title_fontsize='13', labelspacing=1.2)
    plt.gca().set_xticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_xticks()])
    
    # Enhance layout and display settings
    plt.grid(True)
    plt.gcf().set_size_inches(10, 6)
    plt.show()



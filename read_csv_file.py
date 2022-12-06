"""
Program to read and clean csv files.
"""
import os
import numpy as np
import sys, string
import pandas as pd

def read_file(file):
    # create DataFrame with csv data
    shark_attacks_df = pd.read_csv(file)

    # drop the empty bottom rows and unnecessary columns
    shark_attacks_df.drop(shark_attacks_df.tail(19419).index,inplace=True)
    shark_attacks_df.drop(['pdf', 'href formula', 'Case Number.1', 'Case Number.2', 'original order', 'Unnamed: 22', 'Unnamed: 23'], axis=1, inplace=True)

    # change all data to lower cases
    shark_attacks_df =  shark_attacks_df.applymap(lambda s:s.lower() if type(s) == str else s)
    # replace empty values with 0
    shark_attacks_df = shark_attacks_df.fillna(0)

    # change years into integers and order by year
    shark_attacks_df['Year'] = shark_attacks_df['Year'].astype({'Year':'int'})
    shark_attacks_df.sort_values(by=['Year'])

    # clean values in Fatal
    shark_attacks_df['Fatal (Y/N)'] = shark_attacks_df['Fatal (Y/N)'].replace({' n':'n', 'n ':'n', 'm':np.nan, '2017':np.nan, 'unknown':np.nan})

    print(shark_attacks_df.columns)

    return shark_attacks_df

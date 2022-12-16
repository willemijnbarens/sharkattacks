"""
Program to read and clean csv files.
"""
import os
import numpy as np
import sys, string
import pandas as pd

def read_shark_file(file):
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

    # rename column and clean values in Fatal
    shark_attacks_df = shark_attacks_df.rename(columns={'Fatal (Y/N)': 'Fatal'})
    shark_attacks_df['Fatal'] = shark_attacks_df['Fatal'].replace({' n':'n', 'n ':'n', 'm':0, '2017':0, 'unknown':0})

    return shark_attacks_df

def read_world_file(world_file):
    # create DataFrame with csv data
    world_df = pd.read_csv(world_file)

    # import shark data
    shark_attacks_df = read_shark_file('attacks.csv')

    # change all data to lower cases
    world_df =  world_df.applymap(lambda s:s.lower() if type(s) == str else s)

    # merge with shark DataFrame on area
    new_df = shark_attacks_df.join(world_df.set_index(['admin_name']), on=['Area'], how='left')
    # drop duplicate shark attacks based on unique case number
    new_df = new_df.drop_duplicates(subset=['Case Number'])

    # replace empty values with 0
    new_df = new_df.fillna(0)

    # count fatal shark attacks per area and add to sharks_df
    fatalities = new_df.groupby(["Area"])["Fatal"].apply(lambda x: (x=='y').sum()).reset_index(name='fatalities')
    new_df = new_df.join(fatalities.set_index(['Area']), on=['Area'], how='left')

    # merge missing data that didn't have area data on country
    condition = new_df.loc[new_df['lat'] == 0.0]
    # drops coordinates columns
    condition = condition.drop(columns=['city', 'city_ascii', 'lat', 'lng', 'iso2', 'iso3', 'capital', 'population', 'id', 'fatalities'])
    # join DataFrames
    condition = condition.join(world_df.set_index(['country']), on=['Country'], how='left')
    # drop duplicate shark attacks based on unique case number
    condition = condition.drop_duplicates(subset=['Case Number'])

    # count fatal shark attacks per country and add to sharks_df
    fatalities = condition.groupby(["Country"])["Fatal"].apply(lambda x: (x=='y').sum()).reset_index(name='fatalities')
    condition = condition.join(fatalities.set_index(['Country']), on=['Country'], how='left')

    # drop rows that are in the condition DataFrame
    new_df = new_df.drop(new_df[new_df.lat == 0.0].index)
    # merge the condition and the new DataFrame
    new_df = new_df.append(condition)

    # replace empty values with 0
    new_df = new_df.fillna(0)

    return new_df

# Setting path
import sys
import os
# getting the name of the directory where the this file is present.
current = os.path.abspath('')
# Getting the parent directory 
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)


#Importing important libraries
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import warnings
import holidays
warnings.filterwarnings('ignore')
import pickle

#Importing files
import config
import crowd_preprocessing_script as cps
import append_holiday


def preprocessing(data_filename,rest_id,item_name,frq):
    #address_file  = 'iso_address.csv'
    #data_filename = 'CG-Hinjewadi-Pune.json.pickle'
    df = pd.read_pickle(config.DATA+'//data//ver2//'+data_filename)
    #af = pd.read_csv(config.DATA+'//data//ver2//'+address_file)

    #print(len(df['restaurantname'].unique()),len(df['restaurant'].unique()))

    # overwriting data after changing format
    df['placedtime'] = pd.to_datetime(df['placedtime'], format="%Y-%m-%dT%H:%M:%S.%f", errors = 'coerce')
    df['placedtime'] = df['placedtime'].dt.tz_convert('Asia/Kolkata')

    #Select past 2 months data
    df = df[df['placedtime']>'2022-11-01']

    # Removing test payment gateway and cancelled orders
    df= df[df['paymentgateway'] != 'gokhana-test']
    df= df[df['status'] != 'paid-and-cancelled']

    #Select food court
    food_court_id = df['foodcourt'].iloc[1]

    if (os.path.isfile(config.DATA+'//data//ver2//reports//'+data_filename+'.report.csv') == False):
        df.groupby(['restaurantname','restaurant','menuitemname','restaurantmenuitem'])['count'].sum().to_csv(config.DATA+'//data//ver2//reports//'+data_filename+'.report.csv')

    # # Select resturant
    # print(list(df['restaurant'].unique()))
    # rest_id
    # Filtering our target restaurant from our df
    df2 = df[df['restaurant'] == rest_id]

    # Filling missing customer data
    df2['restaurantcustomer'].fillna('missing_cust_ID')

    #Selecting menu items
    item_id = list(df2['menuitemname'].unique())

    # Select desired columns
    df2 = df2[['placedtime','restaurantcustomer','menuitemname','count']]
    df4 = pd.DataFrame(columns = ['menuitemname','count'])
    t_index = pd.date_range("2022-11-01 00:00:00+05:30", "2022-12-27 23:00:00+05:30", freq=frq)
    j = 0
    for i in item_id:
        df3 = df2[df2['menuitemname'] == i]
        df3 = df3.resample(frq,on='placedtime').sum()
        df3 = df3.reindex(t_index).fillna(0)
        df3['menuitemname'] = [i]*len(df3)
        df3 = df3.reset_index().rename(columns = {'index':'placedtime'})
        df4 = df4.append(df3, ignore_index = True)
        j+=1
        #print(len(df3), end = ", ")
        #print(j, end = ", ")
       
    df4 = df4.sort_values(by=['placedtime'],ascending=True)
    df4 = df4[['placedtime','menuitemname','count']]
    df4 = df4.reset_index(drop= True)

    # Getting crowd count
    crowd_df = cps.crowd_num(data_filename,frq)
    crowd_df = crowd_df.reset_index()
    df4['crowd_count'] = [0]*len(df4)

    # Adding crowd count to our df
    for i in range(len(crowd_df['placedtime'])):
        df4.loc[df4['placedtime'] == crowd_df['placedtime'][i], 'crowd_count'] = crowd_df['restaurantcustomer'][i]
    df4['crowd_count'].value_counts()

    # Select menu item
    df5 = df4[df4['menuitemname'] == item_name]
    #df5 = df4

    df5 = append_holiday.add_holiday(df5,food_court_id)
    df5 = df5[['placedtime','menuitemname','holiday','crowd_count','count']]
    return df5
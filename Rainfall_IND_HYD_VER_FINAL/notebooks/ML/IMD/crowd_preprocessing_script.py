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
import config
warnings.filterwarnings('ignore')
import pickle

# address_file  = 'iso_address.csv'
# data_filename = 'CG-Hinjewadi-Pune.json.pickle'
def crowd_num(data_filename,frq):

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

    df = df[['placedtime','restaurantcustomer']]
    df = df.resample(frq, on = 'placedtime').nunique()
    return df

import pandas as pd
import numpy as np

def date_features(dataset):
    #if pd.infer_freq(dataset.index) == 'H':
    dataset['min'] = dataset.index.minute
    dataset['hour'] = dataset.index.hour
    dataset['date'] = dataset.index.day
    dataset['month'] = dataset.index.month
    #dataset['year'] = dataset.index.year
    dataset['dayofweek'] = dataset.index.dayofweek
    return dataset

# Cyclic encoding function
def encode(dataset, col, max_val):
    dataset[col + '_sin'] = np.sin(2 * np.pi * dataset[col]/max_val)
    dataset[col + '_cos'] = np.cos(2 * np.pi * dataset[col]/max_val)
    dataset.drop(col,axis = 1, inplace = True)
    return dataset

def encode_extract(df):
    #Setting placed time as datetime index
    df = df.set_index('placedtime')
    # Adding date features
    df_model = date_features(df)
    
    # Encoding df
    df_model = encode(df_model,'min',60)
    df_model = encode(df_model,'hour',24)
    df_model = encode(df_model,'date',31)
    df_model = encode(df_model,'month',12)
    #df_model = encode(df_model,'year',2)
    df_model = encode(df_model,'dayofweek',7)
    return df_model

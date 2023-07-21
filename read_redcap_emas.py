#!/bin/env python   

import pandas as pd
import getRecord

def plotEMAs(file='/home/jackgray/Downloads/MOREProject-RptEMAcompletion_DATA_2022-10-09_2110.csv'):
    ema_df = pd.read_csv(file)
    
    completion = ema_df['ema_complete']
    
    for i in completion:
        print(completion)
        
plotEMAs()
#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly_express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import empiricaldist as emp
import datetime as dt
import math
import re
import os
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('darkgrid')


# In[ ]:



#Importing Dataset
df1 = pd.read_csv('RTRA_Employ_2NAICS_00_05.csv', parse_dates=([['SYEAR', 'SMTH']]))
df2 = pd.read_csv('RTRA_Employ_2NAICS_06_10.csv', parse_dates=([['SYEAR', 'SMTH']]))
df3 = pd.read_csv('RTRA_Employ_2NAICS_11_15.csv', parse_dates=([['SYEAR', 'SMTH']]))
df4 = pd.read_csv('RTRA_Employ_2NAICS_16_20.csv', parse_dates=([['SYEAR', 'SMTH']]))
df5 = pd.read_csv('RTRA_Employ_2NAICS_97_99.csv', parse_dates=([['SYEAR', 'SMTH']]))
df6 = pd.read_csv('RTRA_Employ_3NAICS_00_05.csv', parse_dates=([['SYEAR', 'SMTH']]))
df7 = pd.read_csv('RTRA_Employ_3NAICS_06_10.csv', parse_dates=([['SYEAR', 'SMTH']]))
df8 = pd.read_csv('RTRA_Employ_3NAICS_11_15.csv', parse_dates=([['SYEAR', 'SMTH']]))
df9 = pd.read_csv('RTRA_Employ_3NAICS_16_20.csv', parse_dates=([['SYEAR', 'SMTH']]))
df10 = pd.read_csv('RTRA_Employ_3NAICS_97_99.csv', parse_dates=([['SYEAR', 'SMTH']]))
df11 = pd.read_csv('RTRA_Employ_4NAICS_00_05.csv', parse_dates=([['SYEAR', 'SMTH']]))
df12 = pd.read_csv('RTRA_Employ_4NAICS_06_10.csv', parse_dates=([['SYEAR', 'SMTH']]))
df13 = pd.read_csv('RTRA_Employ_4NAICS_11_15.csv', parse_dates=([['SYEAR', 'SMTH']]))
df14 = pd.read_csv('RTRA_Employ_4NAICS_16_20.csv', parse_dates=([['SYEAR', 'SMTH']]))
df15 = pd.read_csv('RTRA_Employ_4NAICS_97_99.csv', parse_dates=([['SYEAR', 'SMTH']]))


# In[ ]:


#Concatenation of all three NAICS data frames
two_digit = pd.concat([df1, df2, df3, df4, df5])
three_digit = pd.concat([df6, df7, df8, df9, df10])
four_digit = pd.concat([df11, df12, df13, df14, df15])
two_digit.head()


# In[ ]:



# Reading & Exploring LMO Detailed Industries Data
df_LMO = pd.read_excel('LMO_Detailed_Industries_by_NAICS.xlsx')
df_LMO.info()


# In[ ]:


#Cleaning Data
#Cleaning LMO Detailed Industries

# Changing data types
df_LMO.NAICS.astype('str')
# Cleaning strings
for i in range(len(df_LMO)):
    if '&' in str(df_LMO.NAICS[i]):
        df_LMO.NAICS[i] = df_LMO.NAICS[i].replace(' & ',',')

# Splitting data
for i in range(len(df_LMO)):
    if ',' in str(df_LMO.NAICS[i]):
        df_LMO.NAICS[i] = str(df_LMO.NAICS[i]).split(',')
# Reshaping Dataframe
df_LMO = df_LMO.explode(column='NAICS').reset_index()[['LMO_Detailed_Industry','NAICS']]
df_LMO.info()


# In[ ]:


#Cleaning RTRA CSV Files
df_full = pd.DataFrame()
#Renaming columns
two_digit.rename(columns = {'_EMPLOYMENT_':'employment'},inplace=True)

#Extracting codes from NAICS using regex

two_digit['code'] = 'a'
for i in range(len(two_digit)):
    if '[' not in two_digit.NAICS[i]:
        two_digit.code[i]='0000'
    else:
        x=re.search(r'(\[(\d+-?\d+(-?\d+)?)])',two_digit.NAICS[i])
        two_digit.code[i] = x.group(2)
        two_digit.NAICS[i]=(two_digit.NAICS[i].replace(x.group(1),'')).strip()
        
# Reshaping dataframe
two_digit = (two_digit.set_index(['SYEAR', 'SMTH','NAICS','employment']) .apply(lambda x: x.str.split('-').explode()).reset_index())

two_digit = two_digit[['SYEAR','SMTH','code','NAICS','employment']]   

#Renaming columns
three_digit.rename(columns = {'_EMPLOYMENT_':'employment'},inplace=True)

#Extracting codes from NAICS using regex

three_digit['code'] = 'a'
for i in range(len(three_digit)):
    if '[' not in two_digit.NAICS[i]:
        three_digit.code[i]='0000'
    else:
        x=re.search(r'(\[(\d+-?\d+(-?\d+)?)])',three_digit.NAICS[i])
        three_digit.code[i] = x.group(2)
        three_digit.NAICS[i]=(three_digit.NAICS[i].replace(x.group(1),'')).strip()
        
# Reshaping dataframe
three_digit = (three_digit.set_index(['SYEAR', 'SMTH','NAICS','employment']) .apply(lambda x: x.str.split('-').explode()).reset_index())

three_digit = three_digit[['SYEAR','SMTH','code','NAICS','employment']]   

#Renaming columns
four_digit.rename(columns = {'_EMPLOYMENT_':'employment'},inplace=True)

#Extracting codes from NAICS using regex

four_digit['code'] = 'a'
for i in range(len(four_digit)):
    if '[' not in two_digit.NAICS[i]:
        four_digit.code[i]='0000'
    else:
        x=re.search(r'(\[(\d+-?\d+(-?\d+)?)])',four_digit.NAICS[i])
        four_digit.code[i] = x.group(2)
        four_digit.NAICS[i]=(four_digit.NAICS[i].replace(x.group(1),'')).strip()
        
# Reshaping dataframe
four_digit = (four_digit.set_index(['SYEAR', 'SMTH','NAICS','employment']) .apply(lambda x: x.str.split('-').explode()).reset_index())

four_digit = four_digit[['SYEAR','SMTH','code','NAICS','employment']]   

df_full = df_full.append(two_digit) 

df_full = df_full.append(three_digit) 
        
df_full = df_full.append(four_digit)         
   
# Cleaning up

df_full.reset_index(drop=True,inplace=True)

df_LMO.code = df_LMO.code.astype('int')
df_full.code = df_full.code.astype('int')
      
#Merging dataframes 
LMO_full = pd.merge(df_LMO,df_full[['SYEAR','SMTH','code','employment']],on=['code'],how='left')
LMO_full = LMO_full[(LMO_full.SYEAR > 1996) & (LMO_full.SYEAR < 2019)]

#Creating final output template file 

output = LMO_full[['SYEAR','SMTH','NAICS','employment']].groupby(['NAICS','SYEAR','SMTH']).sum().reset_index()
output.sort_values(['SYEAR','SMTH','NAICS']).reset_index(drop=True)

output.SYEAR=output.SYEAR.astype('int')
output.SMTH = output.SMTH.astype('int')
output.employment = output.employment.astype('int')
output = output[['SYEAR','SMTH','NAICS','employment']]
output = output.sort_values(['SYEAR','SMTH','NAICS']).reset_index(drop=True)
            


# In[ ]:


#Timeseries Analysis
timeseries = output
timeseries['date'] = pd.to_datetime(timeseries.SYEAR.astype(str) + '/' + timeseries.SMTH.astype(str) + '/01')
timeseries.drop(['SYEAR','SMTH'],inplace=True,axis=1)
#How employment in Construction evolved overtime?
fig = px.line(timeseries[timeseries.NAICS == 'Construction'],x = 'date',y='employment',title='Evolution of Constraction over Time')
fig.show()

#How employment in Construction evolved over time, compared to the total employment across all industries?

fig = go.Figure()
fig.add_trace(go.Scatter(x=timeseries[timeseries.NAICS == 'Construction'].date, y=timeseries[timeseries.NAICS == 'Construction'].employment,name = 'Construction'))
fig.add_trace(go.Scatter(x=timeseries.groupby('date').sum().reset_index().date, y=timeseries.groupby('date').sum().reset_index().employment,name = 'Total'))
fig.update_layout(title='Employment in Construction over time WRT total employment',
                   xaxis_title='Date',
                   yaxis_title='Employment')
fig.update_layout(yaxis_type="log")
fig.show()

#Finding the top ten industries each year 
dicts = {}
years = list(timeseries.year.unique())
for i in years:
    temp = timeseries.groupby(['year','NAICS']).mean().reset_index()
    dicts[i] = list(temp[temp.year == i].nlargest(10,'employment').NAICS)
df = pd.DataFrame(dicts)
fig = px.bar(pd.DataFrame(df.stack().value_counts()).reset_index(), y="index", x=0, orientation='h')
fig.update_layout(title='Frequency of top 10 Industries overtime',
                   xaxis_title='Count',
                   yaxis_title='Industries')
fig.show()
 
# Finding the bottom industries
dicts = {}
years = list(timeseries.year.unique())
for i in years:
    temp = timeseries.groupby(['year','NAICS']).mean().reset_index()
    dicts[i] = list(temp[temp.year == i].nsmallest(10,'employment').NAICS)
df = pd.DataFrame(dicts)
fig = px.bar(pd.DataFrame(df.stack().value_counts()).reset_index(), y="index", x=0, orientation='h')
fig.update_layout(title='Frequency of bottom 10 Industries overtime',
                   xaxis_title='Count',
                   yaxis_title='Industries')
fig.show()


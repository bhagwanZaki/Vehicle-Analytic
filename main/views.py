from django.shortcuts import render
import pandas as pd
import json 
from django.http import HttpResponse

# Funtion for Filtering and Cleaning Dataframe 
def filtering_and_cleaning_dataframe():

    '''
        This funtion will return dataframe with 4 columns - Column 1 will be Vehicle Class, Column 2-4 will be months (April-2021, May-2021 and June-2021)
    '''

    # Reading data from 3 excel sheet with no header
    df1 = pd.read_excel('excel_sheet/April-2021.xlsx',header = None,thousands=',')
    df2 = pd.read_excel('excel_sheet/May-2021.xlsx',header = None,thousands=',')
    df3 = pd.read_excel('excel_sheet/June-2021.xlsx',header = None,thousands=',')
    
    # Creating Column Header of all 3 dataframe
    df1.columns = ["Serial", "Class", "Total"]
    df2.columns = ["Serial", "Class", "Total"]
    df3.columns = ["Serial", "Class", "Total"]

    # Droping starting 3 row with inplace = True 
    df1.drop([0,1,2],inplace=True,axis='rows')
    df2.drop([0,1,2],inplace=True,axis='rows')
    df3.drop([0,1,2],inplace=True,axis='rows')
    
    # Droping Serial Column with inplace = True
    df1.drop('Serial',inplace=True,axis='columns')
    df2.drop('Serial',inplace=True,axis='columns')
    df3.drop('Serial',inplace=True,axis='columns')

    # Removing .00 since it is units and units cannot be in decimal
    df1['Total'] = pd.to_numeric(df1["Total"])
    df1['Total'] = df1["Total"].astype(int)
    df2['Total'] = pd.to_numeric(df2["Total"])
    df2['Total'] = df2["Total"].astype(int)
    df3['Total'] = pd.to_numeric(df3["Total"])
    df3['Total'] = df3["Total"].astype(int)

    # Merging df1 , df2 and df3 on Class Column with parameter how=outer to get union of all 3 dataframe
    final = df1.merge(df2,on='Class',how='outer').merge(df3,on='Class',how='outer')

    #Renamaing the final data framing column header
    final.columns = ['Vehicle_Class','April_Total','May_Total','June_Total']

    return final

# Indexpage Table
def indexpage(request):
    # Getting Dataframe from filtering_and_cleaning_dataframe
    df = filtering_and_cleaning_dataframe()
    df = df.fillna(0)

    df['April_Total'] = df["April_Total"].astype(int)
    df['May_Total'] = df["May_Total"].astype(int)
    df['June_Total'] = df["June_Total"].astype(int)

    # Reseting the index of the DataFrame, and use the default one instead. And then converting it to json with orient=record
    json_records = df.reset_index().to_json(orient ='records') 
    data = [] 
    # Loading json in list
    data = json.loads(json_records) 
    context = {'datas': data} 
    return render(request, "main/index.html", context)

def download_dataframe(request):
    # Getting Dataframe from filtering_and_cleaning_dataframe
    results = filtering_and_cleaning_dataframe()

    # Renaming the result column header
    results.columns = ['Vehicle Class','April-2021','May-2021','June-2021']
    
    # Creating Response with csv content
    response = HttpResponse(content_type='text/csv')
    # Disposing 
    response['Content-Disposition'] = 'attachment; filename=result.csv'
    results.to_csv(path_or_buf=response)

    return response

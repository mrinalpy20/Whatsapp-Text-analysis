# import streamlit as st
import numpy as np
import seaborn as sn
import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import datetime


def gettimeanddate(string):
    string = string.split(',')
    date,time = string[0],string[1]
    time = time.split('-')
    time = time[0].strip()
    
    return [date,time]

def getuserandmsg(string):
    string=string.split('-')
    if ':' in string[1]:
        s=string[1].split(':')
        user=s[0]
        msg=s[1]
        
    else:
        user="Group_notification"
        msg=string[1]
    return [user,msg]

def preprocess(data):
    # f = open(data,'r',encoding='utf-8')

    # data = f.read()
    dummy = data.split('\n')
    chat_data=[]
    for text in dummy:
        # Remove \u202f and format the timestamp
        if '\u202f' in text:
            cleaned_text = re.sub(r'\u202f', '', text)
            chat_data.append(cleaned_text)
        else:
            chat_data.append(text)




    merged_text = []
    current_chunk = ""

    for line in chat_data:
        if re.match(r'\d{2}/\d{2}/\d{2}', line):  # Check if the line starts with a date
            if current_chunk:
                merged_text.append(current_chunk.strip())
            current_chunk = line
        else:
            current_chunk += " " + line

    # Append the last chunk if any
    if current_chunk:
        merged_text.append(current_chunk.strip())
    
    columns = ['Date', 'Time', 'User', 'Message','Month','Year','Month_num','Day','Day_name','Hour','Minute']
    df = pd.DataFrame(columns=columns)
    for i in merged_text:
        s=gettimeanddate(i)
        date=s[0]
        time=s[1]
        x=getuserandmsg(i)
        user=x[0]
        msg=x[1]
        datetime_obj = datetime.strptime(date, '%d/%m/%Y')
        
        month = datetime_obj.strftime('%B')  # %B gives the full month name
        year = datetime_obj.year
        month_num = datetime_obj.month
        day = datetime_obj.day
        day_name = datetime_obj.strftime('%A')
        
        time_obj = datetime.strptime(time, '%I:%M%p')
        
        # Extract hour and minute
        hour = time_obj.hour
        minute = time_obj.minute
        data = [date, time, user, msg, month, year, month_num, day, day_name, hour, minute]

        # Create a DataFrame with the new row
        new_row_df = pd.DataFrame([data], columns=columns)

        # Concatenate the existing DataFrame with the new row DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)
#         df = df.append(pd.Series([date,time,user,msg,month,year,month_num,day,day_name,hour,minute], index=columns), ignore_index=True)
        
        df = df[df['User'] != 'Group_notification']
        
    return df
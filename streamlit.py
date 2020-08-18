import datetime
import streamlit as st
from streamlit import caching
import pandas as pd
import altair as alt
import os
import matplotlib.pyplot as plt
import numpy as np
import requests
#%matplotlib inline


st.title('Github Issues Explorer')
owner = st.text_input("type the repo organization name", 'Thinkful-Ed')
repo = st.text_input("type the name of your repo", 'data-analytics-bootcamp')
st.write('Errors will appear below until an appropriate token is entered.')
token = st.text_input("paste your Github token", '')
st.write("Gettting Issues")

for page in range(5):
    
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
    "state": "all","per_page":100, "page":page,
    }
    headers = {'Authorization': f'token {token}'}
    repos_list = []
    r = requests.get(query_url, headers=headers, params=params)
    for i in r.json():
        repos_list.append(i)
    #print("Repo list created. Length: %s" % len(repos_list))
    json_data = repos_list
df = pd.DataFrame.from_dict(json_data)
st.write(str(df.shape[0])+' Issues Returned')

def ext_date(df, column):
    df[column] = pd.to_datetime(df[column],format = "%Y-%m-%d")
    df[column] = df[column].dt.strftime('%Y%m%d')

ext_date(df,'created_at')
ext_date(df,'updated_at')
ext_date(df,'closed_at')
st.dataframe(df.head())


DATE_COLUMN = 'created_at'
#DATA_URL = ('https://raw.githubusercontent.com/AVJdataminer/Fir/master/data/simple_all_repo_issues.csv')

st.subheader('Number of issues per day')
data = df[['created_at','title']]
cnt = pd.DataFrame(data.groupby('created_at').size().rename('Issues'))
cnt['rolling_mean7days'] = cnt['Issues'].rolling(window=7).mean()
cnt['rolling_mean14days'] = cnt['Issues'].rolling(window=14).mean()
st.line_chart(cnt)

#perhaps create a list from length of dates and filter that way
st.subheader('Select the date range for the chart below')
from datetime import date

today = pd.Timestamp(date.today())
before = today + datetime.timedelta(days=-90)

start_date = st.date_input('Start date', before)
end_date = st.date_input('End date ', today)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

st.write(start_date)
st.write(type(start_date))
data['created_at'] = pd.to_datetime(data['created_at']) 
#st.write(data['created_at'])
#st.write(type(data['created_at']))

#filter_mask = data[DATE_COLUMN] > start_date
#filter_mask2 = data[DATE_COLUMN] < end_date
filtered_df = data[(data['created_at']> start_date) & (data['created_at']< end_date)]
#st.dataframe(filtered_df.head())

cnt = pd.DataFrame(filtered_df.groupby('created_at').size().rename('Issues'))
cnt['rolling_mean7days'] = cnt['Issues'].rolling(window=7).mean()
cnt['rolling_mean14days'] = cnt['Issues'].rolling(window=14).mean()
st.line_chart(cnt)

st.subheader('Cummulative Sum of Issues')
cnt2 = pd.DataFrame(data.groupby('created_at').size().rename('Issues'))
cnt2['cum_sum'] = cnt2['Issues'].cumsum()
st.line_chart(cnt2)

st.subheader('Wordcloud of titles')
from wordcloud import WordCloud, STOPWORDS
text = df['title'].values 
wordcloud = WordCloud().generate(str(text))
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot()

st.subheader('Review titles for common issues')
tdf = pd.DataFrame(df.title.value_counts())
st.dataframe(tdf)

st.subheader('Wordcloud of body text')
text = df['body'].values 
wordcloud = WordCloud().generate(str(text))
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot()
#st.subheader('Select another repo...coming soon')
#st.write("Using a radio button restricts selection to only one option at a time.")



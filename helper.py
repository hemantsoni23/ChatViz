# Importing modules
import streamlit as st
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px

# Object
extract = URLExtract()

# -1 => Negative
# 0 => Neutral
# 1 => Positive

# Will return count of messages of selected user per day having k(0/1/-1) sentiment
def week_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['day_name'].value_counts()


# Will return count of messages of selected user per month having k(0/1/-1) sentiment
def month_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['month'].value_counts()

# Will return hear map containing count of messages having k(0/1/-1) sentiment
def activity_heatmap(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    
    # Creating heat map
    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
    return user_heatmap


# Will return count of messages of selected user per date having k(0/1/-1) sentiment
def daily_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==k]
    # count of message on a specific date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


# Will return count of messages of selected user per {year + month number + month} having k(0/1/-1) sentiment
def monthly_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==-k]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# Will return percentage of message contributed having k(0/1/-1) sentiment
def percentage(df,k):
    df = round((df['user'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df

# Return wordcloud from words in message
def create_wordcloud(selected_user,df,k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Remove entries of no significance
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    # Remove stop words according to text file "stop_hinglish.txt"
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    # Dimensions of wordcloud
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    
    # Actual removing
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'][temp['value'] == k]
    
    # Word cloud generated
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# Return set of most common words having k(0/1/-1) sentiment
def most_common_words(selected_user,df,k):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message'][temp['value'] == k]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    # Creating data frame of most common 20 entries
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# Function to filter data based on user
def filter_data_by_user(data, user):
    if user == 'Overall':
        return data
    else:
        return data[data['user'] == user]

# Function to show basic analysis plots
def show_basic_analysis(data, user):
    filtered_data = filter_data_by_user(data, user)
    
    # Line plot based on the number of messages each month-year
    st.subheader("Line plot based on the number of messages each month-year")
    monthly_counts = filtered_data.groupby(['year', 'month_num', 'user']).size().reset_index(name='count')
    fig = px.line(monthly_counts, x='month_num', y='count', color='user', markers=True, title='Number of Messages Each Month-Year')
    fig.update_layout(xaxis_title='Month-Year', yaxis_title='Number of Messages')
    st.plotly_chart(fig, config={'displaylogo': False})

    # Plot for the number of total messages on specific weekdays
    st.subheader("Plot for the number of total messages on specific weekdays")
    weekday_counts = filtered_data.groupby(['day_name', 'user']).size().reset_index(name='count')
    fig = px.bar(weekday_counts, x='day_name', y='count', color='user', barmode='group', title='Number of Messages on Specific Weekdays', labels={'day_name': 'Weekday', 'count': 'Number of Messages'})
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})
    st.plotly_chart(fig, config={'displaylogo': False})

    # Plot for the number of total messages on specific hours (in 12-hour format)
    st.subheader("Plot for the number of total messages on specific hours (in 12-hour format)")
    hourly_counts = filtered_data.groupby(['hour', 'user']).size().reset_index(name='count')
    fig = px.bar(hourly_counts, x='hour', y='count', color='user', barmode='group', title='Number of Messages on Specific Hours (12-hour format)', labels={'hour': 'Hour (12-hour format)', 'count': 'Number of Messages'})
    # fig.update_layout(height=500, width=800)
    st.plotly_chart(fig, config={'displaylogo': False})

    # Plot for the number of total messages on specific days of all the months
    st.subheader("Plot for the number of total messages on specific days of all the months")
    daily_counts = filtered_data.groupby(['day', 'user']).size().reset_index(name='count')
    fig = px.bar(daily_counts, x='day', y='count', color='user', barmode='group', title='Number of Messages on Specific Days of the Month', labels={'day': 'Day of the Month', 'count': 'Number of Messages'})
    # fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]})
    # fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True, theme='streamlit')
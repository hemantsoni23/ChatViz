# Importing modules
import nltk
import streamlit as st
import re
import preprocessor,helper
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# App title
st.sidebar.title("ChatViz")

# VADER : is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments.
nltk.download('vader_lexicon')

# File upload button
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Main heading
st. markdown("<h1 style='text-align: center; color: grey;'>ChatViz</h1>", unsafe_allow_html=True)

if uploaded_file is not None:
    
    # Getting byte form & then decoding
    bytes_data = uploaded_file.getvalue()
    d = bytes_data.decode("utf-8")

    # Perform preprocessing
    data = preprocessor.preprocess(d)
    
    # Importing SentimentIntensityAnalyzer class from "nltk.sentiment.vader"
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
    # Object
    sentiments = SentimentIntensityAnalyzer()
    
    # Creating different columns for (Positive/Negative/Neutral)
    data["po"] = [sentiments.polarity_scores(i)["pos"] for i in data["message"]] # Positive
    data["ne"] = [sentiments.polarity_scores(i)["neg"] for i in data["message"]] # Negative
    data["nu"] = [sentiments.polarity_scores(i)["neu"] for i in data["message"]] # Neutral
    
    # To indentify true sentiment per row in message column
    def sentiment(d):
        if d["po"] >= d["ne"] and d["po"] >= d["nu"]:
            return 1
        if d["ne"] >= d["po"] and d["ne"] >= d["nu"]:
            return -1
        if d["nu"] >= d["po"] and d["nu"] >= d["ne"]:
            return 0

    # Creating new column & Applying function
    data['value'] = data.apply(lambda row: sentiment(row), axis=1)
    
    # User names list
    user_list = data['user'].unique().tolist()
    
    # Sorting
    user_list.sort()
    
    # Insert "Overall" at index 0
    user_list.insert(0, "Overall")
    
    # Selectbox
    selected_user = st.sidebar.selectbox("Show analysis with respect to - ", user_list)
    
    if st.sidebar.button("Show Analysis"):
        # Monthly activity map
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Monthly Activity map(Positive)')
            
            busy_month = helper.month_activity_map(selected_user, data,1)
            
            fig = go.Figure(go.Bar(x=busy_month.index, y=busy_month.values, marker_color='green'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col2:
            st.subheader('Monthly Activity map(Neutral)')
            
            busy_month = helper.month_activity_map(selected_user, data, 0)
            
            fig = go.Figure(go.Bar(x=busy_month.index, y=busy_month.values, marker_color='grey'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col3:
            st.subheader('Monthly Activity map(Negative)')
            
            busy_month = helper.month_activity_map(selected_user, data, -1)
            
            fig = go.Figure(go.Bar(x=busy_month.index, y=busy_month.values, marker_color='red'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})

        # Daily activity map
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Daily Activity map(Positive)')
            
            busy_day = helper.week_activity_map(selected_user, data,1)
            
            fig = go.Figure(go.Bar(x=busy_day.index, y=busy_day.values, marker_color='green'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col2:
            st.subheader('Daily Activity map(Neutral)')
            
            busy_day = helper.week_activity_map(selected_user, data, 0)
            
            fig = go.Figure(go.Bar(x=busy_day.index, y=busy_day.values, marker_color='grey'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col3:
            st.subheader('Daily Activity map(Negative)')
            
            busy_day = helper.week_activity_map(selected_user, data, -1)
            
            fig = go.Figure(go.Bar(x=busy_day.index, y=busy_day.values, marker_color='red'))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})

        # Weekly activity map
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                st.subheader('Weekly Activity Map(Positive)')
                
                user_heatmap = helper.activity_heatmap(selected_user, data, 1)
                
                fig = px.imshow(user_heatmap, color_continuous_scale='Greens')
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                st.image('error.webp')
        with col2:
            try:
                st.subheader('Weekly Activity Map(Neutral)')
                
                user_heatmap = helper.activity_heatmap(selected_user, data, 0)
                
                fig = px.imshow(user_heatmap, color_continuous_scale='Greys')
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                st.image('error.webp')
        with col3:
            try:
                st.subheader('Weekly Activity Map(Negative)')
                
                user_heatmap = helper.activity_heatmap(selected_user, data, -1)
                
                fig = px.imshow(user_heatmap, color_continuous_scale='Reds')
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                st.image('error.webp')

        # Daily timeline
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Daily Timeline(Positive)')
            
            daily_timeline = helper.daily_timeline(selected_user, data, 1)
            
            fig = go.Figure(go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], mode='lines', marker=dict(color='green')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col2:
            st.subheader('Daily Timeline(Neutral)')
            
            daily_timeline = helper.daily_timeline(selected_user, data, 0)
            
            fig = go.Figure(go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], mode='lines', marker=dict(color='grey')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col3:
            st.subheader('Daily Timeline(Negative)')
            
            daily_timeline = helper.daily_timeline(selected_user, data, -1)
            
            fig = go.Figure(go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], mode='lines', marker=dict(color='red')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})

        # Monthly timeline
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Monthly Timeline(Positive)')
            
            timeline = helper.monthly_timeline(selected_user, data,1)
            
            fig = go.Figure(go.Scatter(x=timeline['time'], y=timeline['message'], mode='lines', marker=dict(color='green')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col2:
            st.subheader('Monthly Timeline(Neutral)')
            
            timeline = helper.monthly_timeline(selected_user, data,0)
            
            fig = go.Figure(go.Scatter(x=timeline['time'], y=timeline['message'], mode='lines', marker=dict(color='grey')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})
        with col3:
            st.subheader('Monthly Timeline(Negative)')
            
            timeline = helper.monthly_timeline(selected_user, data,-1)
            
            fig = go.Figure(go.Scatter(x=timeline['time'], y=timeline['message'], mode='lines', marker=dict(color='red')))
            fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
            st.plotly_chart(fig, config={'displaylogo': False})

        # Percentage contributed
        if selected_user == 'Overall':
            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader('Most Positive Contributions')
                x = helper.percentage(data, 1)
                
                # Displaying
                st.dataframe(x)
            with col2:
                st.subheader('Most Neutral Contributions')
                y = helper.percentage(data, 0)
                
                # Displaying
                st.dataframe(y)
            with col3:
                st.subheader('Most Negative Contributions')
                z = helper.percentage(data, -1)
                
                # Displaying
                st.dataframe(z)


        # Most Positive,Negative,Neutral User...
        if selected_user == 'Overall':
            
            # Getting names per sentiment
            x = data['user'][data['value'] == 1].value_counts().head(10)
            y = data['user'][data['value'] == -1].value_counts().head(10)
            z = data['user'][data['value'] == 0].value_counts().head(10)

            col1,col2,col3 = st.columns(3)
            with col1:
                # heading
                st.subheader('Most Positive Users')
                
                # Displaying
                fig = go.Figure(go.Bar(x=x.index, y=x.values, marker_color='green'))
                fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            with col2:
                # heading
                st.subheader('Most Neutral Users')
                
                # Displaying
                fig = go.Figure(go.Bar(x=z.index, y=z.values, marker_color='grey'))
                fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            with col3:
                # heading
                st.subheader('Most Negative Users')
                
                # Displaying
                fig = go.Figure(go.Bar(x=y.index, y=y.values, marker_color='red'))
                fig.update_layout(xaxis=dict(tickangle=-45), height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})

        # WORDCLOUD......
        col1,col2,col3 = st.columns(3)
        with col1:
            try:
                # heading
                st.subheader('Positive WordCloud')
                
                # Creating wordcloud of positive words
                df_wc = helper.create_wordcloud(selected_user, data,1)
                fig = go.Figure(go.Image(z=df_wc))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Display error message
                st.image('error.webp')
        with col2:
            try:
                # heading
                st.subheader('Neutral WordCloud')
                
                # Creating wordcloud of neutral words
                df_wc = helper.create_wordcloud(selected_user, data,0)
                fig = go.Figure(go.Image(z=df_wc))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Display error message
                st.image('error.webp')
        with col3:
            try:
                # heading
                st.subheader('Negative WordCloud')
                
                # Creating wordcloud of negative words
                df_wc = helper.create_wordcloud(selected_user, data,-1)
                fig = go.Figure(go.Image(z=df_wc))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Display error message
                st.image('error.webp')

        # Most common positive words
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                # Data frame of most common positive words.
                most_common_df = helper.most_common_words(selected_user, data,1)
                
                # heading
                st.subheader('Positive Words')
                fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='green'))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Disply error image
                st.image('error.webp')
        with col2:
            try:
                # Data frame of most common neutral words.
                most_common_df = helper.most_common_words(selected_user, data,0)
                
                # heading
                st.subheader('Neutral Words')
                fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='grey'))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Disply error image
                st.image('error.webp')
        with col3:
            try:
                # Data frame of most common negative words.
                most_common_df = helper.most_common_words(selected_user, data,-1)
                
                # heading
                st.subheader('Negative Words')
                fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='red'))
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig, config={'displaylogo': False})
            except:
                # Disply error image
                st.image('error.webp')
    
    if st.sidebar.button("Show basic Analysis"):
        helper.show_basic_analysis(data,selected_user)


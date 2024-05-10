# Importing modules
import nltk
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import preprocessor, helper
import pandas as pd

# Function to display behaviours analysis with caching
@st.cache_data
def display_behaviours_analysis(data, selected_users):
    # Monthly activity map
    st.subheader("Monthly Activity Map")
    busy_month_pos = helper.month_activity_map(selected_users, data, 1)
    busy_month_neu = helper.month_activity_map(selected_users, data, 0)
    busy_month_neg = helper.month_activity_map(selected_users, data, -1)

    fig = go.Figure()

    # Add trace for Positive sentiment
    fig.add_trace(go.Bar(
        x=busy_month_pos.index,
        y=busy_month_pos.values,
        name='Positive',
        marker_color='green'
    ))

    # Add trace for Neutral sentiment
    fig.add_trace(go.Bar(
        x=busy_month_neu.index,
        y=busy_month_neu.values,
        name='Neutral',
        marker_color='grey'
    ))

    # Add trace for Negative sentiment
    fig.add_trace(go.Bar(
        x=busy_month_neg.index,
        y=busy_month_neg.values,
        name='Negative',
        marker_color='red'
    ))

    # Update layout
    fig.update_layout(barmode='stack',
                    xaxis=dict(fixedrange=True),
                    yaxis=dict(fixedrange=True),
                    title='Monthly Activity Map',
                    xaxis_title='Month',
                    yaxis_title='Number of Messages')

    st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True)


    # Daily activity map
    st.subheader('Daily Activity map')
    busy_day_pos = helper.week_activity_map(selected_users, data, 1)
    busy_day_neu = helper.week_activity_map(selected_users, data, 0)
    busy_day_neg = helper.week_activity_map(selected_users, data, -1)

    fig = go.Figure()

    # Add trace for Positive sentiment
    fig.add_trace(go.Bar(
        x=busy_day_pos.index,
        y=busy_day_pos.values,
        name='Positive',
        marker_color='green'
    ))

    # Add trace for Neutral sentiment
    fig.add_trace(go.Bar(
        x=busy_day_neu.index,
        y=busy_day_neu.values,
        name='Neutral',
        marker_color='grey'
    ))

    # Add trace for Negative sentiment
    fig.add_trace(go.Bar(
        x=busy_day_neg.index,
        y=busy_day_neg.values,
        name='Negative',
        marker_color='red'
    ))

    # Update layout
    fig.update_layout(barmode='stack',
                      xaxis=dict(fixedrange=True),
                      yaxis=dict(fixedrange=True),
                      title='Daily Activity Map',
                      xaxis_title='Day',
                      yaxis_title='Number of Messages')

    st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True)

    # # Weekly activity map
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     try:
    #         st.subheader('Weekly Activity Map(Positive)')
            
    #         user_heatmap = helper.activity_heatmap(selected_users, data, 1)
            
    #         fig = px.imshow(user_heatmap, color_continuous_scale='Greens')
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         st.image('error.webp')
    # with col2:
    #     try:
    #         st.subheader('Weekly Activity Map(Neutral)')
            
    #         user_heatmap = helper.activity_heatmap(selected_users, data, 0)
            
    #         fig = px.imshow(user_heatmap, color_continuous_scale='Greys')
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         st.image('error.webp')
    # with col3:
    #     try:
    #         st.subheader('Weekly Activity Map(Negative)')
            
    #         user_heatmap = helper.activity_heatmap(selected_users, data, -1)
            
    #         fig = px.imshow(user_heatmap, color_continuous_scale='Reds')
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         st.image('error.webp')

    # Combine the three Daily Timeline plots into a single multiline plot
    st.subheader('Daily Timeline')

    fig = go.Figure()

    # Add trace for Positive sentiment
    daily_timeline_pos = helper.daily_timeline(selected_users, data, 1)
    fig.add_trace(go.Scatter(x=daily_timeline_pos['only_date'], y=daily_timeline_pos['message'], mode='lines', name='Positive', marker=dict(color='green')))

    # Add trace for Neutral sentiment
    daily_timeline_neu = helper.daily_timeline(selected_users, data, 0)
    fig.add_trace(go.Scatter(x=daily_timeline_neu['only_date'], y=daily_timeline_neu['message'], mode='lines', name='Neutral', marker=dict(color='grey')))

    # Add trace for Negative sentiment
    daily_timeline_neg = helper.daily_timeline(selected_users, data, -1)
    fig.add_trace(go.Scatter(x=daily_timeline_neg['only_date'], y=daily_timeline_neg['message'], mode='lines', name='Negative', marker=dict(color='red')))

    # Update layout
    fig.update_layout(xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), title='Daily Timeline', xaxis_title='Date', yaxis_title='Number of Messages')

    st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True)

    # Monthly timeline
    st.subheader('Monthly Timeline')
    fig = go.Figure()

    # Monthly timeline for Positive sentiment
    timeline_positive = helper.monthly_timeline(selected_users, data, 1)
    fig.add_trace(go.Scatter(x=timeline_positive['time'], y=timeline_positive['message'], mode='markers', name='Positive', marker=dict(color='green')))

    # Monthly timeline for Neutral sentiment
    timeline_neutral = helper.monthly_timeline(selected_users, data, 0)
    fig.add_trace(go.Scatter(x=timeline_neutral['time'], y=timeline_neutral['message'], mode='markers', name='Neutral', marker=dict(color='grey')))

    # Monthly timeline for Negative sentiment
    timeline_negative = helper.monthly_timeline(selected_users, data, -1)
    fig.add_trace(go.Scatter(x=timeline_negative['time'], y=timeline_negative['message'], mode='markers', name='Negative', marker=dict(color='red')))

    # Update layout
    fig.update_layout(xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), title='Monthly Timeline', xaxis_title='Time', yaxis_title='Number of Messages')

    st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True)



    # Percentage contributed
    if selected_users == 'Overall' or selected_option == 'Selected':
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader('Most Positive Contributions')
            x = helper.percentage(data, selected_users, 1)
            
            # Displaying
            st.dataframe(x)
        with col2:
            st.subheader('Most Neutral Contributions')
            y = helper.percentage(data, selected_users, 0)
            
            # Displaying
            st.dataframe(y)
        with col3:
            st.subheader('Most Negative Contributions')
            z = helper.percentage(data, selected_users, -1)
            
            # Displaying
            st.dataframe(z)


    # Most Positive,Negative,Neutral User...
    if selected_users == 'Overall' or selected_option == 'Selected':

        if isinstance(selected_users,list):
            df = data[data['user'].isin(selected_users)]
        else:
            df=data
        
        # Merge the data for each sentiment category
        positive_users = df['user'][df['value'] == 1].value_counts().head(10)
        neutral_users = df['user'][df['value'] == 0].value_counts().head(10)
        negative_users = df['user'][df['value'] == -1].value_counts().head(10)

        # Create a single DataFrame containing all users and their counts for each sentiment
        merged_data = pd.concat([positive_users, neutral_users, negative_users], axis=1)
        merged_data.columns = ['Positive', 'Neutral', 'Negative']
        merged_data.fillna(0, inplace=True)

        # Plot the stacked bar chart
        fig = go.Figure()

        # Add trace for Positive users
        fig.add_trace(go.Bar(x=merged_data.index, y=merged_data['Positive'], name='Positive', marker_color='green'))

        # Add trace for Neutral users
        fig.add_trace(go.Bar(x=merged_data.index, y=merged_data['Neutral'], name='Neutral', marker_color='grey'))

        # Add trace for Negative users
        fig.add_trace(go.Bar(x=merged_data.index, y=merged_data['Negative'], name='Negative', marker_color='red'))

        # Update layout
        fig.update_layout(barmode='stack',
                        xaxis=dict(fixedrange=True),
                        yaxis=dict(fixedrange=True),
                        title='Users Distribution by Sentiment',
                        xaxis_title='Users',
                        yaxis_title='Number of Messages')

        # Display the stacked bar chart
        st.plotly_chart(fig, config={'displaylogo': False}, use_container_width=True)


    # WORDCLOUD......
    col1,col2,col3 = st.columns(3)
    with col1:
        try:
            # heading
            st.subheader('Positive WordCloud')
            
            # Creating wordcloud of positive words
            df_wc = helper.create_wordcloud(selected_users, data,1)
            fig = go.Figure(go.Image(z=df_wc))
            fig.update_layout(height=400, width=400)
            st.plotly_chart(fig, config={'displaylogo': False})
        except:
            # Display error message
            st.image('error.webp')
    with col2:
        try:
            # heading
            st.subheader('Neutral WordCloud')
            
            # Creating wordcloud of neutral words
            df_wc = helper.create_wordcloud(selected_users, data,0)
            fig = go.Figure(go.Image(z=df_wc))
            fig.update_layout(height=400, width=400)
            st.plotly_chart(fig, config={'displaylogo': False})
        except:
            # Display error message
            st.image('error.webp')
    with col3:
        try:
            # heading
            st.subheader('Negative WordCloud')
            
            # Creating wordcloud of negative words
            df_wc = helper.create_wordcloud(selected_users, data,-1)
            fig = go.Figure(go.Image(z=df_wc))
            fig.update_layout(height=400, width=400)
            st.plotly_chart(fig, config={'displaylogo': False})
        except:
            # Display error message
            st.image('error.webp')

    # # Most common positive words
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     try:
    #         # Data frame of most common positive words.
    #         most_common_df = helper.most_common_words(selected_users, data,1)
            
    #         # heading
    #         st.subheader('Positive Words')
    #         fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='green'))
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         # Disply error image
    #         st.image('error.webp')
    # with col2:
    #     try:
    #         # Data frame of most common neutral words.
    #         most_common_df = helper.most_common_words(selected_users, data,0)
            
    #         # heading
    #         st.subheader('Neutral Words')
    #         fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='grey'))
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         # Disply error image
    #         st.image('error.webp')
    # with col3:
    #     try:
    #         # Data frame of most common negative words.
    #         most_common_df = helper.most_common_words(selected_users, data,-1)
            
    #         # heading
    #         st.subheader('Negative Words')
    #         fig = go.Figure(go.Bar(y=most_common_df[0], x=most_common_df[1], orientation='h', marker_color='red'))
    #         fig.update_layout(height=400, width=600)
    #         st.plotly_chart(fig, config={'displaylogo': False})
    #     except:
    #         # Disply error image
    #         st.image('error.webp')

st.set_page_config(layout="wide")

# Main heading
st.markdown("<h1 style='text-align: center; color: grey;'>ChatViz</h1>", unsafe_allow_html=True)
# VADER : is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments.
nltk.download('vader_lexicon')
# File upload button
uploaded_file = st.file_uploader("Choose a Whatsapp chat .txt file")

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
    
    # Dropdown for selecting analysis with respect to
    selected_option = st.selectbox("Show analysis with respect to", ["Overall", "Selected"] + user_list)
    selected_users = st.multiselect("Select users for analysis", user_list) if selected_option == "Selected" else selected_option

    # Organize buttons and graphs in columns
    button_col1, button_col2 = st.columns(2)

    # Show "Stats" button in the second column
    if button_col1.button("Stats (Basic stats analysis)"):
        helper.show_basic_analysis(data, selected_users)

    # Show "Behaviours" button in the first column
    if button_col2.button("Behaviours (Sentiments analysis)"):
        display_behaviours_analysis(data, selected_users)


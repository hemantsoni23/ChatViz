import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import regex
import pandas as pd
import numpy as np
import emoji
import plotly.express as px
import plotly.io as pio
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
import csv

app = Flask(__name__)
app.secret_key = 'hemant_soni'
app.static_folder = 'static'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            convert_txt_to_csv(file_path)
            csv_file_path = os.path.splitext(file_path)[0] + '.csv'
            session['csv_file_path'] = csv_file_path
            return redirect(url_for('analysis'))

    return render_template('upload.html')

@app.route('/analysis')
def analysis():
    csv_file_path = session.get('csv_file_path', None)

    if not csv_file_path:
        flash('No chat file found. Please upload a file first.')
        return redirect(url_for('upload'))
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    data = perform_analysis(df)
    df = df[(df['Time'] != 'System') & (df['Date'].str.match(r'\d{2}/\d{2}/\d{2}'))]
    df.drop(df[df.Author == 'WhatsApp'].index , inplace=True)
    df['Time'] = df['Time'].str.replace('\u202F', ' ')
    df = df[df['Message'].apply(lambda x: isinstance(x, str))]
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df['Month_Year'] = df['Date'].dt.strftime('%Y-%m')
    df['Month'] = df['Date'].dt.strftime('%b')
    df['Date'] = df['Date'].dt.date
    chart_data_1 = df.groupby(['Month_Year', 'Author']).size().reset_index(name='Count')
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p')
    df['Hour'] = df['Time'].dt.hour
    df['AMPM'] = df['Time'].dt.strftime('%p')
    chart_data_2 = df.groupby(['Hour', 'AMPM', 'Author']).size().reset_index(name='Count')
    chart_data_3 = df.groupby('Author')['Message'].count().reset_index(name='Count')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Weekday'] = df['Date'].dt.weekday
    chart_data_4 = df.groupby(['Weekday', 'Author'])['Message'].count().reset_index()

    return render_template('result.html', chart_data_1=chart_data_1.to_dict(orient='records'), chart_data_2=chart_data_2.to_dict(orient='records'),chart_data_3=chart_data_3.to_dict(orient='records'),chart_data_4=chart_data_4.to_dict(orient='records'),analysis_result = data)

def convert_txt_to_csv(txt_file_path):
    data = []
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parts = re.split(r', ', line.strip(), maxsplit=1)

        if len(parts) > 1:
            date = parts[0]
            time_message = parts[1]

            time_message_parts = time_message.split(' - ')
            if len(time_message_parts) > 1:
                time = time_message_parts[0]
                message = time_message_parts[1]
            else:
                time = "System" 
                message = time_message_parts[0]

            if ':' in message:
                author, message = message.split(':', 1)
                author = author.strip()  
                message = message.strip() 
            else:
                author = "WhatsApp"  
                message = message.strip()  

            data.append([date, time, author, message])

    csv_file_path = os.path.splitext(txt_file_path)[0] + '.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Time', 'Author', 'Message'])  # Write header
        writer.writerows(data)
    
    os.remove(txt_file_path)

def perform_analysis(df):
    df = df[(df['Time'] != 'System') & (df['Date'].str.match(r'\d{2}/\d{2}/\d{2}'))]
    df.drop(df[df.Author == 'WhatsApp'].index , inplace=True)
    df = df[(df['Time'] != 'System') & (df['Date'].str.match(r'\d{2}/\d{2}/\d{2}'))]

    message_from_whatsapp = df[df["Author"] == 'WhatsApp'].shape[0]
    total_message = df.shape[0]
    media_messages = df[df["Message"] == '<Media omitted>'].shape[0]
    media_messages_df = df[df['Message'] == '<Media omitted>']
    df['Time'] = df['Time'].str.replace('\u202F', ' ')
    df = df[df['Message'].apply(lambda x: isinstance(x, str))]

    def split_count(text):
        emoji_list = []
        data = regex.findall(r'\X', text)
        for word in data:
            if any(char in emoji.EMOJI_DATA for char in word):
                emoji_list.append(word)
        return emoji_list

    df['emoji'] = df["Message"].apply(split_count)

    emojis = sum(df['emoji'].str.len())
    URL_PATTERN = r'(https?://\S+)'

    df['urlcount'] = df.Message.apply(lambda x: len(re.findall(URL_PATTERN, x)))

    links = np.sum(df.urlcount)

    authors = list(df.Author.unique())
    author_stats = []
    for author in authors:
        if author != 'WhatsApp':
            req_df = df[df["Author"] == author]
            req_df['Word_Count'] = req_df['Message'].apply(lambda s: len(s.split(' ')))
            author_stat = {
                'Author': author,
                'Messages Sent': req_df.shape[0],
                'Average Words per Message': np.mean(req_df['Word_Count']), 
                'Media Messages Sent': media_messages_df[media_messages_df['Author'] == author].shape[0],
                'Emojis Sent': sum(req_df['emoji'].str.len()),
                'Links Sent': sum(req_df["urlcount"])
            }
            author_stats.append(author_stat)
    chat_stats = {
        'Total Messages': total_message,
        'Number of Media Shared': media_messages,
        'Number of Emojis Shared': emojis,
        'Number of Links Shared': links,
        'Author Stats': author_stats
    }
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df['Month_Year'] = df['Date'].dt.strftime('%Y-%m')
    df['Month'] = df['Date'].dt.strftime('%b')
    df['Date'] = df['Date'].dt.date
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p')
    # print('next',df)

    longest_message_index = df['Message'].str.len().idxmax()
    longest_message = df.loc[longest_message_index, 'Message']
    author_of_longest_message = df.loc[longest_message_index, 'Author']
    length_of_longest_message = len(longest_message)

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.sort_values(by='Date')

    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_diff = max_date - min_date
    total_years = date_diff.days // 365
    total_months = (date_diff.days % 365) // 30
    total_days = date_diff.days % 30


    most_active_day = df.groupby(df['Date'].dt.date)['Author'].count().idxmax()
    most_active_month = df.groupby(df['Date'].dt.to_period('M'))['Author'].count().idxmax()
    most_active_year = df.groupby(df['Date'].dt.to_period('Y'))['Author'].count().idxmax()

    chat_stats.update({
        'Author of the Longest Message': author_of_longest_message,
        'Length of the Longest Message': length_of_longest_message,
        'Longest Message': longest_message,
        'Total Years': total_years,
        'Total Months': total_months,
        'Total Days': total_days,
        'Most Active Day': most_active_day,
        'Most Active Month': most_active_month,
        'Most Active Year': most_active_year
    })

    return chat_stats

if __name__ == '__main__':
    app.run(debug=True)


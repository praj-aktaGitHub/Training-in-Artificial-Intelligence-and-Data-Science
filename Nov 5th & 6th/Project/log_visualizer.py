import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from collections import Counter
from analyzer import parse_log  # Import parse_log from analyzer.py
import streamlit as st  # For displaying plots in Streamlit

# Ensure the correct backend for Matplotlib is set to 'TkAgg'
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg for interactive plotting

def visualize_logs(log_content):
    """
    Function to generate visualizations from log content.
    """
    logs = parse_log(log_content)
    log_df = pd.DataFrame(logs)

    # Ensure timestamp is in datetime format
    if 'timestamp' in log_df.columns:
        log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
    else:
        print("Timestamp column is missing.")
        return

    # 1. Visualization: Timeline of Events using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(log_df['timestamp'], [1] * len(log_df), marker='o', linestyle='', color='b', alpha=0.5)
    plt.title("Timeline of Events")
    plt.xlabel("Time")
    plt.ylabel("Events")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)  # Display Matplotlib plot in Streamlit

    # 2. Visualization: Error Frequency Over Time using Matplotlib
    error_df = log_df[log_df['level'] == 'ERROR']
    error_freq = error_df.groupby(error_df['timestamp'].dt.date).size()

    plt.figure(figsize=(10, 6))
    error_freq.plot(kind='bar', color='red')
    plt.title("Error Frequency Over Time")
    plt.xlabel("Date")
    plt.ylabel("Frequency of Errors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)  # Display Matplotlib plot in Streamlit

    # # 3. Visualization: Distribution of Log Levels using Seaborn
    # plt.figure(figsize=(8, 6))
    # sns.countplot(data=log_df, x='level', palette='viridis')
    # plt.title("Distribution of Log Levels")
    # plt.xlabel("Log Level")
    # plt.ylabel("Frequency")
    # plt.tight_layout()
    # st.pyplot(plt)  # Display Seaborn plot in Streamlit

    # 4. Visualization: Graphical Representation of Errors using Matplotlib
    error_messages = ' '.join(error_df['message'])
    error_counts = Counter(error_messages.split())
    most_common_errors = error_counts.most_common(10)

    error_words = [error[0] for error in most_common_errors]
    error_word_counts = [error[1] for error in most_common_errors]

    plt.figure(figsize=(10, 6))
    plt.barh(error_words, error_word_counts, color='orange')
    plt.title("Most Frequent Errors in Logs")
    plt.xlabel("Frequency")
    plt.ylabel("Error Message")
    plt.tight_layout()
    st.pyplot(plt)  # Display Matplotlib plot in Streamlit

    # 5. Interactive: Timeline of Events using Plotly
    fig = px.scatter(log_df, x='timestamp', y=[1] * len(log_df), title="Interactive Timeline of Events")
    fig.update_layout(xaxis_title="Time", yaxis_title="Events")
    st.plotly_chart(fig)  # Display Plotly chart in Streamlit

    # 6. Interactive: Error Frequency Over Time using Plotly
    fig = px.bar(error_freq.reset_index(), x='timestamp', y=0, title="Interactive Error Frequency Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Frequency of Errors")
    st.plotly_chart(fig)  # Display Plotly chart in Streamlit

    # # 7. Interactive: Distribution of Log Levels using Plotly
    # fig = px.pie(log_df, names='level', title="Distribution of Log Levels")
    # st.plotly_chart(fig)  # Display Plotly chart in Streamlit

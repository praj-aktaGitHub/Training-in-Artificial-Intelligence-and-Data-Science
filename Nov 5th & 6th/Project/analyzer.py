import re
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Importing ChatOpenAI from langchain_openai

# Load environment variables from .env file
load_dotenv()

# OpenRouter API key and base URL
api_key = os.getenv("OPENROUTER_API_KEY")  # Get the OpenRouter API key
base_url = "https://openrouter.ai/api/v1"  # Base URL for OpenRouter

# Set up the Langchain OpenAI model (via OpenRouter)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",  # Example: meta-llama/llama-3-8b-instruct model
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,  # Use the OpenRouter API key
    base_url=base_url,  # Use the OpenRouter base URL
)


def parse_log(log: str):
    """
    Parses the log into structured components like timestamp, log level, thread, and message.
    Assumes logs follow the format: 'YYYY-MM-DD HH:MM:SS LOG_LEVEL [thread] MESSAGE'
    """
    log_entries = []

    # Regex pattern to capture timestamp, log level, thread, and message
    log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s([A-Z]+)\s\[(.*?)\]\s(.*)"

    # Find all matches
    matches = re.findall(log_pattern, log)

    # Debugging: Print matches and log entries to see if timestamp is being extracted
    if matches:
        print(f"Found {len(matches)} matches")
        print(f"Sample match: {matches[0]}")
    else:
        print("No matches found.")

    for match in matches:
        timestamp, level, thread, message = match
        log_entries.append({
            'timestamp': timestamp,
            'level': level,
            'thread': thread,
            'message': message
        })

    # Debugging: Show the parsed entries
    print(f"Parsed Log Entries: {log_entries}")
    return log_entries


def analyze_log(log: str):
    """
    This function analyzes the provided log file and returns detailed actionable insights.
    The log is cleaned and processed using the OpenRouter API and LLaMA model.
    """
    parsed_log = parse_log(log)

    # Categorize logs based on their level (INFO, ERROR, DEBUG)
    categorized_logs = {'INFO': [], 'ERROR': [], 'DEBUG': []}

    for entry in parsed_log:
        level = entry['level']
        if level in categorized_logs:
            categorized_logs[level].append(entry)

    # Convert categorized logs to a readable format
    categorized_log_str = ""
    for level, logs in categorized_logs.items():
        categorized_log_str += f"\n\n--- {level} Logs ---\n"
        for log in logs:
            categorized_log_str += f"{log['timestamp']} - {log['message']}\n"

    # Now you can proceed with generating insights and summaries based on the categorized logs
    prompt = f"Analyze the following log file and provide insights based on the categorized data:\n{categorized_log_str}"

    insights = llm.invoke(prompt)
    summarized_insights = summarize_insights(insights)
    fix_suggestions = suggest_fixes(insights)

    return insights.content, summarized_insights, fix_suggestions


def summarize_insights(insights: str) -> str:
    """
    This function generates a summary of the insights provided to make them more concise and easy to act on.
    """
    prompt = f"Summarize the following actionable insights into a concise list of key points for quick action:\n{insights}"

    summary = llm.invoke(prompt)  # Get summarized insights
    return summary.content


def suggest_fixes(insights: str) -> str:
    """
    This function generates quick fix suggestions for the insights based on the issues identified in the log.
    """
    prompt = f"Based on the following actionable insights, provide detailed and technical quick fix suggestions for each issue:\n{insights}"

    suggestions = llm.invoke(prompt)  # Get quick fixes suggestions
    return suggestions.content

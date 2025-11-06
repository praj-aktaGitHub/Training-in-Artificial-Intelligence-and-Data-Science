import streamlit as st
from analyzer import analyze_log, parse_log
from log_visualizer import visualize_logs

# Set the Streamlit page layout
st.set_page_config(page_title="AI Log Analyzer", layout="centered")

# Inject custom CSS into the Streamlit app for styling
st.markdown(
    """
    <style>
        /* Background color of the entire app */
        body {
            background-color: #f0f0f0;  /* Light grey background */
        }

        /* Custom Sidebar Styling */
        .css-1d391kg {
            background-color: #f7d0a1;  /* Light orange background for sidebar */
            border-radius: 12px;         /* Rounded corners for sidebar */
            padding: 20px;               /* Padding inside sidebar */
            box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1); /* Shadow effect */
        }

        /* Sidebar Title Styling */
        .css-1d391kg .stSidebar > header {
            font-size: 28px;
            font-weight: bold;
            color: #0073e6;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Logo Styling */
        .css-1d391kg .stSidebar img {
            max-width: 100%;
            height: auto;
            margin-bottom: 20px;
        }

        /* Button Styling (Remove background and make it look like a "Browse" button) */
        .stButton>button {
            background-color: transparent; /* Remove background color */
            border: 2px solid #0073e6;      /* Blue border to make it look like a button */
            color: #0073e6;                 /* Blue text color */
            border-radius: 8px;             /* Rounded corners */
            padding: 12px 24px;
            font-size: 16px;
            width: 100%;
        }

        /* Button Hover Effect */
        .stButton>button:hover {
            background-color: #f7f7f7;     /* Light hover background */
            border-color: #005bb5;         /* Darker border on hover */
            color: #005bb5;                 /* Darker text color on hover */
        }

        /* Custom Sidebar Radio Button Styling */
        .css-1d391kg .stRadio label {
            font-weight: bold;
            color: #0073e6; /* Text color for radio buttons */
        }

        .css-1d391kg .stRadio div {
            background-color: #ffffff; /* Background for radio buttons */
            border-radius: 8px;         /* Rounded corners for radio buttons */
            padding: 10px;              /* Padding around radio buttons */
        }

        .css-1d391kg .stRadio div:hover {
            background-color: #e6f7ff; /* Hover effect */
        }

    </style>
    """, unsafe_allow_html=True
)

# Sidebar Setup with Custom Styling
st.sidebar.title("Your Space")

# Add an app logo from an assets folder (place the logo image in the "assets" folder)
st.sidebar.image("assets/your_logo.png", width=150)

# Sidebar options with custom radio buttons
sidebar_option = st.sidebar.radio(
    "Choose an action",
    ["Upload Log", "Instructions", "About"],
    format_func=lambda x: f"🚀 {x}" if x == "Upload Log" else f"📝 {x}" if x == "Instructions" else f"ℹ️ {x}"
)

# Title for the web app
st.title("🤖📈AI-Powered Log Analyzer")

# Show different content based on sidebar selection
if sidebar_option == "Upload Log":
    # Description
    st.write("""
        Upload a log file and let AI analyze it for errors, performance issues, and actionable insights.
        The analysis will be performed using OpenRouter's LLaMA model.
    """)

    # File upload section
    uploaded_file = st.file_uploader("Upload a log file", type=["txt", "log"])

    # Initialize session state variables
    if 'insights' not in st.session_state:
        st.session_state['insights'] = ""
    if 'summarized_insights' not in st.session_state:
        st.session_state['summarized_insights'] = ""
    if 'parsed_logs' not in st.session_state:
        st.session_state['parsed_logs'] = []

    # If the file is uploaded, process the file and analyze it
    if uploaded_file is not None:
        # Read the content of the uploaded log file
        log_content = uploaded_file.read().decode("utf-8")

        # Display the log content
        st.subheader("Log Content")
        st.text_area("Log", log_content, height=300)

        # Analyze the log file content using the analyzer
        if st.button("Analyze Log"):
            with st.spinner("Analyzing... Please wait."):
                # Get actionable insights, summarized insights, and parsed logs
                insights, summarized_insights, _ = analyze_log(log_content)

                # Store the parsed logs and insights in session state
                parsed_logs = parse_log(log_content)  # Parse the log content
                st.session_state['parsed_logs'] = parsed_logs  # Store parsed logs
                st.session_state['insights'] = insights  # Detailed actionable insights
                st.session_state['summarized_insights'] = summarized_insights  # Concise key points
                st.success("Log analyzed successfully!")

        # Display Detailed Actionable Insights
        if st.session_state['insights']:
            st.subheader("Detailed Actionable Insights")
            st.write(st.session_state['insights'])

        # Display Summarized Insights (key points)
        if st.session_state['summarized_insights']:
            st.subheader("Summarized Insights (Key Points)")
            st.write(st.session_state['summarized_insights'])

        # Trigger Visualization
        if st.button("Visualize Logs"):
            with st.spinner("Generating visualizations..."):
                visualize_logs(log_content)
                st.success("Visualizations generated successfully!")

elif sidebar_option == "Instructions":
    st.header("How to Use")
    st.write("""
        1. **Upload a Log File**: Click on the "Upload Log" option to upload a log file.
        2. **Analyze Log**: Click the "Analyze Log" button to get detailed actionable insights from the log file.
        3. **Visualize Logs**: Click the "Visualize Logs" button to generate visual representations of the log data.
    """)

elif sidebar_option == "About":
    st.header("About this App")
    st.write("""
        This AI-powered log analyzer helps developers quickly identify errors, performance bottlenecks, and actionable insights from log files.
        The app uses OpenRouter's LLaMA model to process the log files and generates visualizations for a better understanding of the log data.
    """)

import gradio as gr
from transformers import pipeline

# Load sentiment analysis pipeline
classifier = pipeline("sentiment-analysis")

# Function to classify sentiment
def analyze_sentiment(text):
    result = classifier(text)[0]
    label = result['label']
    score = result['score']
    emoji = "🌈😊" if label == "POSITIVE" else "💔😠"
    color = "#f8bbd0" if label == "POSITIVE" else "#880E4F"
    return f"<div style='color:{color}; font-size: 24px; font-weight: bold;'>{emoji} {label}<br><span style='font-size:18px;'>Confidence: {score:.2f}</span></div>"

# Custom CSS with pink background and hover effect
custom_css = """
body {
    background-color: #f8bbd0; /* baby pink */
    font-family: 'Segoe UI', sans-serif;
}
.gradio-container {
    max-width: 700px;
    margin: auto;
    padding-top: 40px;
}
textarea {
    font-size: 18px !important;
    border-radius: 10px !important;
    border: 2px solid #f48fb1 !important;
}
.output-html {
    padding: 20px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
}
h1, .title {
    color: #d81b60 !important;
    font-weight: 700;
}
button {
    background-color: #d81b60 !important; /* dark pink */
    color: white !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    padding: 10px 20px !important;
    transition: background-color 0.3s ease;
}
button:hover {
    background-color: #ad1457 !important; /* darker pink on hover */
}
"""

# Create Gradio interface
demo = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(lines=3, placeholder="Type your sentence here...", label="💬 Your Text"),
    outputs=gr.HTML(label="✨ Sentiment Result"),
    title="💖Sentiment Classifier",
    description="Enter a sentence and get instant vibes — powered by Hugging Face 🤗 and Gradio ✨",
    css=custom_css
)

# Launch the app
demo.launch()

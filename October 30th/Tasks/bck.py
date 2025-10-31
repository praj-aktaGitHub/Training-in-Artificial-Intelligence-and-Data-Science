import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# Prompt for sentiment analysis
prompt_sentiment_analysis = ChatPromptTemplate.from_template(
    "<s>[INST] Analyze the sentiment of the following feedback. "
    "If the sentiment is positive, return 'positive'. If the sentiment is negative, return 'negative'. "
    "Feedback: {feedback} [/INST]"
)

# Prompt to generate a response for positive feedback
prompt_positive_sentiment_response = ChatPromptTemplate.from_template(
    "<s>[INST] Given the positive sentiment in the feedback, generate a thank you response to the user. dont give your faithfully/regards and all that  give just message  "
    "Feedback: {feedback} [/INST]"
)

# Prompt to generate a response for negative feedback
prompt_negative_sentiment_response = ChatPromptTemplate.from_template(
    "<s>[INST] Given the negative sentiment in the feedback, generate an apology response. "
    "Also, analyze the tone of the feedback (e.g., frustrated, neutral, disappointed) and respond accordingly  dont give your faithfully/regards and all that give just message "
    "Feedback: {feedback} [/INST]"
)

parser = StrOutputParser()


def get_sentiment(feedback: str, conversation_history: str) -> str:
    """Get the sentiment of the feedback (positive/negative) considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_sentiment_analysis | llm | parser
    sentiment = chain.invoke(conversation_input)
    return sentiment.strip().lower()


def positive_sentiment_response_generator(feedback: str, conversation_history: str) -> str:
    """Generate a thank-you response for positive feedback considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_positive_sentiment_response | llm | parser
    response = chain.invoke(conversation_input)
    return response.strip()


def negative_sentiment_response_generator(feedback: str, conversation_history: str) -> str:
    """Generate an apology response for negative feedback considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_negative_sentiment_response | llm | parser
    response = chain.invoke(conversation_input)
    return response.strip()


def conversation():
    conversation_history = ""  # To keep track of previous feedback and responses
    print("Welcome to the feedback assistant. Please provide your feedback.")

    while True:
        # Collecting feedback from user
        feedback = input("\nPlease provide your feedback (type 'exit' to quit): ")

        if feedback.lower() == "exit":
            print("Thank you for using the Feedback Assistant!")
            break

        # Analyze sentiment of the feedback, including conversation history
        sentiment = get_sentiment(feedback, conversation_history)

        if sentiment == "positive":
            response = positive_sentiment_response_generator(feedback, conversation_history)
        elif sentiment == "negative":
            response = negative_sentiment_response_generator(feedback, conversation_history)
        else:
            response = "Sorry, I couldn't understand the sentiment of your feedback."

        print("\nResponse to Your Feedback: ")
        print(response)

        # Update conversation history (feedback + response)
        conversation_history += f"User: {feedback}\nAssistant: {response}\n"


if __name__ == "__main__":
    conversation()

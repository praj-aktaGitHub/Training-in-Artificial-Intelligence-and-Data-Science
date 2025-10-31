import os
import requests
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from litellm import completion

# Load environment variables
load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
llm_api_key = os.getenv("OPENAI_API_KEY")


def litellm_wrapper(prompt: str) -> str:
    response = completion(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    return response["choices"][0]["message"]["content"]

# Step 1: Define the Weather Agent
weather_agent = Agent(
    role="Weather Analyst",
    goal="Provide accurate weather information for any city",
    backstory="You are a weather expert who uses OpenWeatherMap API to fetch real-time data.",
    verbose=False
)

# Step 2: Define the Weather Task
def get_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"❌ Couldn't find weather for '{city}'. Try another city."
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return f"🌡️ {temp}°C, {condition.capitalize()}, 💧 Humidity: {humidity}%, 🌬️ Wind: {wind} m/s"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# Step 3: Ask user for city
print("\n=== 🌦️ CrewAI Weather Bot ===")
while True:
    city = input("Which city do you want the weather for? ").strip()
    if city.lower() == "exit":
        print("Bot: Stay safe out there ☔")
        break
    print("Bot:", get_weather(city))


# Step 4: Create Task
weather_task = Task(
    description=f"Get the current weather for {city}.",
    agent=weather_agent,
    expected_output="A friendly weather summary for the user."
)

# Step 5: Create Crew and run
crew = Crew(
    agents=[weather_agent],
    tasks=[weather_task]
)

# Step 6: Run Crew and print result
print("\nBot:", get_weather(city))

import os
from dotenv import load_dotenv
from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


llm_config = {
    "config_list": [
        {
            "model": "gpt-3.5-turbo", # or "gpt-4"
#"model": "mistralai/mistral-7b-instruct",
            "api_key": api_key,
            "base_url": "https://openrouter.ai/api/v1",
            "price":[0.25, 0.25]
        }
    ]
}



researcher = AssistantAgent(
    name="Researcher",
    system_message="You are a skilled researcher. Search the web and gather relevant information.",
    llm_config=llm_config

)


summarizer = AssistantAgent(
    name="Summarizer",
    system_message="You are a concise summarizer. Summarize the research findings clearly and briefly.",
    llm_config=llm_config

)


notifier = AssistantAgent(
    name="Notifier",
    system_message="You are a notifier. Print the final summary to the console and save it to a file.",
    llm_config=llm_config

)


user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False
)


group_chat = GroupChat(
    agents=[user_proxy, researcher, summarizer, notifier],
    messages=[],
    max_round=50
)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)


user_proxy.initiate_chat(
    manager,
    message="Find recent advancements in quantum computing and summarize them."
)


def save_to_file(content):
    with open("summary_output.txt", "w", encoding="utf-8") as f:
        f.write(content)


final_output = group_chat.messages[-1]["content"]
print("\nFinal Summary:\n", final_output)
save_to_file(final_output)

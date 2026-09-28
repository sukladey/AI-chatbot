import warnings 
import logging 
# Hide warnings and library logs 
warnings.filterwarnings("ignore") 
logging.getLogger().setLevel(logging.ERROR)


from dotenv import load_dotenv 

load_dotenv() 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

model = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash"
)

print("Choose your AI mode")
print("Press 1 for Angry mode")
print("Press 2 for Funny mode")
print("Press 3 for Sad mode")

choice = int(input("Tell your response : "))

if choice == 1:
    mode = "You are an angry agent. You responsed aggressively and impatiently."
elif choice == 2:
    mode = "You are very funny AI agent."
else:
    mode = "You are Sad AI agent."

messages = [
    SystemMessage(content=mode)

]

print("---------- Welcome enter 0 to exit the application ----------")
while True:
    prompt = input("You : ")

    if prompt == "0":
        break
    messages.append(HumanMessage(content=prompt))

    try:
        result = model.invoke(messages)
        messages.append(AIMessage(content=result.content[0]["text"]))

        print("Bot : ", result.content[0]["text"])
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Bot : API quota exceeded. Please try again later.")

        else:
            print("Bot : Something went wrong.")

print(messages)

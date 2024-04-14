#loading the library
import os
from dotenv import load_dotenv
import google.generativeai as genai
# from swarms.models import Gemini

#loading the API key
load_dotenv()

API_KEY = os.getenv('API_KEY')
genai.configure(
    api_key=API_KEY
)

#creating a chatbot

model = genai.GenerativeModel('gemini-pro')

history = []  
chat = model.start_chat(history=history)
selected_language = ''
#checking if the question is related to agriculture
def is_agriculture_related(question):
    question_lower = question.lower()
    all_keywords = []
    with open(r"C:\Users\Prerna\Desktop\agri_chatbot\django_chatbot\chat\keywords.py", 'r') as file:
        for line in file:
            keywords = line.strip().split(',')  # Assuming keywords are comma-separated
            all_keywords.extend(keywords)

    for keyword in all_keywords:
        if keyword in question_lower:
            return True

def chatbot_call(selected_language, message):
    # max_words = 100
   
        
    print(message)

    if selected_language == 'English':
        instruction = ["Talk in english","My name is Agribot","I am trained by Prerna Arya","I am agriculture expert"]
    elif selected_language == 'Hindi':
        instruction = ["हिंदी में बात करें", "मेरा नाम एग्रीबॉट है", "मैं प्रेरणा आर्य द्वारा प्रशिक्षित हूं", "मैं कृषि विशेषज्ञ हूं"]
    else:
        print("selected language is not defined")
        instruction = ["Talk in english","My name is Agribot","I am trained by Prerna Arya","I am agriculture expert"]


    if message.strip() == " ":
        return f"Please enter a valid message."
    

    if not is_agriculture_related(message):
        return f"I'm here to assist you with agriculture-related queries. Unfortunately, I'm unable to provide an answer to this message as it's outside my domain."
        
    #adding the message to the history
    history.append({"user":message})


    response = chat.send_message(message + str(instruction))
    print(response)
    response_words = response.text.split()

    final_response = " ".join(response_words)
    # final_response = final_response.replace("*","")
    final_response = final_response.replace("**","\n")
    # gemini.max_tokens = 150 
    print(final_response)
   
    #adding the response to the history
    history.append({"Bot":final_response})
    
    return final_response





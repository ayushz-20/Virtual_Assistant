from Frontend.GUI import(
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetAssistantStatus,
    GetMicrophoneStatus)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import sys
import time
import logging
from cohere import Client as CohereClient
from groq import Groq
from huggingface_hub import HfApi
from dotenv import load_dotenv
import re
from Backend.ImageGeneration import generate_images_and_open

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open","close","play","system","content","google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r'Data\Chatlog.json',"r",encoding='utf-8')
    if len(File.read())<5:
        with open(TempDirectoryPath('Database.data'),'w',encoding='utf-8') as file:
            file.write("")
            
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)
            
            
def ReadChatLogJson():
    with open(r'Data\Chatlog.json', 'r' , encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data :
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] =="assistant":
            formatted_chatlog += f"User: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")
    
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))
        
def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'), "r", encoding='utf-8')
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8')
        File.write(result)
        File.close()
        
def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()
    
InitialExecution()

def test_api_connections():
    load_dotenv()
    api_status = {
        "cohere": False,
        "groq": False,
        "huggingface": False
    }
    
    # Test Cohere API
    try:
        cohere = CohereClient(os.getenv("CohereAPIKey"))
        response = cohere.generate(prompt="Test", max_tokens=5)
        api_status["cohere"] = True
        logger.info("Cohere API: Connected")
    except Exception as e:
        logger.error(f"Cohere API Error: {e}")

    # Test Groq API
    try:
        groq_client = Groq(api_key=os.getenv("GroqAPIKey"))
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": "Test"}],
            model="mixtral-8x7b-32768"
        )
        api_status["groq"] = True
        logger.info("Groq API: Connected")
    except Exception as e:
        logger.error(f"Groq API Error: {e}")

    # Test HuggingFace API
    try:
        hf = HfApi(token=os.getenv("HuggingFaceAPIKey"))
        hf.whoami()
        api_status["huggingface"] = True
        logger.info("HuggingFace API: Connected")
    except Exception as e:
        logger.error(f"HuggingFace API Error: {e}")

    return api_status

# Add this after InitialExecution()
api_status = test_api_connections()
if not all(api_status.values()):
    logger.warning("Some APIs failed to connect. Check logs for details.")

def classify_query(query: str) -> str:
    query = query.lower().strip()
    
    patterns = {
        'realtime': [
            r'(news|weather|latest|current)',
            r'(price|stock|market|trending)',
            r'(today|now|update|recent)',
            r'(who is|where is|what is.*doing)',
        ],
        'command': [
            r'^(open|close|play|stop)',
            r'^(search|generate|remind)',
            r'^(system|volume|mute)',
        ],
        'exit': [
            r'(bye|goodbye|exit|quit|close)',
        ]
    }
    
    # Check realtime patterns
    for pattern in patterns['realtime']:
        if re.search(pattern, query):
            return 'realtime'
            
    # Check command patterns
    for pattern in patterns['command']:
        if re.search(pattern, query):
            return 'command'
            
    # Check exit patterns
    for pattern in patterns['exit']:
        if re.search(pattern, query):
            return 'exit'
            
    return 'general'  # Default case

def split_complex_query(query: str) -> list:
    """Split query with multiple commands"""
    commands = []
    parts = query.split(" and ")
    
    for part in parts:
        part = part.strip()
        if "generate" in part:
            prompt = part[part.find("generate"):].strip()
            commands.append(prompt)
        elif "what is the time" in part:
            commands.append("realtime time")
        elif "open" in part or "close" in part:
            commands.append(part)
        else:
            commands.append(f"general {part}")
            
    return commands

def FirstLayerDMM(query: str) -> list:
    query = query.lower()
    commands = split_complex_query(query)
    decisions = []
    
    for command in commands:
        if command.startswith("generate"):
            prompt = command.replace("generate", "", 1).strip()
            decisions.append(["generate", prompt])
        elif command.startswith("realtime"):
            decisions.append(["realtime", command])
        elif command.startswith("open") or command.startswith("close"):
            decisions.append(["command", command])
        else:
            decisions.append(["general", command])
            
    return decisions

def MainExecution():
    TaskExecution = False
    
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    
    # Get decisions from Model
    decisions = FirstLayerDMM(Query)
    
    # Process each decision
    for decision in decisions:
        decision_type = decision[0]
        
        if decision_type == "generate":
            try:
                prompt = decision[1]
                SetAssistantStatus("Generating image...")
                success = generate_images_and_open(prompt)
                TaskExecution = success
            except Exception as e:
                logger.error(f"Image generation failed: {e}")
                
        elif decision_type == "realtime":
            Answer = RealtimeSearchEngine(QueryModifier(decision[1]))
            ShowTextToScreen(f"{Assistantname}:{Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            TaskExecution = True
            
        elif decision_type == "command":
            run(Automation([decision[1]]))
            TaskExecution = True
            
        elif decision_type == "exit":
            Answer = "Goodbye! Have a great day!"
            ShowTextToScreen(f"{Assistantname}:{Answer}")
            TextToSpeech(Answer)
            sys.exit(0)
            
        else:  # general
            Answer = ChatBot(QueryModifier(decision[1]))
            ShowTextToScreen(f"{Assistantname}:{Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            TaskExecution = True
            
    return TaskExecution

def firstThread():
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            
            if CurrentStatus == "True":
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                
                if "Available..." in AIStatus:
                    time.sleep(0.1)
                else:
                    SetAssistantStatus("Available...")
        except Exception as e:
            logger.error(f"Error in firstThread: {e}", exc_info=True)
            time.sleep(1)  # Add delay before retrying

def SecondThread():
    try:
        GraphicalUserInterface()
    except Exception as e:
        logger.error(f"Error in SecondThread: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        thread1 = threading.Thread(target=firstThread, name="MicrophoneStatusThread", daemon=True)
        thread1.start()
        SecondThread()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Main thread error: {e}", exc_info=True)

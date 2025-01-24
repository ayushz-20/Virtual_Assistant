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
import asyncio
from Backend.ImageGeneration import generate_images_and_open

# Add new imports
import nest_asyncio
nest_asyncio.apply()

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
    """Split multi-part queries and detect command types"""
    commands = []
    parts = query.split(" and ")
    
    automation_keywords = {
        "open": "command",
        "close": "command",
        "play": "command",
        "start": "command",
        "launch": "command"
    }
    
    for part in parts:
        part = part.strip().lower()
        
        # Check for automation commands first
        for keyword, cmd_type in automation_keywords.items():
            if part.startswith(keyword):
                commands.append([cmd_type, part])
                break
        else:
            # If no automation command found, check other types
            if part.startswith("generate"):
                commands.append(["generate", part])
            elif any(word in part for word in ["time", "weather", "news"]):
                commands.append(["realtime", part])
            elif "tell me" in part or "what is" in part:
                commands.append(["general", part])
            else:
                commands.append(["general", part])
    
    return commands

def detect_multiple_commands(query: str) -> list:
    """Advanced command detection using NLP patterns"""
    commands = []
    
    # Command patterns with intent classification
    patterns = {
        'generate': [
            r'(generate|create|make|draw)\s+(a|an)?\s*(\w+(?:\s+\w+)*)',
            r'(image|picture|artwork)\s+of\s+(\w+(?:\s+\w+)*)'
        ],
        'realtime': [
            r'(weather|news|time|updates?)\s+(\w+(?:\s+\w+)*)',
            r'(what|how)\s+is\s+(weather|time|stock|price)'
        ],
        'command': [
            r'(open|close|launch|start)\s+(\w+(?:\s+\w+)*)',
            r'(play|pause|stop)\s+(\w+(?:\s+\w+)*)'
        ],
        'system': [
            r'(volume|brightness)\s+(up|down|mute|unmute)',
            r'(turn|switch)\s+(on|off)\s+(\w+(?:\s+\w+)*)'
        ],
        'general': [
            r'(tell|explain|what|how)\s+(about|is|to)\s+(\w+(?:\s+\w+)*)',
            r'(search|find|look)\s+(for)?\s+(\w+(?:\s+\w+)*)'
        ]
    }
    
    query = query.lower().strip()
    for cmd_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            matches = re.finditer(pattern, query)
            for match in matches:
                commands.append([cmd_type, match.group()])
    
    return commands

def extract_commands(query: str) -> tuple[list, str]:
    """Extract automation and generation commands, return remaining text"""
    commands = []
    remaining_text = query.lower()
    
    # Command extraction patterns
    patterns = {
        'automation': r'(open|close|play|launch|start)\s+(\w+(?:\s+\w+)*)',
        'generate': r'(generate|create|make|draw)\s+(a|an)?\s*(\w+(?:\s+\w+)*)'
    }
    
    # Extract automation commands
    auto_matches = re.finditer(patterns['automation'], remaining_text)
    for match in auto_matches:
        commands.append(["command", match.group()])
        remaining_text = remaining_text.replace(match.group(), "")
    
    # Extract generation commands
    gen_matches = re.finditer(patterns['generate'], remaining_text)
    for match in gen_matches:
        commands.append(["generate", match.group()])
        remaining_text = remaining_text.replace(match.group(), "")
    
    # Clean remaining text
    remaining_text = " ".join(remaining_text.split())
    return commands, remaining_text

async def execute_parallel_tasks(decisions):
    """Enhanced parallel task execution with command separation"""
    automation_tasks = []
    generation_tasks = []
    other_tasks = []
    
    # Separate commands by type
    for decision_type, content in decisions:
        if decision_type == "command":
            automation_tasks.append((decision_type, content))
        elif decision_type == "generate":
            generation_tasks.append((decision_type, content))
        else:
            other_tasks.append((decision_type, content))
    
    try:
        # Process generation and other tasks in parallel
        parallel_tasks = []
        if generation_tasks:
            parallel_tasks.extend([process_decision(dtype, content) 
                                 for dtype, content in generation_tasks])
        if other_tasks:
            parallel_tasks.extend([process_decision(dtype, content) 
                                 for dtype, content in other_tasks])
        
        if parallel_tasks:
            await asyncio.gather(*parallel_tasks)
        
        # Process automation tasks sequentially
        for dtype, content in automation_tasks:
            await process_decision(dtype, content)
        
        return True
    except Exception as e:
        logger.error(f"Task execution error: {e}")
        return False

def FirstLayerDMM(query: str) -> list:
    """Enhanced decision making with command separation"""
    commands, remaining_text = extract_commands(query)
    
    # Process remaining text if any
    if remaining_text:
        if any(word in remaining_text for word in ["weather", "news", "time"]):
            commands.append(["realtime", remaining_text])
        else:
            commands.append(["general", remaining_text])
    
    return commands

async def process_decision(decision_type: str, content: str) -> bool:
    """Enhanced process_decision with parallel support"""
    try:
        match decision_type:
            case "generate":
                SetAssistantStatus(f"Generating image: {content}")
                return await asyncio.to_thread(generate_images_and_open, content)
                
            case "realtime":
                SetAssistantStatus("Getting realtime info...")
                answer = await asyncio.to_thread(RealtimeSearchEngine, QueryModifier(content))
                ShowTextToScreen(f"{Assistantname}:{answer}")
                await asyncio.to_thread(TextToSpeech, answer)
                return True
                
            case "command" | "system":
                SetAssistantStatus(f"Executing {decision_type}: {content}")
                return await Automation([content])
                
            case _:  # general or chat
                SetAssistantStatus("Processing query...")
                answer = await asyncio.to_thread(ChatBot, QueryModifier(content))
                ShowTextToScreen(f"{Assistantname}:{answer}")
                await asyncio.to_thread(TextToSpeech, answer)
                return True
                
    except Exception as e:
        logger.error(f"Error processing {decision_type}: {e}")
        return False

# Add async event loop management
async def execute_tasks(decisions):
    """Execute multiple tasks in parallel with priority handling"""
    # Group tasks by priority
    high_priority = []    # generate, realtime
    medium_priority = []  # general, chat
    low_priority = []     # command, system
    
    for decision_type, content in decisions:
        if decision_type in ["generate", "realtime"]:
            high_priority.append((decision_type, content))
        elif decision_type in ["general", "chat"]:
            medium_priority.append((decision_type, content))
        else:
            low_priority.append((decision_type, content))
    
    try:
        # Execute high priority tasks in parallel
        if high_priority:
            tasks = [process_decision(dtype, content) for dtype, content in high_priority]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        # Execute medium priority tasks in parallel
        if medium_priority:
            tasks = [process_decision(dtype, content) for dtype, content in medium_priority]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        # Execute low priority tasks sequentially
        for dtype, content in low_priority:
            await process_decision(dtype, content)
        
        return True
        
    except Exception as e:
        logger.error(f"Task execution error: {e}")
        return False

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def MainExecution():
    try:
        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
        ShowTextToScreen(f"{Username} : {Query}")
        
        decisions = FirstLayerDMM(Query)
        success = run_async(execute_parallel_tasks(decisions))
        
        if success:
            SetAssistantStatus("Tasks completed")
        return success
        
    except Exception as e:
        logger.error(f"MainExecution error: {e}")
        SetAssistantStatus("Error occurred")
        return False

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

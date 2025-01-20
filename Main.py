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

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    
    print("")
    print(f"Decision : {Decision}")
    print("")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    Mearged_query = "and".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        
    )
    
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
            
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
                
    if ImageExecution == True:
        
        with open(r"Fontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery},True")
            
        try:
            p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
                                stdout=subprocess.PIPE, stderr = subprocess.PIPE,
                                stdin=subprocess.PIPE, shell=False)
            
            subprocesses.append(p1)
            
        except Exception as e:
            print(f"Error starting ImageGeneration.py:{e}")
            
    if G and R or R:
        
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname}:{Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    
    else:
        for Queries in Decision:
            
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general ","")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ","")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay , Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering...")
                os._exit(1)
                
                
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        
        if CurrentStatus == "True":
            MainExecution()
            
        else:
            AIStatus = GetAssistantStatus()
            
            if "Available..." in AIStatus:
                sleep(0.1)
                
            else:
                SetAssistantStatus("Available...")
                
def SecondThread():
    GraphicalUserInterface()
    
if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()




# from Frontend.GUI import (
#     GraphicalUserInterface,
#     SetAssistantStatus,
#     ShowTextToScreen,
#     TempDirectoryPath,
#     SetMicrophoneStatus,
#     AnswerModifier,
#     QueryModifier,
#     GetAssistantStatus,
#     GetMicrophoneStatus
# )

# from Backend.Model import FirstLayerDMM
# from Backend.RealtimeSearchEngine import RealtimeSearchEngine
# from Backend.Automation import Automation
# from Backend.SpeechToText import SpeechRecognition
# from Backend.Chatbot import ChatBot
# from Backend.TextToSpeech import TextToSpeech
# from dotenv import dotenv_values
# from asyncio import run
# from time import sleep
# import subprocess
# import threading
# import json
# import os

# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username")
# Assistantname = env_vars.get("Assistantname")
# DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?
# {Assistantname}: Welcome {Username}. I am doing well. How may I help you?'''
# subprocesses = []
# Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# def ShowDefaultChatIfNoChats():
#     with open(r'Data\Chatlog.json', "r", encoding='utf-8') as file:
#         if len(file.read()) < 5:
#             with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
#                 db_file.write("")
#             with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as resp_file:
#                 resp_file.write(DefaultMessage)

# def ReadChatLogJson():
#     with open(r'Data\Chatlog.json', 'r', encoding='utf-8') as file:
#         chatlog_data = json.load(file)
#     return chatlog_data

# def ChatLogIntegration():
#     json_data = ReadChatLogJson()
#     formatted_chatlog = ""
#     for entry in json_data:
#         role = entry["role"]
#         content = entry["content"]
#         formatted_chatlog += f"{Username if role == 'user' else Assistantname}: {content}\n"
    
#     with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
#         file.write(AnswerModifier(formatted_chatlog))

# def ShowChatsOnGUI():
#     with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
#         data = file.read()
#     if data.strip():
#         with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
#             file.write(data)

# def InitialExecution():
#     SetMicrophoneStatus("False")
#     ShowTextToScreen("")
#     ShowDefaultChatIfNoChats()
#     ChatLogIntegration()
#     ShowChatsOnGUI()

# def handle_image_generation(image_query):
#     with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
#         file.write(f"{image_query},True")
    
#     try:
#         p1 = subprocess.Popen(
#             ['python', r'Backend\ImageGeneration.py'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             stdin=subprocess.PIPE,
#             shell=False
#         )
#         subprocesses.append(p1)
#     except Exception as e:
#         print(f"Error starting ImageGeneration.py: {e}")

# def handle_realtime_search(merged_query):
#     SetAssistantStatus("Searching...")
#     answer = RealtimeSearchEngine(QueryModifier(merged_query))
#     ShowTextToScreen(f"{Assistantname}: {answer}")
#     SetAssistantStatus("Answering...")
#     TextToSpeech(answer)

# def handle_general_queries(decision):
#     for query in decision:
#         if query.startswith("general"):
#             query_final = query.replace("general ", "")
#             answer = ChatBot(QueryModifier(query_final))
#             ShowTextToScreen(f"{Assistantname}: {answer}")
#             SetAssistantStatus("Answering...")
#             TextToSpeech(answer)
#             break
#         elif query.startswith("realtime"):
#             query_final = query.replace("realtime ", "")
#             handle_realtime_search(query_final)
#             break
#         elif query.startswith("exit"):
#             query_final = "Okay, Bye!"
#             answer = ChatBot(QueryModifier(query_final))
#             ShowTextToScreen(f"{Assistantname}: {answer}")
#             SetAssistantStatus("Answering...")
#             TextToSpeech(answer)
#             os._exit(1)

# def MainExecution():
#     TaskExecution = False
#     ImageExecution = False
#     ImageGenerationQuery = ""

#     SetAssistantStatus("Listening...")
#     Query = SpeechRecognition()
#     ShowTextToScreen(f"{Username}: {Query}")
#     SetAssistantStatus("Thinking...")
#     Decision = FirstLayerDMM(Query)

#     print(f"\nDecision: {Decision}\n")

#     G_or_R = any(query.startswith("general") or query.startswith("realtime") for query in Decision)
#     Mearged_query = " and ".join(
#         " ".join(query.split()[1:]) for query in Decision if query.startswith("general") or query.startswith("realtime")
#     )

#     if "generate" in " ".join(Decision):
#         ImageGenerationQuery = [query for query in Decision if "generate" in query][0]
#         ImageExecution = True

#     for query in Decision:
#         if any(query.startswith(func) for func in Functions):
#             if not TaskExecution:
#                 run(Automation(list(Decision)))
#                 TaskExecution = True
#             break

#     if ImageExecution:
#         handle_image_generation(ImageGenerationQuery)

#     if G_or_R:
#         handle_realtime_search(Mearged_query)
#     else:
#         handle_general_queries(Decision)

# def FirstThread():
#     while True:
#         CurrentStatus = GetMicrophoneStatus()
#         if CurrentStatus == "True":
#             MainExecution()
#         else:
#             AIStatus = GetAssistantStatus()
#             if "Available..." in AIStatus:
#                 sleep(0.1)
#             else:
#                 SetAssistantStatus("Available...")

# def SecondThread():
#     GraphicalUserInterface()

# if __name__ == "__main__":
#     thread2 = threading.Thread(target=FirstThread, daemon=True)
#     thread2.start()
#     SecondThread()

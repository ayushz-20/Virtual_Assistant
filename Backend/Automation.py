# from AppOpener import close , open as appopen
# from webbrowser import open as webopen
# from pywhatkit import search , playonyt
# from dotenv import dotenv_values
# from bs4 import BeautifulSoup
# from rich import print
# from groq import Groq
# import webbrowser
# import subprocess
# import requests
# import keyboard
# import asyncio
# import os

# env_vars = dotenv_values(".env")
# GroqAPIKey = env_vars.get("GroqAPIKey")

# # Define CSS classes for parsing specific elements in HTML content.
# classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
#             "IZ6rdc", "O5uR6d LTKOO", "vLzy6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
#             "LwFkFe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# # Define a user-agent for making web requests.
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# # Initialize the Groq client with the API key.
# client = Groq(api_key=GroqAPIKey)

# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else i can help you with.",
#     "I'm at your service for any additional questions or support you may need-don't hesitate to ask",
# ]

# messages = []

# SystemChatBot = [{"role":"system" , "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write a content like letter"}]

# def GoogleSearch(Topic):
#     search(Topic)
#     return True

# def Content(Topic):
    
#     def OpenNotepad(File):
#         default_text_editor = 'notepad.exe'
#         subprocess.Popen([default_text_editor, File])
        
#         def ContentWriterAI(prompt):
#             messages.append({"role":"user", "content": f"{prompt}"})
            
#             completion = client.chat.completions.create(
#                 model="mixtral-8x7b-32768",
#                 messages=SystemChatBot+messages,
#                 max_tokens=2048,
#                 temperature=0.7,
#                 top_p=1,
#                 stream=True,
#                 stop=None
#             )
            
#             Answer = ""
            
            
#             for chunk in completion:
#                 if chunk.choices[0].delta.content:
#                     Answer += chunk.choices[0].delta.content
                    
#             Answer = Answer.replace("</s>", "")
#             messages.append({"role":"assistant", "content":Answer})
#             return Answer
        
#         Topic: str = Topic.replace("content", "")
#         contentByAI= ContentWriterAI(Topic)
        
#         with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
#             file.write(contentByAI)
#             file.close()
            
#         OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
#         return True
    
    
# #function to search for a topic on Youtube
# def YoutubeSearch(Topic):
#     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
#     webbrowser.open(Url4Search)
#     return True

# #function to play a video on youtube
# def PlayYoutube(query):
#     playonyt(query)
#     return True

# #function to open am application or a relevant web-page
# def OpenApp(app, sess=requests.session()):
    
    
#     try:
#         appopen(app, match_closest=True, output=True , throw_error=True)
#         return True
    
#     except:
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')
#             links = soup.find_all('a', {'jsname': 'UWckNb'})
#             return [link.get('href') for link in links]
        
#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}"
#             headers = {"User-Agent": useragent}
#             response = sess.get(url, headers=headers)
            
#             if response.status_code == 200:
#                 return response.text
#             else:
#                 print("Failed to retrieve search results.")
                
#             return None
        
#         html = search_google(app)
        
#         if html:
#             link = extract_links(html)[0]
#             webopen(link)
            
#         return True
    
    
# #function to close an application
# def CloseApp(app):
        
#         if "chrome" in app:
#             pass
#         else:
#             try:
#                 close(app, match_closest=True, output=True, throw_error=True)
#                 return True
#             except:
#                 return False
            
# #function to execute system-level commands
# def System(command):
#     def mute():
#         keyboard.press_and_release("volume mute")
        
#     def unmute():
#         keyboard.press_and_release("volume mute")
        
#     def volume_up():
#         keyboard.press_and_release("volume up")
        
#     def volume_down():
#         keyboard.press_and_release("volume down")
        
        
#     if command == "mute":
#         mute()
#     elif command == "unmute":
#         unmute()
#     elif command == "volume up":
#         volume_up()
#     elif command == "volume down":
#         volume_down()
        
#     return True

# #Asynchronus function to translate and execute user commands
# async def TranslateAndExecute(commands: list[str]):
    
#     funcs = []
    
#     for command in commands:
#         if command.startswith("open"):
#             if "open it" in command:
#                 pass
#             if "open file" == command:
#                 pass
            
#             else:
#                 fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
#                 funcs.append(fun)
                
#         elif command.startswith("general "):
#             pass
#         elif command.startswith("realtime "):
#             pass
#         elif command.startswith("close "):
#             fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
#             funcs.append(fun)
            
#         elif command.startswith("play "):
#             fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
#             funcs.append(fun)
            
#         elif command.startswith("content "):
#             fun = asyncio.to_thread(Content, command.removeprefix("content "))
#             funcs.append(fun)
            
#         elif command.startswith("google search "):
#             fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
#             funcs.append(fun)
            
#         elif command.startswith("youtube search "):
#             fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
#             funcs.append(fun)
            
#         elif command.startswith("system "):
#             fun = asyncio.to_thread(System, command.removeprefix("system "))
#             funcs.append(fun)
            
#         else:
#             print(f"No Function Found. Fpr {command}")
            
#     results = await asyncio.gather(*funcs)
    
#     for result in results:
#         if isinstance(result,str):
#             yield result
#         else:
#             yield result
            
# async def Automation(commands: list[str]):
#     async for result in TranslateAndExecute(commands):
#         pass
#     return True

# if __name__ == "__main__":
#     pass




import asyncio
import logging
import os
import subprocess
import time
from datetime import datetime
from functools import lru_cache
from typing import Dict, Callable, List, Optional, Tuple

import keyboard
import requests
import webbrowser
from AppOpener import close, open as app_open
from dotenv import dotenv_values
from pywhatkit import search, playonyt
import pyttsx3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define a user-agent for web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Define CSS classes for parsing specific elements in HTML content (if needed later)

class AutomationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.command_history = []
        self.command_registry: Dict[str, Callable] = {
            'open': self._handle_open,
            'close': self._handle_close,
            'minimize': self._handle_minimize,
            'play': self._handle_play,
            'system': self._handle_system,
            'content': self._handle_content,
            'google_search': self._handle_google_search,
            'youtube_search': self._handle_youtube_search
        }
        self.automation_keywords = ['open', 'close', 'minimize', 'play', 'start', 'launch']
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.feedback_enabled = False  # Disable feedback
        self.app_keywords = {
            'open': ['and', ',', '&', 'also', 'plus'],
            'close': ['and', ',', '&', 'also', 'plus'],
            'minimize': ['and', ',', '&', 'also', 'plus']
        }
        
    def speak(self, message: str):
        """Provide voice feedback"""
        if self.feedback_enabled:
            self.logger.info(f"TalkBack: {message}")
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()
        
    @lru_cache(maxsize=100)
    async def _handle_open(self, app_name: str) -> bool:
        self.speak(f"Opening {app_name}")
        try:
            success = await asyncio.to_thread(self.open_app, app_name)
            if success:
                self.speak(f"{app_name} opened successfully")
            else:
                self.speak(f"Failed to open {app_name}, trying web search")
            return success
        except Exception as e:
            self.speak(f"Error opening {app_name}")
            return False

    async def _handle_close(self, app_name: str) -> bool:
        """Enhanced close handler with retries"""
        try:
            success = await asyncio.to_thread(self.close_app, app_name)
            if success:
                self.logger.info(f"Closed {app_name}")
            else:
                self.logger.error(f"Failed to close {app_name}")
            return success
        except Exception as e:
            self.logger.error(f"Error closing {app_name}: {e}")
            return False

    async def _handle_minimize(self, app_name: str) -> bool:
        try:
            return await asyncio.to_thread(self.minimize_app, app_name)
        except Exception as e:
            self.logger.error(f"Error minimizing {app_name}: {e}")
            return False

    async def _handle_play(self, query: str) -> bool:
        try:
            return await asyncio.to_thread(self.play_youtube, query)
        except Exception as e:
            self.logger.error(f"Play error: {e}")
            return False

    async def _handle_system(self, command: str) -> bool:
        try:
            return await asyncio.to_thread(self.execute_system_command, command)
        except Exception as e:
            self.logger.error(f"Error executing system command {command}: {e}")
            return False

    async def _handle_content(self, topic: str) -> bool:
        try:
            return await asyncio.to_thread(self.generate_content, topic)
        except Exception as e:
            self.logger.error(f"Error generating content for {topic}: {e}")
            return False

    @lru_cache(maxsize=100)
    async def _handle_google_search(self, query: str) -> bool:
        try:
            return await asyncio.to_thread(self.google_search, query)
        except Exception as e:
            self.logger.error(f"Error searching Google for {query}: {e}")
            return False

    @lru_cache(maxsize=100)
    async def _handle_youtube_search(self, query: str) -> bool:
        try:
            return await asyncio.to_thread(self.youtube_search, query)
        except Exception as e:
            self.logger.error(f"Error searching YouTube for {query}: {e}")
            return False

    def _log_command(self, command: str, success: bool):
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'success': success
        })

    def parse_complex_command(self, command: str) -> List[Tuple[str, str]]:
        """Parse complex commands with multiple actions and apps"""
        all_commands = []
        current_action = None
        
        # First split by different actions
        action_parts = []
        words = command.lower().split()
        temp_part = []
        
        for word in words:
            if word in ['open', 'close', 'minimize']:
                if temp_part:
                    action_parts.append(' '.join(temp_part))
                    temp_part = []
                current_action = word
                temp_part.append(word)
            elif word == 'and':
                if temp_part:
                    action_parts.append(' '.join(temp_part))
                    temp_part = [current_action] if current_action else []
            else:
                temp_part.append(word)
                
        if temp_part:
            action_parts.append(' '.join(temp_part))
        
        # Process each action part
        for part in action_parts:
            words = part.split()
            if words[0] in ['open', 'close', 'minimize']:
                current_action = words[0]
                apps = ' '.join(words[1:])
                # Split multiple apps
                for app in [a.strip() for a in apps.split('and') if a.strip()]:
                    all_commands.append((current_action, app))
                    
        return all_commands

    async def execute_command(self, command: str) -> Tuple[bool, str]:
        """Enhanced execute_command for multiple actions"""
        commands = self.parse_complex_command(command)
        results = []
        
        # Group commands by action type
        action_groups = {
            'open': [],
            'close': [],
            'minimize': []
        }
        
        for action, app in commands:
            action_groups[action].append(app)
        
        # Execute each group
        for action, apps in action_groups.items():
            if apps:
                handler = self.command_registry.get(action)
                if handler:
                    for app in apps:
                        try:
                            success = await handler(app)
                            self._log_command(f"{action} {app}", success)
                            results.append(success)
                        except Exception as e:
                            self.logger.error(f"Error {action} {app}: {e}")
                            results.append(False)
        
        return all(results), ""

    # Individual method implementations
    def open_app(self, app: str) -> bool:
        try:
            app_open(app, match_closest=True, output=True, throw_error=True)
            return True
        except Exception as e:
            self.logger.error(f"App open error: {e}")
            return self.fallback_to_web(app)

    def close_app(self, app: str) -> bool:
        """Enhanced close_app with verification"""
        try:
            # Try multiple close attempts
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # Close using AppOpener
                    close(app, match_closest=True, output=True, throw_error=True)
                    time.sleep(0.5)  # Wait for closure
                    
                    # Verify closure using win32gui
                    import win32gui
                    def check_window(hwnd, app_name):
                        if win32gui.IsWindowVisible(hwnd):
                            title = win32gui.GetWindowText(hwnd).lower()
                            return app_name.lower() in title
                        return False
                    
                    # Check if app is still running
                    found = False
                    def enum_windows(hwnd, result):
                        nonlocal found
                        if check_window(hwnd, app):
                            found = True
                    win32gui.EnumWindows(enum_windows, None)
                    
                    if not found:
                        self.logger.info(f"Successfully closed {app}")
                        return True
                        
                    if attempt < max_attempts - 1:
                        time.sleep(1)  # Wait before retry
                        
                except Exception as e:
                    self.logger.error(f"Close attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        continue
                        
            # Alternative close method using taskkill
            try:
                subprocess.run(['taskkill', '/F', '/IM', f'{app}.exe'], 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
                return True
            except Exception as e:
                self.logger.error(f"Taskkill failed: {e}")
                
            return False
            
        except Exception as e:
            self.logger.error(f"App close error: {e}")
            return False

    def minimize_app(self, app: str) -> bool:
        try:
            # Using Windows API to minimize window
            import win32gui
            def minimize_window(hwnd, wildcard):
                if win32gui.IsWindowVisible(hwnd):
                    if wildcard.lower() in win32gui.GetWindowText(hwnd).lower():
                        win32gui.ShowWindow(hwnd, 6)  # SW_MINIMIze
            
            win32gui.EnumWindows(lambda hwnd, _: minimize_window(hwnd, app), None)
            return True
        except Exception as e:
            self.logger.error(f"Minimize error: {e}")
            return False

    def play_youtube(self, query: str) -> bool:
        try:
            webbrowser.open('https://www.youtube.com')
            time.sleep(2)  # Wait for YouTube to load
            playonyt(query.strip().replace(' ', '+'))
            return True
        except Exception as e:
            self.logger.error(f"YouTube playback error: {e}")
            return False

    def execute_system_command(self, command: str) -> bool:
        commands = {
            "mute": lambda: keyboard.press_and_release("volume mute"),
            "unmute": lambda: keyboard.press_and_release("volume mute"),
            "volume up": lambda: keyboard.press_and_release("volume up"),
            "volume down": lambda: keyboard.press_and_release("volume down")
        }
        action = commands.get(command)
        if action:
            action()
            return True
        self.logger.error(f"Unknown system command: {command}")
        return False

    def generate_content(self, topic: str) -> bool:
        # Mock content generation logic
        content = f"Generated content for {topic}"
        filepath = rf"Data\{topic.lower().replace(' ', '')}.txt"
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        subprocess.Popen(['notepad.exe', filepath])
        return True

    def google_search(self, query: str) -> bool:
        search(query)
        return True

    def youtube_search(self, query: str) -> bool:
        Url4Search = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(Url4Search)
        return True

    def fallback_to_web(self, app: str) -> bool:
        try:
            webbrowser.open(f"https://www.google.com/search?q={app}")
            return True
        except Exception as e:
            self.logger.error(f"Fallback web search error: {e}")
            return False

    def filter_automation_commands(self, command: str) -> bool:
        """Check if command is automation-related"""
        return any(command.lower().startswith(keyword) for keyword in self.automation_keywords)

async def Automation(commands: List[str]) -> Tuple[bool, List[str]]:
    """Enhanced automation for complex commands"""
    manager = AutomationManager()
    results = []
    feedback = []
    
    for command in commands:
        # Handle complex command
        if any(keyword in command.lower() for keyword in ['and', ',', '&']):
            success, msg = await manager.execute_command(command)
            results.append(success)
            feedback.append(msg)
        # Handle simple command
        else:
            success, msg = await manager.execute_command(command)
            results.append(success)
            feedback.append(msg)
    
    return all(results), feedback

# Test function
if __name__ == "__main__":
    async def test():
        test_commands = [
            "open chrome and firefox and whatsapp",
            "close notepad and word and minimize excel",
            "open spotify and close vlc and minimize chrome"
        ]
        
        success, feedback = await Automation(test_commands)
        print(f"Overall success: {success}")
        for cmd, msg in zip(test_commands, feedback):
            print(f"{cmd}: {msg}")
    
    asyncio.run(test())


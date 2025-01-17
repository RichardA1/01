from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from platformdirs import user_data_dir
import os
import glob
import json
from pathlib import Path
from interpreter import OpenInterpreter
from .system_messages.BaseSystemMessage import system_message


def configure_interpreter(interpreter: OpenInterpreter):
    
    ### SYSTEM MESSAGE
    interpreter.system_message = system_message

    ### LLM SETTINGS

    # Local settings
    # interpreter.llm.model = "local"
    # interpreter.llm.api_base = "https://localhost:8080/v1" # Llamafile default
    # interpreter.llm.max_tokens = 1000
    # interpreter.llm.context_window = 3000

    # Hosted settings
    interpreter.llm.api_key = os.getenv('OPENAI_API_KEY')
    interpreter.llm.model = "gpt-4"

    ### MISC SETTINGS

    interpreter.auto_run = True
    interpreter.computer.languages = [l for l in interpreter.computer.languages if l.name.lower() in ["applescript", "shell", "zsh", "bash", "python"]]
    interpreter.force_task_completion = False
    interpreter.offline = True
    interpreter.id = 206 # Used to identify itself to other interpreters. This should be changed programatically so it's unique.

    ### RESET conversations/user.json

    
    app_dir = user_data_dir('01')
    conversations_dir = os.path.join(app_dir, 'conversations')
    os.makedirs(conversations_dir, exist_ok=True)
    user_json_path = os.path.join(conversations_dir, 'user.json')
    with open(user_json_path, 'w') as file:
        json.dump([], file)

    ### SKILLS
    skills_dir = user_data_dir('01', 'skills')
    interpreter.computer.skills.path = skills_dir
    interpreter.computer.skills.import_skills()

    interpreter.computer.run("python", "tasks=[]")

    interpreter.computer.api_base = "https://oi-video-frame.vercel.app/"
    interpreter.computer.run("python","print('test')")

    return interpreter
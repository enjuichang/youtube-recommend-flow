import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, 'data')

GPT3_PROMPT_FILE = os.path.join(DATA_DIR, 'gpt3_video_game.txt')
BRAIN_OPENAI_URI = os.getenv('BRAIN_OPENAI_URI', 'https://api.braininc.net/be/bas-demo-v4/nlp/brain_openai')

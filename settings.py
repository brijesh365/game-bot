import os

# TODO load this settings from env
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
RESULTS_COUNT = 5
API_KEY = os.environ.get('API_KEY')
CSE_ID = os.environ.get('CSE_ID')
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

from dotenv import load_dotenv
from os import getenv
load_dotenv()


PORT = int(getenv('PORT', 5000))
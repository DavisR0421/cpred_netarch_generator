import requests
from dotenv import load_dotenv
import os
# use pprint for pretty-printing the output
import json
from pprint import pprint

# dotenv is used to load environment variables from a .env file
# This allows for sensitive information like API keys to be kept out of the source code
load_dotenv()
# API Key is unused for now
v_api_key = os.getenv("API_KEY")

v_difficulty_rating = input("Architecture difficulty rating: ")
# value2 = input("Enter the value for 'j': ")

def create_net():
    return "Wake the fuck up, samurai. We have a city to burn."

if __name__ == "__main__":
    message = create_net()
    print(f"\n{message}\n")
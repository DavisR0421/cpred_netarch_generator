"""
Created Oct 2025
Davis Richardson
"""
# import requests
from dotenv import load_dotenv
import os
# import json
import logging
from pprint import pprint
import time

from src.utils.roll import roll
from src.corebook_reference.netarch_options import set_difficulty,set_size,populate_floor
from src.utils.net_arch_builder import NetArchitecture

logger = logging.getLogger(__name__)
# dotenv is used to load environment variables from a .env file
# This allows for sensitive information like API keys to be kept out of the source code
# load_dotenv()
# # API Key is unused for now
# v_api_key = os.getenv("API_KEY")

# NET = describe_options()

WAKEUP_MESSAGE = "\nWake the fuck up, samurai. We have a city to burn.\n" 

"""
python -m src.gm_funcs.netarchgenerator
"""

def create_net():

    netarch_difficulty = set_difficulty()
    netarch_size = set_size()
    constructed_floors = 0
    can_branch = True

    net_architecture = NetArchitecture()

    while constructed_floors < netarch_size:
        branchroll = roll()
        floor_data = populate_floor(constructed_floors, netarch_difficulty)
        if 2 <= constructed_floors <= (netarch_size-3) and can_branch and branchroll >= 7:
            net_architecture.append(floor_data,branching=True)
            constructed_floors += 1
        elif 2 <= constructed_floors <= (netarch_size-3) and can_branch and branchroll < 7:
            net_architecture.append(floor_data)
            constructed_floors += 1
            can_branch = False
        else:
            net_architecture.append(floor_data)
            constructed_floors += 1
    
    print(f"> {netarch_difficulty} net architecture created with {netarch_size} floors\n")
    return net_architecture


if __name__ == "__main__":
   
    print(WAKEUP_MESSAGE)
    time.sleep(1)

    net_architecture = create_net()

    netrun_active = True
    while netrun_active:
        command = input(f"> input net action or '-jackout': ").lower()
        match command:
            case '-jackout':
                print(f"Later, Choom. good luck out there.\n")
                netrun_active = False
            case _ :
                print(f"> actually that's all i've got, sorry\n> just -jackout for now and i'll have more later.")
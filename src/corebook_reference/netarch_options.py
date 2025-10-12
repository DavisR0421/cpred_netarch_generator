import time
import sys

from src.utils.roll import roll
from src.corebook_reference.difficulty import net_architecture_difficulty, net_architecture_difficulty_fulldesc
from src.corebook_reference.floorcontents import lobby_contents, floor_contents


JACK_OUT_REMINDER = "> input -net.exitto exit the program"
INFO_REMINDER = "input '<option>.info' or '-all.info' for more details"

REF_DIFFICULTY = net_architecture_difficulty
REF_DIFFICULTY_FULLDESC = net_architecture_difficulty_fulldesc

LOBBY_TABLE = lobby_contents
FLOOR_TABLE = floor_contents

def _describe_reference(reference, fulldesc, option:str, printopts:bool =True) -> list:
    option = option.lower()
    if option not in reference.keys():
        print(f"\nOption '{option}' not recognized. Valid options are: {list(reference.keys())}\n")
        return
    else:
        option_info = reference.get(option)
        option_msg = f"\n{option.capitalize()}:"
        optionout = [option_msg]
        print(option_msg)
        for k in fulldesc.keys():
            optionout.append(f"{k}: {option_info[k]}")
            print(f"{fulldesc[k]}: {option_info[k]}")

    return optionout

def _describe_all(reference, fulldesc, printopts:bool=True) -> dict:
    opts = {}
    for option in reference.keys():
        _describe_reference(reference, fulldesc, option, printopts)
        opts[option] = reference.get(option)
    return opts

def set_difficulty() -> str:
    
    v_difficulty_rating = None
    # netarch_difficulty_opts = self.netarch_difficulty_opts
    opts_list = list(REF_DIFFICULTY.keys())

    while v_difficulty_rating not in REF_DIFFICULTY:
        # print("")
        v_difficulty_rating = str(input(f"> input net architecture difficulty or -net.exit\n"\
                                        f"> {INFO_REMINDER}\n"\
                                        f"> {opts_list}: ")).lower()
        # v_difficulty_rating = v_difficulty_rating.lower()
        match v_difficulty_rating:
            case '-jackout':
                print(f"\nDidn't have it in you, huh? Later, choom.\n")
                time.sleep(1)
                sys.exit(0)
            case '-all.info':
                _describe_all(REF_DIFFICULTY, REF_DIFFICULTY_FULLDESC)
                print("")
            case i if '.info' in i:
                _describe_reference(REF_DIFFICULTY, REF_DIFFICULTY_FULLDESC, i.replace('.info',''))
                print("")
            case quotes if '"' in quotes or "'" in quotes:
                print("\nFirst netrun? Drop the quotes and try again, gonk.\n")
            case _:
                if v_difficulty_rating not in REF_DIFFICULTY:
                    print(f"Option '{v_difficulty_rating}' not recognized. Valid options are: {list(REF_DIFFICULTY)}\n")
    

    return v_difficulty_rating

def get_difficulty_dv(difficulty):
    v_diff_dv = REF_DIFFICULTY.get(difficulty).get('pfcn_dv')
    return v_diff_dv

def set_size(n_oversized_dice:int=0) -> int:
    v_total_floors = roll(3+n_oversized_dice,'d6')
    return v_total_floors


def populate_floor(floor_num:int, netarch_difficulty:str) -> str:
    lobby_table = LOBBY_TABLE
    floor_table = FLOOR_TABLE.get(netarch_difficulty) 
    floor_dv = get_difficulty_dv(netarch_difficulty)

    if floor_num < 2:
        content = lobby_table.get(roll(1,'d6'))
    else:
        content = floor_table.get(roll(3,'d6'))
    
    if content[0] in ['file','password','control node'] and len(content)<2:
        content += [floor_dv]
    
    return {'floor_id':floor_num,
            'content':content}
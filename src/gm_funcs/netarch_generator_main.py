"""
Created Oct 2025
Davis Richardson
"""
import os
import datetime as dt
import logging
from pprint import pprint
import time
import pickle

from src.utils.roll import roll
from src.corebook_reference.netarch_options import set_difficulty,set_size,populate_floor
from src.utils.net_arch_builder import NetArchitecture
from src.utils.dir_utils import set_file_dir, get_file_dir,is_valid_filename

logger = logging.getLogger(__name__)

WAKEUP_MESSAGE = "\nWake the fuck up, samurai. We have a city to burn.\n" 


"""
python -m src.gm_funcs.netarch_generator_main
"""

def create_net(netarch_instance=None)->NetArchitecture:

    load_safe = False
    if netarch_instance:
        while not load_safe:
            confirm = input(f"\n! WARNING ! Net Architecture [{netarch_instance.get_name()}] is currently active\
                            \ninitializing a new net architecture will override it and any unsaved changes will be lost\
                            \n> '-continue' to continue with load\
                            \n> '-save -c' to save current architecture then continue with load\
                            \n> '-cancel' to cancel load and return to previous options\
                            \n> input: ").lower()
            match confirm:
                case '-continue':
                    load_safe = True
                case '-save -c':
                    save_net(netarch_instance)
                    load_safe = True
                    print(f"\n> continuing with net architecture init")
                case '-cancel':
                    print(f"\n> cancelling init")
                    break    
                case _:
                    print("\n> input not recognized")

    else:
        load_safe = True

    if load_safe == True:
        netarch_difficulty = set_difficulty()
        netarch_size = set_size()
        constructed_floors = 0
        can_branch = True

        retries, max_retries = 0, 10 
        valid_root = False

        while valid_root is False and retries < max_retries:
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
            retries += 1
            valid_root = net_architecture.validate_root()

        print(f"\n> {netarch_difficulty} net architecture created with {netarch_size} floors")
        return net_architecture

def save_net(netarch_instance:NetArchitecture):
    archname = netarch_instance.get_name()

    save_directory = get_file_dir('net_architectures')
    os.makedirs(save_directory, exist_ok=True)

    # if archname == '':
    #     netarch_instance.set_name(f'net_architecture_{dt.datetime.today().date().strftime('%y%m%d')}')
    #     archname = netarch_instance.get_name()
        
    save_complete = False
    while save_complete is False:
        nameconfirm = input(f"\n> current architecture name is [{archname}]\
                         \n> current save directory is [{os.path.abspath(save_directory)}]\
                         \n> '-confirm' to save with this name and directory\
                         \n> '-rename' to change netarch name\
                         \n> '-changedir' to change the save directory\
                         \n> '-cancel' to cancel save operation\
                         \n input: ")
        match nameconfirm:
            case '-confirm':
                filename = f"{archname}.pkl"
                full_path = os.path.join(save_directory,filename)
                print(f"\n> saving [{archname}] to [{full_path}]")
                with open(full_path, 'wb') as f:
                    pickle.dump(netarch_instance, f)
                print(f"\n> save complete")
                save_complete = True
            case '-rename':
                newname = input(f"\n> input new architecture name: ")
                if is_valid_filename(newname+'.pkl'):
                    netarch_instance.set_name(newname)
                    archname = netarch_instance.get_name()
                    # print(f"\n> architecture name set: {newname}")
                else:
                    print(f"\n> WARNING: Invalid name\
                          \n> architecture name cannot contain [<, >, :, \", /, \\\\, |, or * ]\
                          \n> keeping old name")
            case '-changedir':
                newdir = input("\n input new save file directory: ")
                set_file_dir(newdir)
                save_directory = get_file_dir()
                print(f"\n> save file directory set: {newdir}")
            case '-cancel':
                print("\n> cancelling file save")
                save_complete = True
            case _:
                print("> option not recognized")

def load_net(netarch_instance:NetArchitecture = None)->NetArchitecture:
    save_directory = get_file_dir('net_architectures')
    abspath = os.path.abspath(save_directory)

    saved_files = [f for f in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, f))]
    name_dict = {i:file[:-4] for i, file in enumerate(saved_files)}

    load_safe = False
    if netarch_instance:
        while not load_safe:
            confirm = input(f"\n! WARNING ! Net Architecture [{netarch_instance.get_name()}] is currently active\
                            \nloading a saved net architecture will override it and any unsaved changes will be lost\
                            \n> '-continue' to continue with load\
                            \n> '-save -c' to save current architecture then continue with load\
                            \n> '-cancel' to cancel load and return to previous options\
                            \n> input: ").lower()
            match confirm:
                case '-continue':
                    load_safe = True
                case '-save -c':
                    save_net(netarch_instance)
                    load_safe = True
                    print(f"\n> continuing with net architecture load")
                case '-cancel':
                    print(f"\n> cancelling load")
                    break
                case _:
                    print("\n> input not recognized")
    else:
        load_safe = True
    
    load_complete = False
    while not load_complete:
        loadcommand = input(f"\n> current save directory is [{os.path.abspath(abspath)}]\
                            \n> '-load <net architecture name>' to load a known net architecture\
                            \n> '-list all' to view existing net architectures in directory\
                            \n> '-changedir' to change to a different directory\
                            \n> '-cancel' to cancel load\
                            \n> input: ")
        if loadcommand[:6] == '-load ':
            archname = loadcommand[6:]
            filename = archname
            if loadcommand[-4:] != '.pkl':
                filename += '.pkl'
            
            if filename in saved_files:
                full_path = os.path.join(save_directory,filename)
                try:
                    with open(full_path, 'rb') as f:
                        obj = pickle.load(f)
                    print(f"{archname} loaded!")
                    load_complete = True
                    netarch_instance = obj
                except:
                    print(f"\nnet architecture load failed. Try again")
            else: 
                print(f"\ncannot find '{filename}' in directory")
        elif loadcommand == "-list all":
            pprint(name_dict)
            iload_complete = False
            while not iload_complete:
                indexload = input(f"\n> input the index of the file to load or '-cancel': ")
                if name_dict[int(indexload)]:
                    filename = name_dict[int(indexload)]+'.pkl'
                    full_path = os.path.join(save_directory,filename)
                    with open(full_path, 'rb') as f:
                            obj = pickle.load(f)
                    print(f"{name_dict[int(indexload)]} loaded!")
                    iload_complete = True
                    load_complete = True
                    netarch_instance = obj
                elif indexload == '-cancel':
                    print("cancelling index load")
                    iload_complete = True
                else:
                    print(f"> option not recognized")
        elif loadcommand == '-changedir':
            newdir = input("\n input new save file directory: ")
            set_file_dir(newdir)
            save_directory = get_file_dir()
            abspath = os.path.abspath(save_directory)
            print(f"\n> save file directory set: {newdir}")
        elif loadcommand == '-cancel':
            print("cancelling file load")
            load_complete = True

    return netarch_instance

if __name__ == "__main__":
   
    print(WAKEUP_MESSAGE)
    # print(SAVE_DIRECTORY)
    # print(os.path.abspath(SAVE_DIRECTORY))
    time.sleep(1)

    net_architecture = None

    netrun_active = False
    netrun_floor = None
    available_actions = {
                        'arch': 
                            [
                                '-init',
                                '-exit',
                                '-save',
                                '-load',
                                {'-show':['--all','--root']}
                            ],
                         'net':
                            [
                             '-jack_in',
                             '-jack_out'
                            ]
                         }
    
    

    SESSION_ACTIVE = True
    while SESSION_ACTIVE:
        command = input(f"\n> awaiting input ('options -show' for help): ").lower()
        match command:
            case 'options -show':
                pprint(available_actions)
            case 'arch -init':
                net_architecture = create_net(net_architecture)
            case 'arch -exit':
                print(f"\nLater, Choom. good luck out there.\n")
                SESSION_ACTIVE = False
            case 'arch -save':
                if net_architecture:
                    save_net(net_architecture)
                else:
                    print(f"\nno active net acitecture to save\
                          \ninitiate a new net architecture or load an existing one")
            case 'arch -load':
                if net_architecture:
                    net_architecture = load_net(net_architecture)
                else:
                    net_architecture = load_net()
            case 'arch -show --all':
                net_architecture.display()
            case 'arch -show --root':
                net_architecture.get_root_identity()
            case 'net -jack_in':
                if netrun_active is False:
                    print("jacked in!")
                    # current = net_architecture.move_forward(1)
                    current = net_architecture.head
                    print(f" current floor: {current.data['floor_name']}")
                    print(f" CONTACT -> {current.data['content']}")
                    netrun_active = True
                else:
                    print("\n you're already jacked in")
            case 'net -jack_out':
                if netrun_active and current.data['floor_name'] == "b.000.0::f.0.1":
                    current = None
                    netrun_active = False
                    print("\n> jacked out safely\nwelcome back to the real world, runner")
                elif netrun_active and current.data['floor_name'] != "b.000.0::f.0.1":
                    confirm = ''
                    while confirm not in ['y','n']:
                        confirm = input(f"\n!!! WARNING !!! UNSAFE JACK OUT !!!> \
                                        \ncurrent floor is {current.data['floor_name']}\
                                        \nsafe jackout on floor b.000.0::f.0.1 only\
                                        \nCONFIRM JACK OUT [Y/N]: ").lower()
                        if confirm == 'y':
                            print("forcing jack out")
                            current = None
                            netrun_active = False
                            print("forced jack out complete")
                        elif confirm == 'n':
                            print("cancelling jack out")
                        else:
                            print("\nnot a good time to be screwing around, gonk\n")
            case _ :
                print(f"> actually that's all i've got, sorry\n> just -jackout for now and i'll have more later.")
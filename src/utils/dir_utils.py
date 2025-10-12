import configparser
import os
import re

CONFIG_FILE = 'config.ini'

def get_file_dir(directory:str=None):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('paths', directory, fallback='./data/')

def set_file_dir(new_path, directory=None):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'paths' not in config:
        config['paths'] = {}
    config['paths'][directory] = './data/'+new_path
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def is_valid_filename(filename):
    # Disallowed characters on Windows
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    # Reserved filenames on Windows
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }

    # Check for invalid characters
    if re.search(invalid_chars, filename):
        return False

    # Check for reserved names (case-insensitive)
    name_without_ext = os.path.splitext(filename)[0].upper()
    if name_without_ext in reserved_names:
        return False

    # Check for empty or whitespace-only filenames
    if not filename.strip():
        return False

    return True
# def save_pickle(obj, filename='object.pkl'):
#     pickle_dir = get_file_dir()
#     os.makedirs(pickle_dir, exist_ok=True)
#     full_path = os.path.join(pickle_dir, filename)
#     with open(full_path, 'wb') as f:
#         pickle.dump(obj, f)
#     return os.path.abspath(full_path)
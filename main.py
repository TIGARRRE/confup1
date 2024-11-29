import yaml
import os
from zipfile import ZipFile, ZIP_DEFLATED

# Load configuration
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# Open zip archive with the virtual file system
vfs_path = cfg.get('vfs_path', 'a.zip')
with ZipFile(vfs_path, 'a') as file:
    pwd = '/'  # Current directory

def cmd_exit():
    # Process the 'exit' command
    print("Exiting the virtual shell.")
    return True  # Indicate that we should exit

while True:
    command = input(f"{cfg['Name']}@virtual_shell:{pwd}$ ").strip()
    
    if command == 'exit':
        if cmd_exit():
            break  # Exit the loop if cmd_exit indicates to exit
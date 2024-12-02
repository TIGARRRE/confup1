import logging
import yaml
import os
from zipfile import ZipFile

# Настройка логирования
logging.basicConfig(level=logging.INFO)

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

vfs_path = cfg.get('vfs_path', 'a.zip')
pwd = '/'


def cmd_pwd():
    logging.info(f"Current directory: {pwd}")
    print(pwd)

def cmd_ls():
    contents = set()
    with ZipFile(vfs_path, 'r') as file:
        for name in file.namelist():
            if name.startswith(pwd.lstrip('/')):
                relative = name[len(pwd.lstrip('/')):].strip('/')
                if relative:
                    contents.add(relative.split('/')[0])
    if contents:
        logging.info(f"Contents of directory {pwd}: {sorted(contents)}")
        print('\n'.join(sorted(contents)))
    else:
        logging.info(f"Directory {pwd} is empty.")
        print()

def cmd_rm(target):
    target_path = os.path.join(pwd, target).lstrip('/')
    found = False
    updated_files = []
    
    with ZipFile(vfs_path, 'r') as file:
        for name in file.namelist():
            if name == target_path or name.startswith(target_path + '/'):
                found = True
            else:
                updated_files.append(name)
    
    if not found:
        logging.warning(f"rm: cannot remove '{target}': No such file or directory")
        print(f"rm: cannot remove '{target}': No such file or directory")
    else:
        temp_zip_path = 'temp.zip'
        try:
            with ZipFile(temp_zip_path, 'w') as updated_zip:
                for name in updated_files:
                    with ZipFile(vfs_path, 'r') as file:
                        updated_zip.writestr(name, file.read(name))
            
            os.replace(temp_zip_path, vfs_path)
            logging.info(f"'{target}' has been removed.")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")
            print(f"PermissionError: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

def cmd_cd(dir_name):
    global pwd
    if dir_name == '/':
        pwd = '/'
    elif dir_name == '..':
        pwd = os.path.dirname(pwd.rstrip('/')) or '/'
    else:
        path = os.path.join(pwd, dir_name).lstrip('/')
        with ZipFile(vfs_path, 'r') as file:
            if any(name.startswith(path + '/') for name in file.namelist() if name.endswith('/')):
                pwd = path if path.endswith('/') else path + '/'
                logging.info(f"Changed directory to {pwd}")
            else:
                logging.warning(f"cd: no such file or directory: {dir_name}")
                print(f"cd: no such file or directory: {dir_name}")

def cmd_mkdir(new_dir):
    path = os.path.join(pwd, new_dir).lstrip('/') + '/'
    with ZipFile(vfs_path, 'r') as file:
        if path in file.namelist():
            logging.warning(f"mkdir: cannot create directory '{new_dir}': File exists")
            print(f"mkdir: cannot create directory '{new_dir}': File exists")
        else:
            with ZipFile(vfs_path, 'a') as file:
                file.writestr(path, '')
            logging.info(f"Directory '{new_dir}' created.")
            print(f"Directory '{new_dir}' created.")

def cmd_touch(touch_file):
    path = os.path.join(pwd, touch_file).lstrip('/')
    with ZipFile(vfs_path, 'r') as file:
        if path in file.namelist():
            logging.warning(f"touch: '{touch_file}' already exists")
            print(f"touch: '{touch_file}' already exists")
        else:
            with ZipFile(vfs_path, 'a') as file:
                file.writestr(path, '')
            logging.info(f"File '{touch_file}' created.")
            print(f"File '{touch_file}' created.")

def cmd_exit():
    logging.info("Exiting the virtual shell.")
    exit()

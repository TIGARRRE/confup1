import yaml
import os
from zipfile import ZipFile

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

vfs_path = cfg.get('vfs_path', 'a.zip')
pwd = '/'


def cmd_pwd():
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
        print('\n'.join(sorted(contents)))
    else:
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
        print(f"rm: cannot remove '{target}': No such file or directory")
    else:
        temp_zip_path = 'temp.zip'
        try:
            with ZipFile(temp_zip_path, 'w') as updated_zip:
                for name in updated_files:
                    with ZipFile(vfs_path, 'r') as file:
                        updated_zip.writestr(name, file.read(name))
            
            # Attempt to replace the original zip file
            os.replace(temp_zip_path, vfs_path)
            print(f"'{target}' has been removed.")
        except PermissionError as e:
            print(f"PermissionError: {e}")
            print("Make sure the file is not open in another program and that you have the required permissions.")
        except Exception as e:
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
            else:
                print(f"cd: no such file or directory: {dir_name}")

def cmd_mkdir(new_dir):
    path = os.path.join(pwd, new_dir).lstrip('/') + '/'
    with ZipFile(vfs_path, 'r') as file:
        if path in file.namelist():
            print(f"mkdir: cannot create directory '{new_dir}': File exists")
        else:
            with ZipFile(vfs_path, 'a') as file:
                file.writestr(path, '')
            print(f"Directory '{new_dir}' created.")

def cmd_touch(touch_file):
    path = os.path.join(pwd, touch_file).lstrip('/')
    with ZipFile(vfs_path, 'r') as file:
        if path in file.namelist():
            print(f"touch: '{touch_file}' already exists")
        else:
            with ZipFile(vfs_path, 'a') as file:
                file.writestr(path, '')
            print(f"File '{touch_file}' created.")

def cmd_exit():
    return 0

with ZipFile(vfs_path, 'a') as file:
    while True:
        command = input(f"{cfg['Name']}@virtual_shell:{pwd}$ ").strip()
        if not command:
            continue

        parts = command.split()
        cmd, *args = parts

        if cmd == 'exit':
            cmd_exit()
        elif cmd == 'pwd':
            cmd_pwd()
        elif cmd == 'ls':
            cmd_ls()
        elif cmd == 'rm':
            if args:
                file.close()
                cmd_rm(args[0]) 
                file = ZipFile(vfs_path, 'a') 
            else:
                print("rm: missing argument")
        elif cmd == 'cd':
            if args:
                cmd_cd(args[0])
            else:
                print("cd: missing argument")
        elif cmd == 'mkdir':
            if args:
                cmd_mkdir(args[0])
            else:
                print("mkdir: missing argument")
        elif cmd == 'touch':
            if args:
                cmd_touch(args[0])
            else:
                print("touch: missing argument")
        else:
            print(f"{cmd}: command not found")
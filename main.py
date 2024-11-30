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
    for name in file.namelist():
        if name.startswith(pwd.lstrip('/')):  
            relative = name[len(pwd.lstrip('/')):].strip('/')
            if relative:
                contents.add(relative.split('/')[0])
    if contents:
        print('\n'.join(sorted(contents)))
    else:
        print()

def cmd_cd(dir_name):
    global pwd
    if dir_name == '/':
        pwd = '/'
    elif dir_name == '..':
        pwd = os.path.dirname(pwd.rstrip('/')) or '/'
    else:
        path = os.path.join(pwd, dir_name).lstrip('/')
        if any(name.startswith(path + '/') for name in file.namelist() if name.endswith('/')):
            pwd = path if path.endswith('/') else path + '/'
        else:
            print(f"cd: no such file or directory: {dir_name}")

def cmd_mkdir(new_dir):
    path = os.path.join(pwd, new_dir).lstrip('/') + '/'
    if path in file.namelist():
        print(f"mkdir: cannot create directory '{new_dir}': File exists")
    else:
        file.writestr(path, '')

def cmd_touch(touch_file):
    path = os.path.join(pwd, touch_file).lstrip('/')
    if path in file.namelist():
        print(f"touch: '{touch_file}' already exists")
    else:
        file.writestr(path, '')
def cmd_exit():
    return 0

with ZipFile(vfs_path, 'a') as file:
    while True:
        command = input(f"{cfg['Name']}@virtual_shell:{pwd}$ ").strip()
        if not command:
            continue

        parts = command.split()
        cmd, *args = parts

        # Обработка команд
        if cmd == 'exit':
            exit()
        elif cmd == 'pwd':
            cmd_pwd()
        elif cmd == 'ls':
            cmd_ls()
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

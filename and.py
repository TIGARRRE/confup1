import yaml
import os
from zipfile import ZipFile, ZIP_DEFLATED

# Загружаем конфигурацию
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# Открываем zip-архив с виртуальной файловой системой
vfs_path = cfg.get('vfs_path', 'a.zip')
with ZipFile(vfs_path, 'a') as file:
    pwd = '/'  # Текущая директория

    while True:
        # Получаем команду от пользователя
        command = input(f"{cfg['Name']}@virtual_shell:{pwd}$ ").strip()

        # Обработка команды 'exit'
        if command == 'exit':
            break

        # Обработка команды 'pwd' для отображения текущей директории
        elif command == 'pwd':
            print(pwd)

        # Обработка команды 'ls' для отображения содержимого текущей директории
        elif command == 'ls':
            contents = set()
            for name in file.namelist():
                if name.startswith(pwd.lstrip('/')):  # Проверяем содержимое текущего каталога
                    relative_path = name[len(pwd.lstrip('/')):].strip('/')
                    if relative_path:
                        first_part = relative_path.split('/')[0]
                        contents.add(first_part)

            for item in contents:
                print(item)

        # Обработка команды 'cd'
        elif command.startswith('cd '):
            dir_name = command[3:].strip()
            if dir_name == '/':
                # Переход на уровень выше
                pwd = os.path.dirname(pwd.rstrip('/'))
                if pwd == '':
                    pwd = '/'
            else:
                # Переход в указанный каталог
                potential_path = os.path.join(pwd, dir_name).lstrip('/')
                if any(name.startswith(potential_path + '/') for name in file.namelist() if name.endswith('/')):
                    pwd = potential_path
                    if not pwd.endswith('/'):
                        pwd += '/'
                else:
                    print(f"cd: no such file or directory: {dir_name}")

        # Обработка команды 'mkdir'
        elif command.startswith('mkdir '):
            new_dir = command[6:].strip()
            new_dir_path = os.path.join(pwd, new_dir).lstrip('/') + '/'
            if new_dir_path in file.namelist():
                print(f"mkdir: cannot create directory '{new_dir}': File exists")
            else:
                # Создаем "пустой" каталог в zip-файле
                with ZipFile(vfs_path, 'a') as zip_file:
                    zip_file.writestr(new_dir_path, '')
                    
        # Обработка команды 'rm'            
        elif command.startswith('rm '):
            del_dir = command[3:].strip()
            print(pwd)
            file.remove(f"del_dir")
            
            

        #обработка комманды touch
                    
        elif command.startswith('touch '):
                    touch_file = command[6:].strip()
                    fullnewname = (touch_file + ".txt")
                    char = (fullnewname)
                    # Определяем полный путь до файла в текущей директории
                    file_path = os.path.join(pwd, touch_file).lstrip('/')
                    
                    # Проверяем, существует ли файл в текущей директории
                    if any(name == file_path for name in file.namelist()):
                        print(f"touch: '{touch_file}' already exists")
                    else:
                        # Создаем новый файл
                        with ZipFile(vfs_path, 'a') as zip_file:
                            zip_file.writestr(char, '')
                        print(f"'{touch_file}' has been created.")


        # Обработка неизвестных команд
        else:
            print(f"{command}: command not found")
            

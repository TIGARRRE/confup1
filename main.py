import yaml
import sys
import os
from zipfile import ZipFile

# Настройка
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
        return f"rm: cannot remove '{target}': No such file or directory"
    else:
        temp_zip_path = 'temp.zip'
        try:
            with ZipFile(temp_zip_path, 'w') as updated_zip:
                for name in updated_files:
                    with ZipFile(vfs_path, 'r') as file:
                        updated_zip.writestr(name, file.read(name))
            os.replace(temp_zip_path, vfs_path)
            return f"'{target}' has been removed."
        except Exception as e:
            return f"An error occurred: {e}"


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
                pwd =  path if path.endswith('/') else path + '/'
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
    exit()
    
    
    

def cmd_test():
    results = []
    # Тесты для cmd_pwd
    print("Testing cmd_pwd:")
    global pwd
    pwd = '/'  # Установим начальный путь
    output = sys.stdout  # Сохраним стандартный вывод
    from io import StringIO  # Импортируем StringIO для захвата вывода

    # Тест 1
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_pwd()
    sys.stdout = output
    if captured_output.getvalue().strip() == '/':
        print("Test 1 for cmd_pwd: success")
        results.append('pwd test 1 passed\n')
    else:
        print("Test 1 for cmd_pwd: error")
        results.append('pwd test 1 not passed\n')

    # Тест 2
    pwd = '/dir1'
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_pwd()
    sys.stdout = output
    if captured_output.getvalue().strip() == '/dir1':
        print("Test 2 for cmd_pwd: success")
        results.append("pwd test 2 passed\n")
    else:
        print("Test 2 for cmd_pwd: error")
        results.append("pwd test 2 not passed\n")
    pwd = '/'
    print()

    # Тесты для cmd_ls
    print("Testing cmd_ls:")
    # Очистим архив перед тестами
    with ZipFile(vfs_path, 'w') as file:
        pass  # Создаем пустой архив

    
    cmd_mkdir('dir1')
    pwd = '/'  # Установим начальный путь
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_ls()
    sys.stdout = output
    if captured_output.getvalue().strip() == 'dir1':
        print("Test 1 for cmd_ls: success")
        results.append("ls test 1 passed\n")
    else:
        print("Test 1 for cmd_ls: error")
        results.append("ls test 1 not passed\n")

    
    with ZipFile(vfs_path, 'w') as file:
        pass  # Создаем пустой архив
    cmd_mkdir('dir1')
    cmd_cd("dir1") 
    cmd_touch('file2')
    cmd_mkdir('dir2')
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_ls()
    sys.stdout = output

    if captured_output.getvalue().strip() == 'dir2\nfile2':
        print("Test 2 for cmd_ls: success")
        results.append("ls test 2 passed\n")
    else:
        print("Test 2 for cmd_ls: error")
        results.append("ls test 2 not passed\n")
    print()
    

    with ZipFile(vfs_path, 'w') as file:
        pass 
    
# Тесты для cmd_rm
    print("Testing cmd_rm:")
    #coздадим файл
    cmd_touch('rem')
    cmd_ls()
    # Удаляем файл
    cmd_rm('rem')
    print("pass1")
    
    
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_ls()
    sys.stdout = output
    cmd_ls()
    if 'rem' in captured_output.getvalue():
        print("Test 1 for cmd_rm: error")
        results.append("rm test 1 not passed\n")
    else:
        print("Test 1 for cmd_rm: success")
        results.append("rm test 1 passed\n")


    # Проверяем удаление несуществующего файла
    captured_output = StringIO()
    sys.stdout = captured_output
    result = cmd_rm('non_existent_file')
    sys.stdout = output
    if result == "rm: cannot remove 'non_existent_file': No such file or directory":
        print("Test 2 for cmd_rm: success")
        results.append("rm test 2 passed\n")
    else:
        print("Test 2 for cmd_rm: error")
        results.append("rm test 2 not passed\n")
    print()
    
    with ZipFile(vfs_path, 'w') as file:
        pass 
    

    # Тесты для cmd_cd
    print("Testing cmd_cd:")
    
    pwd = '/'  # Установ ленный путь
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_cd('dir4')  # Ожидаем: cd: no such file or directory
    sys.stdout = output
    if captured_output.getvalue().strip() == "cd: no such file or directory: dir4":
        print("Test 1 for cmd_cd: success")
        results.append("cd test 1 passed\n")
    else:
        print("Test 1 for cmd_cd: error")
        results.append("cd test 1 not passed \n ")
        
    #test 2 cd
    cmd_mkdir('dir1')
    cmd_ls()
    cmd_cd('dir1')  # Ожидаем: ничего не выводится, просто меняем путь
    cmd_pwd()
    if pwd == 'dir1/':
        print("Test 2 for cmd_cd: success")
        results.append("cd test 2 passed \n ")
    else:
        print("Test 2 for cmd_cd: error")
        results.append("cd test 2 not passed\n")

    cmd_cd('..')  # Возвращаемся на уровень выше
    if pwd == '/':
        print("Test 3 for cmd_cd: success")
        results.append("cd test 3 passed\n")
    else:
        print("Test 3 for cmd_cd: error")
        results.append("cd test 3 not passed\n")
    
    #test touch   
    #сброс вфс
    pwd = '/'
    with ZipFile(vfs_path, 'w') as file:
        pass
    print('cmd_touch: test 1')
    cmd_touch("touch_test")
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_ls()
    sys.stdout = output
    if "touch_test" in captured_output.getvalue().strip():
        print("Test 1 for cmd_touch: success")
        results.append("touch test 1 passed\n")
    else:
        print("Test 1 for cmd_touch: error")
        results.append("touch test 1 not passed\n")
    
    print('cmd_touch: test 2')
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_touch("touch_test")
    sys.stdout = output
    if captured_output.getvalue().strip() == "touch: 'touch_test' already exists" :
        print("test 2 for cmd_touch: success")
        results.append("touch test 2 passed\n")
    else:
        print("test 2 for cmd_touch: error")
        results.append("touch test 2 not passed\n")
        
    with ZipFile(vfs_path, 'w') as file:
        pass
    for each in results:
        print(each)
    
    
    

if __name__ == "__main__":
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
                    print(cmd_rm(args[0])) 
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
            elif cmd == 'test':
                cmd_test()
            elif cmd == 'touch':
                if args:
                    cmd_touch(args[0])
                else:
                    print("touch: missing argument")

            else:
                print(f"{cmd}: command not found")
                

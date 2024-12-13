import yaml
import os
import sys
from zipfile import ZipFile
from main import cmd_cd, cmd_exit, cmd_ls, cmd_mkdir, cmd_pwd, cmd_rm, cmd_touch
from io import StringIO  # Импортируем StringIO для захвата вывода
# Настройка
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

vfs_path = cfg.get('vfs_path', 'test.zip')
pwd = '/'
output_pwd = (cmd_pwd)

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
    
    #test mkdir
    
        print('cmd_mkdir: test 1')
    cmd_mkdir("mkdir_test")
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_ls()
    sys.stdout = output
    if "mkdir_test" in captured_output.getvalue().strip():
        print("Test 1 for cmd_mkdir: success")
        results.append("mkdir test 1 passed\n")
    else:
        print("Test 1 for cmd_mkdir: error")
        results.append("mkdir test 1 not passed\n")
    
    print('cmd_mkdir: test 2')
    captured_output = StringIO()
    sys.stdout = captured_output
    cmd_mkdir("mkdir_test")
    sys.stdout = output
    if captured_output.getvalue().strip() == "mkdir: cannot create directory 'mkdir_test': File exists" :
        print("test 2 for cmd_mkdir: success")
        results.append("mkdir test 2 passed\n")
    else:
        print("test 2 for cmd_mkdir: error")
        print (captured_output.getvalue().strip())
        results.append("mkdir test 2 not passed\n")
        
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
            elif cmd == 'test':
                cmd_test()
    



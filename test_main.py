import yaml
import os
import sys
import io
from zipfile import ZipFile
from main import cmd_cd, cmd_exit, cmd_ls, cmd_mkdir, cmd_pwd, cmd_rm, cmd_touch

# Настройка
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

vfs_path = cfg.get('vfs_path', 'test.zip')
pwd = '/'
output_pwd = (cmd_pwd)
def cmd_pwdtest():
    output_pwd = io.StringIO
    output_pwd = sys.stdout
    cmd_pwd()




def cmd_exit():
    exit()
cmd_pwdtest()
if output_pwd == '/':
    print('sucasess')
else:
    print(output_pwd)

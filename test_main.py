import unittest
import os
import shutil
from zipfile import ZipFile
import main
from unittest.mock import patch
from main import  cmd_ls, cmd_pwd, cmd_cd, cmd_mkdir, cmd_rm, cmd_touch



class TestVirtualShell(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_vfs = 'test_a.zip'
        main.vfs_path = cls.test_vfs
        main.pwd = '/'
        with ZipFile(cls.test_vfs, 'w') as file:
            pass

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_vfs):
            os.remove(cls.test_vfs)

    def setUp(self):
        with ZipFile(main.vfs_path, 'w') as file:
            pass

    def test_pwd(self):
        main.pwd = '/'
        with self.assertLogs() as log:
            main.cmd_pwd()
        self.assertIn('/', log.output[0])

    def test_ls_with_contents(self):
        # Создаём архив с некоторыми файлами и папками
        with ZipFile(main.vfs_path, 'w') as zip_file:
            zip_file.writestr('file1.txt', 'content1')
            zip_file.writestr('dir1/', '')  # Папка
            zip_file.writestr('dir1/file2.txt', 'content2')
        
        with patch('builtins.input', side_effect=['ls', 'exit']):
            with patch('builtins.print') as mocked_print:
                main()

        # Проверяем, что команда `ls` корректно отобразила содержимое
        mocked_print.assert_any_call('file1.txt')
        mocked_print.assert_any_call('dir1')




    def test_ls_nonempty(self):
        with ZipFile(main.vfs_path, 'a') as file:
            file.writestr('file1.txt', '')
            file.writestr('dir1/', '')
        with self.assertLogs() as log:
            main.cmd_ls()
        self.assertIn('file1.txt', log.output[0])
        self.assertIn('dir1', log.output[0])

    def test_rm_file(self):
        with ZipFile(main.vfs_path, 'a') as file:
            file.writestr('file1.txt', '')
        main.cmd_rm('file1.txt')
        with ZipFile(main.vfs_path, 'r') as file:
            self.assertNotIn('file1.txt', file.namelist())

    def test_rm_directory(self):
        with ZipFile(main.vfs_path, 'a') as file:
            file.writestr('dir1/', '')
            file.writestr('dir1/file.txt', '')
        main.cmd_rm('dir1')
        with ZipFile(main.vfs_path, 'r') as file:
            self.assertNotIn('dir1/', file.namelist())
            self.assertNotIn('dir1/file.txt', file.namelist())

    def test_cd_root(self):
        main.cmd_cd('/')
        self.assertEqual(main.pwd, '/')

    def test_cd_directory(self):
        with ZipFile(main.vfs_path, 'a') as file:
            file.writestr('dir1/', '')
        main.cmd_cd('dir1')
        self.assertEqual(main.pwd, 'dir1/')

    def test_mkdir(self):
        main.cmd_mkdir('new_dir')
        with ZipFile(main.vfs_path, 'r') as file:
            self.assertIn('new_dir/', file.namelist())

    def test_touch(self):
        main.cmd_touch('new_file.txt')
        with ZipFile(main.vfs_path, 'r') as file:
            self.assertIn('new_file.txt', file.namelist())

    def test_touch_existing(self):
        with ZipFile(main.vfs_path, 'a') as file:
            file.writestr('file.txt', '')
        with self.assertLogs() as log:
            main.cmd_touch('file.txt')
        self.assertIn("touch: 'file.txt' already exists", log.output[0])

    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.cmd_exit()


if __name__ == '__main__':
    unittest.main()

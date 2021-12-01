"""
This module provides communications tools
"""
from ftplib import FTP
from ftplib import error_perm
from pathlib import Path
import os


class FTP(FTP):
    def download(self, server_file_name, to_local_dir=None, blocksize=8192, rest=None):
        if to_local_dir is None:
            to_local_dir = os.getcwd()
        to_file_path = os.path.join(to_local_dir, os.path.split(server_file_name)[-1])
        print(f'downloading {server_file_name} to {to_file_path}')
        with open(to_file_path, 'wb') as fh:
            self.retrbinary(f'RETR {server_file_name}', fh.write, blocksize=blocksize, rest=rest)
        if self.size(server_file_name) != Path(to_file_path).stat().st_size:
            raise ValueError(f'File {to_file_path} not same size as server file. Potential corruption')
        print('download done')

    def upload(self, local_file_name, to_server_dir=None, blocksize=8192, rest=None):
        if to_server_dir is None:
            to_server_dir = '/'
        try:
            self.nlst(to_server_dir)
        except error_perm:
            raise SystemError(f'{to_server_dir} directory not available on server')
        to_file_path = os.path.join(to_server_dir, os.path.split(local_file_name)[-1])
        print(f'uploading {local_file_name} to {to_server_dir}')
        with open(local_file_name, 'rb') as fh:
            self.storbinary(f'STOR {to_file_path}', fh, blocksize=blocksize, rest=rest)
        if self.size(to_file_path) != Path(local_file_name).stat().st_size:
            raise ValueError(f'File {to_file_path} not same size as local file. Potential corruption')
        print('upload done')

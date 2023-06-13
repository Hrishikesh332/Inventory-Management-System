from __future__ import unicode_literals

import os
import hashlib


class FilePathInfo(object):
    """Give additional info around file path:

    >>> f = FilePathInfo('/path/to/my_file.txt')
    >>> f.file_name
    'my_file.txt'
    >>> f.file_extension
    'txt'
    >>> f.file_name_without_extension
    'my_file'
    >>> f.file_path_without_extension
    '/path/to/my_file'
    >>> f.file_path_without_name
    '/path/to/'
    """
    file_extension = None
    file_name = None
    file_name_without_extension = None
    file_path_without_extension = None
    file_path_without_name = None

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

        if value:
            self.file_path_with_name, self.file_extension = os.path.splitext(
                                                                        value)
            self.file_extension = self.file_extension.split('?')[0]
            self.file_name = os.path.basename(self._file_path).split('?')[0]

            if self.file_extension:

                name_no_ext = ''.join(self.file_name.rsplit(
                    self.file_extension, 1)
                )
                self.file_name_without_extension = name_no_ext

            path_no_ext = self.file_path.replace(self.file_extension, '')
            self.file_path_without_extension = path_no_ext

            if '.' in self.file_name:
                self.file_extension = self.file_name.rsplit('.')[-1]

            path_no_name = self.file_path.replace(self.file_name, '')
            self.file_path_without_name = path_no_name
        else:
            self.file_extension = None
            self.file_name = None
            self.file_name_without_extension = None
            self.file_path_without_extension = None
            self.file_path_without_name = None

    def is_file(self):
        return os.path.isfile(path=self.file_path)

    def __init__(self, file_path, **kwargs):
        self.file_path = file_path


def get_md5_for_file(file):
    """Get the md5 hash for a file.

    :param file: the file to get the md5 hash for
    """
    md5 = hashlib.md5()

    while True:
        data = file.read(md5.block_size)

        if not data:
            break

        md5.update(data)

    return md5.hexdigest()

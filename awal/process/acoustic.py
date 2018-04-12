"""Acoustic is for processing data at Acoustic level"""
import os


class Acoustic(object):
    """ Extracting Acoustic Features """
    roots_file_name = ''

    def __init__(self, roots_file_name):
        self.roots_file_name = roots_file_name

    def __string__(self):
        print('roots file name {}'.format(self.roots_file_name))

    def get_file_name(self):
        """ Getter  """
        return os.path.basename(self.roots_file_name)

    def get_ext_file_name(self):
        """  Getting Extension  """
        return os.path.splitext(self.roots_file_name)

    def set_file_name(self, roots_file_name):
        """" Setter  """
        self.roots_file_name = roots_file_name

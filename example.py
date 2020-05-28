""" This is the main script  """


#
# Pylint Tutorial
#

# from awal.managedcorpus import managed_corpus


# import os

# import roots


# class Car:
#     """ tutorial to learn how to us PyLint   """
#     color = ''
#     def __init__(self, color):
#         self.color = color
#     def __string__(self):
#         print(self.color)
#     def get_color(self):
#         """ Getter """
#         return self.color
#     def set_color(self, color):
#         """ Setter  """
#         self.color = color


# def crach(car1, car2):
#     """  Craching function is used to processing Car Object  """
#     car1.color = car2.color

import argparse
import os
import sys
from awal.utils.assessment.Phonemes import SAMPAPhonemes

from configparser import ConfigParser



#*************** II ***********************************************************************#
#parse defaults configuration files
#******************************************************************************************#
basedir=os.getcwd()
config = ConfigParser()
try:
    configFilePath=os.path.join(basedir,'default.cfg')
    config.read(configFilePath)
    ESPEAK_BIN=os.path.join(basedir,config.get('binary', 'espeak_bin'))
    POCKETSPHINX_BIN=os.path.join(basedir,config.get('binary', 'pocketsphinx_bin'))
except ConfigParser.NoSectionError:
    print("check the section name or config")




def build_arg_parser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("audio_file", help="audio file")
    parser.add_argument("text_file", help="text file")
    parser.add_argument('--language', dest='lang', default='fr')
    parser.add_argument('--model', dest='acmod',
                        default='/home/aghilas/Workspace/Experiments/Nadine/example/config', help='models directory')
    
   
    return parser

def main():
    args = build_arg_parser().parse_args()
    audio_file = args.audio_file
    text_file = args.text_file
    

    config = {
        'acmod': args.acmod,
        'PocketSphinx': POCKETSPHINX_BIN,
        'eSpeak': ESPEAK_BIN,
        'language': args.lang

    }
    print('********')
    print(audio_file)
    print('********')
    print(text_file)
    print('configuration :')
    print(config)
    with open(text_file,'r') as txtFile:
        for line in txtFile.readlines():
            sentence=line.strip().split()
            phonemes=SAMPAPhonemes().labels(sentence,language)
            
            



if __name__ == '__main__':
    main()

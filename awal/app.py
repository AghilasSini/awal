import sys
import os
import argparse
import roots



def build_args():
    parser=argparse.ArgumentParser(description=' language and speech toolkit...')
    parser.add_argument('-s',type='str',default='')
    return parser.parse_args()






def main():
    
    print('you have change...')
    print('on my way')
    rootsFilename=roots.Corpus()
    print(os.path.dirname())
def run():
    sys.exit(main(sys.argv[1:]))



if __name__ == '__main__':
    run()

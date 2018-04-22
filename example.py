""" This is the main script  """


#
#Pylint Tutorial
#

from awal.managedcorpus import managed_corpus
import os
import roots


class Car:
    """ tutorial to learn how to us PyLint   """
    color = ''
    def __init__(self, color):
        self.color = color
    def __string__(self):
        print(self.color)
    def get_color(self):
        """ Getter """
        return self.color
    def set_color(self, color):
        """ Setter  """
        self.color = color




def crach(car1, car2):
    """  Craching function is used to processing Car Object  """
    car1.color = car2.color

def main():
    """ main function  """
    my_car = Car('blue')
    crach(Car('red'), my_car)
    print('my new car color {}'.format(my_car.get_color()))
    """" managing roots corpus """
    
    rootsfilename="/home/aghilas/Workspace/data/data_120218/zola_germinal_15/zola_germinal_15_057_syl.json"
    if os.path.exists(rootsfilename):
        with managed_corpus(rootsfilename) as corpus:
            nbutts=corpus.count_utterances()
            utts=corpus.get_utterances(0,nbutts)
            for iutt,utt in enumerate(utts):
                seq_items=utt.get_sequence('Word Text').as_word_sequence().get_all_items()
                print(len(seq_items))
                utt.destroy()










if __name__ == '__main__':
    main()

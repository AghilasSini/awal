from contextlib import contextmanager
import roots
import os
@contextmanager
def managed_corpus(rootsfilename):
    try:
        corpus=roots.Corpus()
        corpus.load(rootsfilename)
        yield corpus
    finally:
        corpus.destroy()



def main():
    rootsfilename="/home/aghilas/Workspace/data/data_120218/zola_germinal_15/zola_germinal_15_057_syl.json"
    if os.path.exists(rootsfilename):
        with managed_corpus(rootsfilename) as corpus:
            nbutts=corpus.count_utterances()
            utts=corpus.get_utterances(0,nbutts)
            for iutt,utt in enumerate(utts):
                seq_items=utt.get_sequence('Word Text').as_word_sequence().get_all_items()
                print(len(seq_items))
                utt.destroy()
                
                
                
         
if __name__ == "__main__":
    main()


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


#!/usr/bin/python
#
# author: Aghilas SINI
# pseudo: asini
# mail  : aghilas.sini@irisa.fr
# date  : April,13th 2020
# Pronunciation assessment using Automatique Speech Recognition (ASR)/ Forced Alignment
# #

import os
import utils
from lib import GenerateJSpeechGrammar as jsgf
import subprocess
import shlex
import re
import math
import pandas
from genson import SchemaBuilder
import json
import numpy as np
import statistics
import re
import codecs
import librosa    
import soundfile as sf


def flatten(l): return [item for sublist in l for item in sublist]


def norm_score(log_score):
    if log_score < -8:
        nscore = 0.0
    elif log_score >= -8 and log_score < -7:
        nscore = 0.2
    elif log_score >= -7 and log_score < -6.7:
        nscore = 0.3
    elif log_score >= -6.7 and log_score < -6.5:
        nscore = 0.4    
    elif log_score >= -6.5 and log_score < -6.3:
        nscore = 0.5
    elif log_score >= -6.3 and log_score < -6.2:
        nscore = 0.6
    elif log_score >= -6.2 and log_score < -6.1:
        nscore = 0.7
    elif log_score >= -6.1 and log_score < -5.9:
        nscore = 0.8
    elif log_score >= -5.9 and log_score < -5.7:
        nscore = 0.9
    elif log_score >= -5.7:
        nscore = 1.0
    return nscore



def forcing_audio_properties(audio_file,audio_file_name):
    data, samplerate = sf.read(audiofile)
    data = data.T
    data = librosa.to_mono(data)
    data_16k = librosa.resample(data, samplerate, 16000)
    #overwrite wavfile
    sf.write(audio_file_name, data_16k,16000,subtype='PCM_16')




class SpeechRecognition():

    @staticmethod
    def scoring(config, sentence, phonemes, tmp_user):
        pocketsphinx_cmd = config["pocketsphinx"]

        # # # #
        phoneme_dict = config["phoneme_dict"]

        # no need for word dictionary
        # words_dict = config["words_dict"]
        acmod = config["acmod"]

     
        # remove accentuation  ... in the english case
        new_phonemes = []
        for word_phone in phonemes:
            phones = word_phone.split()
            new_phonemes.append(" ".join(
                [re.sub(r'[0-9]$', '', phone.lower()) for phone in flatten([ph.split() for ph in phones])]))

        phonemes = new_phonemes

        jsgfile = jsgf.GenerateJSpeechGrammar(sentence, phonemes, tmp_user)

        jsgfile.forcing()
        jsgfile.word()

        wbeam = ["1e-56", "1e-100", "1e-125", "1e-150", "1e-200", "1e-225", "1e-250",
                 "1e-270", "1e-300", "1e-325", "1e-350", "1e-400", "1e-450", "1e-500"]
        beam = ["1e-57", "1e-100", "1e-125", "1e-150", "1e-200", "1e-225", "1e-250",
                "1e-270", "1e-300", "1e-325", "1e-350", "1e-400", "1e-450", "1e-500"]

        niter = 0
        MAX_NITER = len(wbeam)
        success = False
        result = None

        # check the sampling rate
        # audiodata, samplerate = librosa.load(tmp_user.path("audiofile.wav"))
      
        # if len(audiodata.shape) > 1 or samplerate != 16000:
        #     audiodata = librosa.resample(librosa.to_mono(audiodata), samplerate, 16000)
        #     samplerate=16000


        # sf.write(tmp_user.path("audiofile_16k.wav"), audiodata,samplerate,subtype='PCM_16')
    
      



        while (not success) and niter < MAX_NITER:
            # # forced align at phoneme level
            cmd_forced_align = [pocketsphinx_cmd,
                                '-hmm', acmod,
                                '-infile', tmp_user.path("audiofile.wav"),
                                "-jsgf",   tmp_user.path(
                                    "speech_recognition/audiofile-forcing.jspf"),
                                "-dict", phoneme_dict,
                                "-backtrace", "yes",
                                "-fsgusefiller", "no",
                                "-wbeam", "{}".format(wbeam[niter]),
                                "-beam", "{}".format(beam[niter]),
                                "-remove_noise", "no"
                                ]
            result = subprocess.run(cmd_forced_align, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)


            # # word alignment

            words_dict = tmp_user.path("speech_recognition/words.dict")
            with codecs.open(words_dict, 'w', 'utf-8') as new_dict:
                for word, transcription in zip(sentence, phonemes):
                    new_dict.write('{} {}\n'.format(
                        word.lower(), transcription))
                new_dict.write('sil SIL')

            cmd_word_align = [pocketsphinx_cmd,
                              '-hmm', acmod,
                              '-infile', tmp_user.path("audiofile.wav"),
                              "-jsgf",   tmp_user.path(
                                  "speech_recognition/audiofile-word.jspf"),
                              "-dict", words_dict,
                              "-backtrace", "yes",
                              "-fsgusefiller", "no",
                              "-wbeam", "{}".format(wbeam[niter]),
                              "-beam", "{}".format(beam[niter]),
                              "-remove_noise", "no"
                              ]

            word_result = subprocess.run(cmd_word_align, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         universal_newlines=True)
            recognized_phoneset = result.stdout
            recognized_wordset = word_result.stdout

            with open(tmp_user.path("speech_recognition/audiofile-forcing.txt"), 'w') as outfile:
                outfile.writelines(result.stderr)

            # saving word align output

            with open(tmp_user.path("speech_recognition/audiofile-word.txt"), 'w') as word_outfile:
                word_outfile.writelines(word_result.stderr)

            # print(phoneset)
            # update the phoneset

            if recognized_phoneset != " " and recognized_wordset != " ":
                success = False
            else:
                success = True
            niter += 1

        # phonemes_scoring = []

        scoring = []
     
        with open(tmp_user.path("speech_recognition/audiofile-forcing.txt"), 'r') as infile:
            for line in infile.readlines():
                for phone in recognized_phoneset.split():
                    if line.startswith(("{} ".format(phone))):
                        phone, seg_beg, seg_end, _, score, _, _ = line.strip().split()
                        log_score = -math.log(1-float(score))
                        scoring.append(norm_score(log_score))

        score_phone_sent = 0.0

        if len(scoring) != 0:
            score_phone_sent = statistics.mean(scoring)

        word_scoring = []
        nword_scoring = []
        with open(tmp_user.path("speech_recognition/audiofile-word.txt"), 'r') as word_infile:
            for line in word_infile.readlines():
                for word in set(recognized_wordset.split()):
                    if line.startswith(("{} ".format(word))):
                        word, seg_beg, seg_end, _, score, _, _ = line.strip().split()
                        if word != 'sil':

                            word_score_norm = norm_score(
                                -math.log(1-float(score)))
                            word_scoring.append({
                                "score": word_score_norm,
                                "value": word

                            })
                            nword_scoring.append(word_score_norm)

        score_word_sent = 0.0
        if len(nword_scoring) > 0:
            score_word_sent = statistics.mean(nword_scoring)

        result = {

            "sentence": "{}".format(" ".join(sentence)),
            "score":  round((score_phone_sent+score_word_sent)/2, 3),
            "words":  word_scoring
        }

        return result, 200



def main():
        args=build_arg_parser().parse_args()
    roots_file_name=args.in_corpus[0]
    out_filename=args.out_filename[0]
    speaker_name=args.speaker_name[0]
    if os.path.exists(out_filename):
        print('this file exists')
        sys.exit(-1)
    else:
        print('output filename {}'.format(out_filename))
    config={
    'acmod':args.acmod,
    'pocketsphinx_bin':args.pocketsphinx_bin,
    'espeak_bin':args.espeak_bin
    }

if __name__ == '__main__':
    main()
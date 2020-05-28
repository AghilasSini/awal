import os
from lib import espeak
import utils

class Grapheme2Phonemes(object):

    @classmethod
    def aligned(cls,sentence,language,tmp_user):

        words = utils.arr_cleaning(sentence.replace(".","").split(" "))
        pron_dataJSON = utils.CONFIG["data"]["prononciation"][next(i for i,v in enumerate(utils.CONFIG["data"]["prononciation"]) if(v["language"] == language))]

        # Calcul Phonemes
        phonemes = espeak.get_raw_IPAPhoneme(sentence,language,ipa=3).split(" ")
        fcontent_gr = ""

        for phoneme, word in zip(phonemes,words):

            phoneme = phoneme.replace("_"," ").replace("-","").replace("ˈ","").replace("ˌ","")
            word = word.replace("?","").replace(",","").replace("!","").replace(";","").replace(":","")

            tmp_word = word[0].lower()
            for l in word[1:]:
                tmp_word = tmp_word + " " + l.lower()

            fcontent_gr = fcontent_gr + tmp_word + "\t" + phoneme + "\n"

        fcontent_gr = fcontent_gr[:(len(fcontent_gr) - 1)]

        tmp_user.create("grapheme")
        with open(tmp_user.path("grapheme/input.txt"),"w") as input_grapheme:
                input_grapheme.write(fcontent_gr)

        cmd_Gr = utils.CONFIG["binaries"]["m2m"]+" --maxX 3 --maxY 3 --delX --alignerIn "+pron_dataJSON["aligner"]+"  -i "+tmp_user.path("grapheme/input.txt")+" -o " + tmp_user.path("grapheme/output.txt")
        os.system(cmd_Gr)

        # récup les graph
        file_gr = open(tmp_user.path("grapheme/output.txt")).readlines()

        gr_match=[]
        for line_gr in file_gr:
            line_tab = line_gr.split("\t")
            tmp = line_tab[1].replace("\n","")

            # diphtongues EN
            tmp = tmp.replace("eɪ","e:ɪ").replace("aɪ","a:ɪ").replace("ɔɪ","ɔ:ɪ").replace("əʊ","ə:ʊ").replace("ɪə","ɪ:ə").replace("eə","e:ə").replace("ʊə","ʊ:ə")
            gr_match.append([line_tab[0].replace("|","").replace(":",""),line_tab[0],tmp])

        return gr_match

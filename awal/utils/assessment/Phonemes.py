import roots
import espeak
import utils

class Phonemes(object):

    IPA_Alphabet = roots.phonology_ipa_Ipa()

    @classmethod
    def recognition(cls,sentence,language):

        IPA_phonemes =[]
        for word in espeak.ipa_escape(espeak.get_raw_IPAPhoneme(sentence,language,ipa=1)).split(" "):
            for ph in word.split("_"):
                IPA_phonemes.append(espeak.convert_IPA_PhonSeq(espeak.extract_ipa(Phonemes.IPA_Alphabet,ph)))

        array_sentence = utils.arr_cleaning(sentence.replace(".","").split(" "))

        # FIX: Si language = French alors phonemes = ['j E v R I w @ U n'] sentence = ['hi', 'everyone'] => len(phonemes) diff len(sentence)
        if not(len(IPA_phonemes) == len(array_sentence)):
            IPA_phonemes =[]

            phonemeSent = ""
            for w in array_sentence:
                phonemeSent = phonemeSent + " " + espeak.get_raw_IPAPhoneme(w,language,ipa=1).replace(" ","")
            phonemeSent = phonemeSent[1:]

            for word in espeak.ipa_escape(phonemeSent).split(" "):
                for ph in word.split("_"):
                    IPA_phonemes.append(espeak.convert_IPA_PhonSeq(espeak.extract_ipa(Phonemes.IPA_Alphabet,ph)))


        return IPA_phonemes



class SAMPAPhonemes(Phonemes):

    SAMPA_Alphabet = roots.phonology_ipa_SampaAlphabet.get_instance()

    @classmethod
    def labels(cls,sentence,language):

        # Retrive Phonemes
        IPA_phonemes = super().recognition(sentence,language)
        SAMPA_phonemes = []

        # Conversion IPA vers SAMPA
        for phonemes in IPA_phonemes:
            res=""
            for phoneme in phonemes.get_all_items():
                tPhoneme = SAMPAPhonemes.SAMPA_Alphabet.approximate_phoneme(phoneme)
                tPhoneme=tPhoneme.replace("\\","")
                tPhoneme=tPhoneme.replace("%","")
                tPhoneme=tPhoneme.replace("\"","")
                tPhoneme=tPhoneme.replace("~","")

                if res == "":
                    res=tPhoneme
                else:
                    res=res+" "+tPhoneme

            SAMPA_phonemes.append(res)
            phonemes.destroy()

        return SAMPA_phonemes

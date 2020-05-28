# Service: Phonetisation via espeak en ayant des phonemes compatible avec IPA Alphabet
# Auteur: Cédric Fayet
# Description: Version 1 fix mineur des pb de phonétisation

import roots
import subprocess


def get_raw_IPAPhoneme(word, language,dict_config, ipa=1):
    eSpeak_CMD = dict_config["eSpeak"]

    # Phonétisation
    result = subprocess.run([eSpeak_CMD, '-v', language, word,
                             '-x', '-q', '--ipa='+str(ipa)], stdout=subprocess.PIPE)
    phoneme = result.stdout.decode("utf8")

    if phoneme[0] == " ":
        phoneme = phoneme[1:]

    # Suppression des éventuels cara de mise en page
    phoneme = phoneme.replace("\n", "")

    return phoneme


def ipa_escape(phoneme):

    # Suppression des symboles nn compa avec IPA Alphabet
    phoneme = phoneme.replace("-", "")
    phoneme = phoneme.replace("ə͡", "ə")
    phoneme = phoneme.replace("e͡", "e")
    phoneme = phoneme.replace("d͡", "d")
    phoneme = phoneme.replace("t͡", "t")
    phoneme = phoneme.replace("a͡", "a")
    phoneme = phoneme.replace("i͡", "i")
    phoneme = phoneme.replace("ʊ͡", "ʊ")
    phoneme = phoneme.replace("ɔ͡", "ɔ")
    phoneme = phoneme.replace("ɪ͡", "ɪ")
    phoneme = phoneme.replace("ǵ", "g")
    phoneme = phoneme.replace("o͡", "o")

    return phoneme


def extract_ipa(alphabet, phoneme):
    # Transformation en obj Roots pour faire le calcul de simi
    try:
        vipa = alphabet.extract_ipas(phoneme)
    except Exception as e:
        raise Exception(
            "Impossible de traiter la séquence de phonémes suivante:"+str(phoneme))

    return vipa


def convert_IPA_PhonSeq(vipa):

    seqPhoneme = roots.PhonemeSequence()
    for ipa in vipa:
        seqPhoneme.add(roots.phonology_Phoneme(ipa))

    return seqPhoneme


def get_vipa(word, language, alphabet, ipa=1):

    # Phonétisation
    phoneme = get_raw_IPAPhoneme(word, language, ipa)
    phoneme = ipa_escape(phoneme)
    return extract_ipa(alphabet, phoneme)


def get_phoneme(word, language, alphabet, ipa=1):

    vipa = get_vipa(word, language, alphabet, ipa)
    return convert_IPA_PhonSeq(vipa)

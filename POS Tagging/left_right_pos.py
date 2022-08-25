import regex as re
import malaya
import math
import pandas as pd
import nltk
import json
from nltk import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

model = malaya.pos.transformer(model = 'bert')

mal_noun = ["NOUN","PROPN"]
mal_pron = ["PRON"]
mal_verb = ["ADX","VERB"]
mal_adv = ["ADV"]
mal_adj = ["ADJ"]
mal_adp = ["ADP"]
mal_conj = ["CCONJ","SCONJ"]
mal_det = ["DET"]
mal_par = ["PART"]
mal_num = ["NUM"]
mal_sym = ["SYM"]
mal_oth = ["X"]

eng_noun = ["NN","NNP","NNPS","NNS"]
eng_pron = ["PRP","PRP$","WP","WP$"]
eng_verb = ["VB","VBD","VBG","VBN","VBP","VBZ","MD"]
eng_adv = ["RB","RBR","RBS"]
eng_adj = ["JJ","JJR","JJS"]
eng_adp = ["IN"]
eng_conj = ["CC"]
eng_det = ["DT","PDT","TO","EX"]
eng_par = ["RP"]
eng_num = ["CD"]
eng_sym = ["$","(",")",",","--",".",":","SYM","``","''"]
eng_oth = ["FW","LS","POS","UH"]

def mal_eng_pos(pos_mal,pos_eng,mal_eng):
    eng = ""
    if pos_eng in eng_noun:
        eng = "NOUN"
    elif pos_eng in eng_pron:
        eng = "PRON"
    elif pos_eng in eng_verb:
        eng = "VERB"
    elif pos_eng in eng_adv:
        eng = "ADVB"
    elif pos_eng in eng_adj:
        eng = "ADJC"
    elif pos_eng in eng_adp:
        eng = "ADPN"
    elif pos_eng in eng_conj:
        eng = "CONJ"
    elif pos_eng in eng_det:
        eng = "DETR"
    elif pos_eng in eng_par:
        eng = "PCLE"
    elif pos_eng in eng_num:
        eng = "NMBR"
    elif pos_eng in eng_sym:
        eng = "SYMB"
    else:
        eng = "OTHR"
    
    mal = ""
    if pos_mal in mal_noun:
        mal = "NOUN"
    elif pos_mal in mal_pron:
        mal = "PRON"
    elif pos_mal in mal_verb:
        mal = "VERB"
    elif pos_mal in mal_adv:
        mal = "ADVB"
    elif pos_mal in mal_adj:
        mal = "ADJC"
    elif pos_mal in mal_adp:
        mal = "ADPN"
    elif pos_mal in mal_conj:
        mal = "CONJ"
    elif pos_mal in mal_det:
        mal = "DETR"
    elif pos_mal in mal_par:
        mal = "PCLE"
    elif pos_mal in mal_num:
        mal = "NMBR"
    elif pos_mal in mal_sym:
        mal = "SYMB"
    else:
        mal = "OTHR"

    tag = mal + " || " + eng
    if tag in mal_eng.keys():
        mal_eng[tag] += 1
    else:
        mal_eng[tag] = 1
    
    return mal_eng

def eng_mal_pos(pos_mal,pos_eng,eng_mal):
    eng = ""
    if pos_eng in eng_noun:
        eng = "NOUN"
    elif pos_eng in eng_pron:
        eng = "PRON"
    elif pos_eng in eng_verb:
        eng = "VERB"
    elif pos_eng in eng_adv:
        eng = "ADVB"
    elif pos_eng in eng_adj:
        eng = "ADJC"
    elif pos_eng in eng_adp:
        eng = "ADPN"
    elif pos_eng in eng_conj:
        eng = "CONJ"
    elif pos_eng in eng_det:
        eng = "DETR"
    elif pos_eng in eng_par:
        eng = "PCLE"
    elif pos_eng in eng_num:
        eng = "NMBR"
    elif pos_eng in eng_sym:
        eng = "SYMB"
    else:
        eng = "OTHR"
    
    mal = ""
    if pos_mal in mal_noun:
        mal = "NOUN"
    elif pos_mal in mal_pron:
        mal = "PRON"
    elif pos_mal in mal_verb:
        mal = "VERB"
    elif pos_mal in mal_adv:
        mal = "ADVB"
    elif pos_mal in mal_adj:
        mal = "ADJC"
    elif pos_mal in mal_adp:
        mal = "ADPN"
    elif pos_mal in mal_conj:
        mal = "CONJ"
    elif pos_mal in mal_det:
        mal = "DETR"
    elif pos_mal in mal_par:
        mal = "PCLE"
    elif pos_mal in mal_num:
        mal = "NMBR"
    elif pos_mal in mal_sym:
        mal = "SYMB"
    else:
        mal = "OTHR"

    tag = eng + " || " + mal
    if tag in eng_mal.keys():
        eng_mal[tag] += 1
    else:
        eng_mal[tag] = 1
    
    return eng_mal

def tag_left_right(sentence, eng_mal, mal_eng):
    data = sentence.split()
    index = 0
    while index < len(data)-1:
        if not "</" in data[index]:
            index += 1
            continue
        mal_word = ""
        eng_word = ""
        pos_mal = ""
        pos_eng = ""
        if "<malay>" in data[index] and "</malay>" in data[index]:
            mal_word = data[index][7:-8]
            resulting_model_mal = model.analyze(mal_word)
            pos_mal = resulting_model_mal[0]["type"]
            if "<english>" in data[index+1] and "</english>" in data[index+1]:
                eng_word = data[index+1][9:-10]
            else:
                eng_word = data[index+1][9:]
            eng_word = word_tokenize(eng_word)
            resulting_model_eng = nltk.pos_tag(eng_word)
            pos_eng = resulting_model_eng[0][1]
            mal_eng = mal_eng_pos(pos_mal,pos_eng,mal_eng)
            index += 2
        elif "</malay>" in data[index]:
            mal_word = data[index][:-8]
            resulting_model_mal = model.analyze(mal_word)
            pos_mal = resulting_model_mal[0]["type"]
            if "<english>" in data[index+1] and "</english>" in data[index+1]:
                eng_word = data[index+1][9:-10]
            else:
                eng_word = data[index+1][9:]
            eng_word = word_tokenize(eng_word)
            resulting_model_eng = nltk.pos_tag(eng_word)
            pos_eng = resulting_model_eng[0][1]
            mal_eng = mal_eng_pos(pos_mal,pos_eng,mal_eng)
            index += 2

        elif "<english>" in data[index] and "</english>" in data[index]:
            eng_word = data[index][9:-10]
            eng_word = word_tokenize(eng_word)
            resulting_model_eng = nltk.pos_tag(eng_word)
            pos_eng = resulting_model_eng[0][1]
            if "<malay>" in data[index+1] and "</malay>" in data[index+1]:
                mal_word = data[index+1][7:-8]
            else:
                mal_word = data[index+1][7:]
            resulting_model_mal = model.analyze(mal_word)
            pos_mal = resulting_model_mal[0]["type"]
            eng_mal = eng_mal_pos(pos_mal,pos_eng,eng_mal)
            index += 2
        elif "</english>" in data[index]:
            eng_word = data[index][:-10]
            eng_word = word_tokenize(eng_word)
            resulting_model_eng = nltk.pos_tag(eng_word)
            pos_eng = resulting_model_eng[0][1]
            if "<malay>" in data[index+1] and "</malay>" in data[index+1]:
                mal_word = data[index+1][7:-8]
            else:
                mal_word = data[index+1][7:]
            resulting_model_mal = model.analyze(mal_word)
            pos_mal = resulting_model_mal[0]["type"]
            eng_mal = eng_mal_pos(pos_mal,pos_eng,eng_mal)
            index += 2
    return eng_mal, mal_eng

filenametrain = "Train_POS.txt"
with open(filenametrain) as f:
    datatrain = f.readlines()

eng_mal_train = dict()
mal_eng_train = dict()
for sentence in datatrain:
    if "<english>" in sentence or "<malay>" in sentence:
        eng_mal_train, mal_eng_train = tag_left_right(sentence, eng_mal_train, mal_eng_train)

json.dump(eng_mal_train, open("eng_mal_train.txt",'w'))
json.dump(mal_eng_train, open("mal_eng_train.txt",'w'))

filenamevalidation = "Vaidation_POS.txt"
with open(filenamevalidation) as f:
    datavalidation = f.readlines()

eng_mal_validation = dict()
mal_eng_validation = dict()
for sentence in data:
    if "<english>" in sentence or "<malay>" in sentence:
        eng_mal_validation, mal_eng_validation = tag_left_right(sentence, eng_mal_validation, mal_eng_validation)

json.dump(eng_mal_validation, open("eng_mal_validation.txt",'w'))
json.dump(mal_eng_validation, open("mal_eng_validation.txt",'w'))


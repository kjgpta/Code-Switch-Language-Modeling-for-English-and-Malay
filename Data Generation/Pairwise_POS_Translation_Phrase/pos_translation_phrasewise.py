# Installing and Importing required libraries

import malaya
from random import *
import nltk
import tensorflow as tf
import pandas as pd
from nltk import word_tokenize
from deep_translator import GoogleTranslator
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

model = malaya.pos.transformer(model = 'bert')

# Importing the required data from real Codeswitch data
df1 = pd.read_excel('Left_Right_POS_English.xlsx')
df2 = pd.read_excel('Left_Right_POS_Malay.xlsx')

msdf = pd.read_csv("Malay_Substitutes.csv")
msdf.columns = ["Index", "Standard words", "Accepted words"]
standard_words = list(msdf["Standard words"])
accepted_words = list(msdf["Accepted words"])

eng_mal = dict()
for i in range(int(df1.index[-1])+1):
    eng_mal[df1.at[i,"POS || POS"]] =  df1.at[i,"English to Malay Conversion Ratio"]

mal_eng = dict()
for i in range(int(df2.index[-1])+1):
    mal_eng[df2.at[i,"POS || POS"]] =  df2.at[i,"Malay to English Conversion Ratio"]

# Converting Monolingual Malay sentences to Code-switch English-Malay Sentence

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
mal_oth = ["X", "PUNCT"]

def malPOS(pos_mal):
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
    
    return mal


def malay_array_generator(string_mal):
    resulting_model = model.predict(string_mal)
    eng_ar = []
    mal_ar = []
    left_flag = False # False --> Malay and True --> English word
    flag = False # False --> 1st word is malay
    if len(resulting_model) == 1:
        txt = resulting_model[0][0]
        if randint(0, 100) > 50:
            eng_ar.append(txt)
        else:
            mal_ar.append(txt)
    else:
        eng = ""
        mal = ""
        for i in range(len(resulting_model)-1):
              left_txt = resulting_model[i][0]
              left_pos = resulting_model[i][1]
              if i == 0:
                  if randint(0, 100) > 50:
                      eng += left_txt+ " "
                      left_flag = True
                      flag = True
                  else:
                      mal += left_txt+ " "
              right_txt = resulting_model[i+1][0]
              right_pos = resulting_model[i+1][1]
              tag = malPOS(left_pos) + " || " + malPOS(right_pos)
              if left_flag == False:
                  if tag in mal_eng.keys():
                      threshold = mal_eng[tag]
                  else:
                      threshold = 0
              else:
                  if tag in eng_mal.keys():
                      threshold = eng_mal[tag]
                  else:
                      threshold = 0
              rand = randint(0, 100)
              if rand > threshold:
                  left_flag = True
                  if eng == "":
                      mal_ar.append(mal)
                      mal = ""
                  eng += right_txt + " "
              else:
                  left_flag = False
                  if mal == "":
                      eng_ar.append(eng)
                      eng = ""
                  mal += right_txt + " "
        if eng == "":
            mal_ar.append(mal)
        else:
            eng_ar.append(eng)  
    return eng_ar, mal_ar, flag

def malay_sentence(eng_ar, mal_ar, flag):
    sentence = ""
    i = 0
    j = 0
    if len(eng_ar) != 0 and flag:
        while i < len(eng_ar) or j < len(mal_ar):
            if i < len(eng_ar):
                try: 
                    sentence += GoogleTranslator(source='ms', target='en').translate(eng_ar[i][:-1]) + " "
                except: 
                    sentence += eng_ar[i][:-1] + " "
                i += 1
            if j < len(mal_ar):
                sentence += mal_ar[j][:-1] + " "
                j += 1
    else:
        while i < len(eng_ar) or j < len(mal_ar):
            if j < len(mal_ar):
                sentence += mal_ar[j][:-1] + " "
                j += 1
            if i < len(eng_ar):
                try:
                    sentence += GoogleTranslator(source='ms', target='en').translate(eng_ar[i][:-1]) + " "
                except:
                    sentence += eng_ar[i][:-1] + " "
                i += 1
    return sentence

malay_text = []
with open('Malay_Normalized.txt') as f:
    malay_text = f.readlines()
f.close()

malay_cs = []
for i in range(len(malay_text)):
    string_mal = malay_text[i]
    eng_ar, mal_ar, flag = malay_array_generator(string_mal)
    if string_mal != "\n":
        sentence = malay_sentence(eng_ar, mal_ar, flag)
        malay_cs.append(sentence)

malay_cs_arr = []
for i in malay_cs:
        txt = ""
        for j in range(len(standard_words)):
            txt = i.replace(standard_words[j], accepted_words[j])
        t = txt.split()
        malay_cs_arr.append(" ".join(t))

malay_cs_text = ""
for i in malay_cs_arr:
    malay_cs_text += i + '\n'

f1 = open('Malay_CS.txt','w+')
f1.write(malay_cs_text)
f1.close()


# Converting Monolingual English sentences to Code-switch English-Malay Sentence

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

def engPOS(pos_eng):
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
    
    return eng

def english_array_generator(string_eng):
    sentence_eng = word_tokenize(string_eng)
    resulting_model = nltk.pos_tag(sentence_eng)    
    eng_ar = []
    mal_ar = []
    left_flag = True # False --> Malay and True --> English word
    flag = True # True --> 1st word is English
    if len(resulting_model) == 1:
        txt = resulting_model[0][0]
        if randint(0, 100) > 50:
            mal_ar.append(txt)
        else:
            eng_ar.append(txt)
    else:
        eng = ""
        mal = ""
        for i in range(len(resulting_model)-1):
              left_txt = resulting_model[i][0]
              left_pos = resulting_model[i][1]
              if i == 0:
                  if randint(0, 100) > 50:
                      mal += left_txt+ " "
                      left_flag = False
                      flag = False
                  else:
                      eng += left_txt+ " "
              right_txt = resulting_model[i+1][0]
              right_pos = resulting_model[i+1][1]
              tag = engPOS(left_pos) + " || " + engPOS(right_pos)
              if left_flag == False:
                  if tag in mal_eng.keys():
                      threshold = mal_eng[tag]
                  else:
                      threshold = 0
              else:
                  if tag in eng_mal.keys():
                      threshold = eng_mal[tag]
                  else:
                      threshold = 0
              rand = randint(0, 100)
              if rand > threshold:
                  left_flag = False
                  if mal == "":
                      eng_ar.append(eng)
                      eng = ""
                  mal += right_txt + " "
              else:
                  left_flag = True
                  if eng == "":
                      mal_ar.append(mal)
                      mal = ""
                  eng += right_txt + " "
        if eng == "":
            mal_ar.append(mal)
        else:
            eng_ar.append(eng)  
    return eng_ar, mal_ar, flag

def english_sentence(eng_ar, mal_ar, flag):
    sentence = ""
    i = 0
    j = 0
    if len(eng_ar) != 0 and flag:
        while i < len(eng_ar) or j < len(mal_ar):
            if i < len(eng_ar):
                sentence += eng_ar[i][:-1] + " "
                i += 1
            if j < len(mal_ar):
                try: 
                    sentence += GoogleTranslator(source='en', target='ms').translate(mal_ar[j][:-1]) + " "
                except: 
                    sentence += mal_ar[j][:-1] + " "
                j += 1
    else:
        while i < len(eng_ar) or j < len(mal_ar):
            if j < len(mal_ar):
                try: 
                    sentence += GoogleTranslator(source='en', target='ms').translate(mal_ar[j][:-1]) + " "
                except: 
                    sentence += mal_ar[j][:-1] + " "
                j += 1
            if i < len(eng_ar):
                sentence += eng_ar[i][:-1] + " "
                i += 1
    return sentence

english_text = []
with open('English_Normalized.txt') as f:
    english_text = f.readlines()
f.close()

english_cs = []
for i in range(len(english_text)):
    string_eng = english_text[i]
    eng_ar, mal_ar, flag = english_array_generator(string_eng)
    if string_eng != "\n":
        sentence = english_sentence(eng_ar, mal_ar, flag)
        english_cs.append(sentence)

english_cs_arr = []
for i in english_cs:
        txt = ""
        for j in range(len(standard_words)):
            txt = i.replace(standard_words[j], accepted_words[j])
        t = txt.split()
        english_cs_arr.append(" ".join(t))

english_cs_text = ""
for i in english_cs_arr:
    english_cs_text += i + '\n'

f1 = open('English_CS.txt','w+')
f1.write(english_cs_text)
f1.close()
'''

Generates the code switched English/Malay Data from monolingual English and Malay Data 

Input File details:

Text files "imda5eng.txt" and "imda5mal.txt" is already normalized of extra spaces, repeated words/phrases (from preprocessing script)
Excel files "POS_English.xlsx" and "POS_Malay.xlsx" are already provided in the directory, these files consists of results of pair wise tagging which we are using while generating Code switched data.
CSV file "malaywords.csv" consists of words and its accepted form

Packages to be installed: 
1. h5py              :  pip install h5py
2. typing-extensions :  pip install typing-extensions
3. wheel             :  pip install wheel
4. imgaug            :  pip install imgaug==0.2.5
5. malaya            :  pip install malaya
6. tensorflow==2.9.0 :  pip install tensorflow==2.9.0
7. tensorflow_addons :  pip install tensorflow_addons
8. transformers      :  pip install transformers

Output File details: 
"CS_English.txt" contains Code-Switched data generated from Monolingual English Data
"CS_Malay.txt" contains Code-Switched data generated from Monolingual Malay Data

Author: Kshitij Gupta
Email: mailguptakshitij@gmail.com
Date: 25 August 2022

'''

# Importing required libraries
import malaya
import tensorflow as tf
import pandas as pd
import random
import nltk
from nltk import word_tokenize
from random import *
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

# Importing POS Tagging Model, English to Malay Alignment Model, Malay to English Alignment Model
model = malaya.pos.transformer(model = 'bert')
alignment_en_ms = malaya.alignment.en_ms.huggingface()
alignment_ms_en = malaya.alignment.ms_en.huggingface()

# Saving the monolingual english sentences from "imda5eng.txt" in english_text array 
english_text = []
with open('imda5eng.txt') as f:
    english_text = f.readlines()
f.close()

# Saving the monolingual malay sentences from "imda5mal.txt" in malay_text array 
malay_text = []
with open('imda5mal.txt') as f:
    malay_text = f.readlines()
f.close()

# Storing information regarding malay words and their shortened/accepted forms of word
msdf = pd.read_csv("malaywords.csv")
msdf.columns = ["Standard Word", "Accepted Word"]
standard_words = list(msdf["Standard Word"])
accepted_words = list(msdf["Accepted Word"])


# Reading the pairwise part of speech results in both English and Malay 
df1 = pd.read_excel('POS_English.xlsx')
df2 = pd.read_excel('POS_Malay.xlsx')

# Creating the dictionary which stores the pairwise part of speech results in both English and Malay 
eng_mal = dict()
for i in range(int(df1.index[-1])+1):
    eng_mal[df1.at[i,"POS || POS"]] =  df1.at[i,"English to Malay Conversion Ratio"]

mal_eng = dict()
for i in range(int(df2.index[-1])+1):
    mal_eng[df2.at[i,"POS || POS"]] =  df2.at[i,"Malay to English Conversion Ratio"]


''' 
English POS tags stored are distributed among 12 categories  
1. Noun
2. Pronoun
3. Verb
4. Adverb
5. Adjective
6. Adposition 
7. Conjunction
8. Determiner
9. Particle
10. Number
11. Symbol
12. Other
'''

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


# Function for getting information about category to which our POS belong
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


# Now, we will be converting our monolingual English to Code switched English/Malay
english_cs_text = []
n = len(english_text)
for l in range(n):
    string_eng = english_text[l]
    string_mal = malay_text[l]
    sentence_eng = word_tokenize(string_eng)
    resulting_model_eng = nltk.pos_tag(sentence_eng)
    resulting_alignment_model = alignment_en_ms.align([string_eng], [string_mal], align_layer = 7)
    left_splitted = string_eng.split()
    right_splitted = string_mal.split()
    codeswitch_english_sentence = ""
    left_flag = False # False --> English and True --> Malay word
    for i in range(len(resulting_model_eng)-1):
        left_txt = resulting_model_eng[i][0]
        left_pos = resulting_model_eng[i][1]
        right_txt = resulting_model_eng[i+1][0]
        right_pos = resulting_model_eng[i+1][1]
        tag = engPOS(left_pos) + " || " + engPOS(right_pos)
        if i == 0:
            codeswitch_english_sentence += left_txt + ' '
        if left_flag == False:
            if tag in eng_mal.keys():
                threshold = eng_mal[tag]
            else:
                threshold = 0
        else:
            if tag in mal_eng.keys():
                threshold = mal_eng[tag]
            else:
                threshold = 0
        rand = randint(0, 100)
        if rand > threshold:
            left_flag = True
            lst = ""
            for k in resulting_alignment_model[0]:
                if k[0] == i+1:
                    lst += right_splitted[k[1]] + " "
            codeswitch_english_sentence +=  lst + ' '
        else:
            left_flag = False
            codeswitch_english_sentence += right_txt + " "
    english_cs_text.append(codeswitch_english_sentence)


# Now, we will be converting our monolingual Malay to Code switched English/Malay
malay_cs_text = []
n = len(malay_text)
for l in range(n):
    string_eng = english_text[l]
    string_mal = malay_text[l]
    resulting_model = model.predict(string_mal)
    resulting_alignment_model = alignment_ms_en.align([string_mal], [string_eng], align_layer = 7)
    left_splitted = string_mal.split()
    right_splitted = string_eng.split()
    codeswitch_malay_sentence = ""
    left_flag = False # False --> Malay and True --> English word
    for i in range(len(resulting_model)-1):
        left_txt = resulting_model[i][0]
        left_pos = resulting_model[i][1]
        right_txt = resulting_model[i+1][0]
        right_pos = resulting_model[i+1][1]
        tag = malPOS(left_pos) + " || " + malPOS(right_pos)
        if i == 0:
            codeswitch_malay_sentence += left_txt + ' '
        if left_flag == False:
            if tag in mal_eng.keys():
                threshold = mal_eng[tag]
            else:
                threshold = 0
        else:
            if tag in eng_mal.keys():
                threshold = mal_eng[tag]
            else:
                threshold = 0
        rand = randint(0, 100)
        if rand > threshold:
            left_flag = False
            lst = ""
            for k in resulting_alignment_model[0]:
                if k[0] == i+1:
                    lst += right_splitted[k[1]] + " "
            codeswitch_malay_sentence +=  lst + ' '
        else:
            left_flag = True
            codeswitch_malay_sentence += right_txt + " "
    malay_cs_text.append(codeswitch_malay_sentence)


# Replacing words with their accepted/short form of words
english_cs_arr = []
for i in english_cs_text:
    txt = ""
    for j in range(len(standard_words)):
        txt = i.replace(standard_words[j], accepted_words[j].lower())
        txt = txt.replace(standard_words[j].lower(), accepted_words[j].lower())
    t = txt.split()
    english_cs_arr.append(" ".join(t))

malay_cs_arr = []
for i in malay_cs_text:
    txt = ""
    for j in range(len(standard_words)):
        txt = i.replace(standard_words[j], accepted_words[j].lower())
        txt = txt.replace(standard_words[j].lower(), accepted_words[j].lower())
    t = txt.split()
    malay_cs_arr.append(" ".join(t))

# Saving the Code-Switched data files for English and Malay
english_cs = ""
for i in english_cs_arr:
    english_cs += i + '\n'
filename = "CS_English.txt"
f1 = open(filename, "w+")
f1.write(english_cs)
f1.close()

malay_cs = ""
for i in malay_cs_arr:
    malay_cs += i + '\n'
filename = "CS_Malay.txt"
f2 = open(filename, "w+")
f2.write(malay_cs)
f2.close()
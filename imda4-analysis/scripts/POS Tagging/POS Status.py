"""
Code for checking POS tags of each phrase and increment the count according to those tags.
Contains function for checking POS tags of English and Malay respectively

Requirements:
    1. Malay Library
    2. NLTK
    3. REGEX


"""
import regex as re
import malaya
import nltk
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

def english_pos(phrase,english_arr):
            phrase = re.sub(r'[^\w\s]', '', phrase)
            tokenized_sentence = word_tokenize(phrase)
            resulting_model = nltk.pos_tag(tokenized_sentence)
            for i in range(len(resulting_model)):
                pos = resulting_model[i][1]
                if pos in eng_noun:
                    english_arr[0] += 1
                elif pos in eng_pron:
                    english_arr[1] += 1
                elif pos in eng_verb:
                    english_arr[2] += 1
                elif pos in eng_adv:
                    english_arr[3] += 1
                elif pos in eng_adj:
                    english_arr[4] += 1
                elif pos in eng_adp:
                    english_arr[5] += 1
                elif pos in eng_conj:
                    english_arr[6] += 1
                elif pos in eng_det:
                    english_arr[7] += 1
                elif pos in eng_par:
                    english_arr[8] += 1
                elif pos in eng_num:
                    english_arr[9] += 1
                elif pos in eng_sym:
                    english_arr[10] += 1
                else:
                    english_arr[11] += 1
            return english_arr

def malay_pos(phrase, malay_arr):
            phrase = re.sub(r'[^\w\s]', '', phrase)
            resulting_model = model.analyze(phrase)
            for i in range(len(resulting_model)):
                pos = resulting_model[i]["type"]
                if pos in mal_noun:
                    malay_arr[0] += 1
                elif pos in mal_pron:
                    malay_arr[1] += 1
                elif pos in mal_verb:
                    malay_arr[2] += 1
                elif pos in mal_adv:
                    malay_arr[3] += 1
                elif pos in mal_adj:
                    malay_arr[4] += 1
                elif pos in mal_adp:
                    malay_arr[5] += 1
                elif pos in mal_conj:
                    malay_arr[6] += 1
                elif pos in mal_det:
                    malay_arr[7] += 1
                elif pos in mal_par:
                    malay_arr[8] += 1
                elif pos in mal_num:
                    malay_arr[9] += 1
                elif pos in mal_sym:
                    malay_arr[10] += 1
                else:
                    malay_arr[11] += 1
            return malay_arr


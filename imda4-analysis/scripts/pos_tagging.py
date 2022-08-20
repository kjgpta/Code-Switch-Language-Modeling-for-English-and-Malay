"""

"""

!pip -q install h5py
!pip -q install typing-extensions
!pip -q install wheel
!pip -q install imgaug==0.2.5
!pip -q install malaya
!pip -q install tensorflow==2.9.0
!pip -q install tensorflow_addons
!pip -q install xlsxwriter

import regex as re
import malaya
import math
import pandas as pd
import nltk
import xlsxwriter
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

order = ["Noun", "Pronoun", "Verb", "Adverb", "Adjective", "Adposition", "Conjunction", "Determiner", "Particle", "Number", "Symbol", "Other", "Total"]
head = ["Part of Speech", "No of English Words", "No of Malay Words","Total no of Words", "Substitution Rate", "CMI", "M-Index", "Language Entropy"]
n = len(order)

english_re = []
malay_re = []
engSpa = []
malSpa = []
otherLan = []
interject = []

workbook = xlsxwriter.Workbook('/content/drive/MyDrive/Thesis/IMDA_4/Text/Results.xlsx')
results = workbook.add_worksheet("Results")

results.write('A2', 'Different Room Results')

results.write('B3', 'Dataset')
results.write('C3', 'English Substitution Rate')
results.write('D3', 'CMI')
results.write('E3', 'Multilingual index')
results.write('F3', 'Language Entropy')
results.write('G3', 'Integration Index')
results.write('H3', 'Burstiness')
results.write('I3', 'Memory')

results.write('B4', 'Training Data')
results.write('B5', 'Validation Data')
results.write('B6', 'Total Data')

results.write('A8', 'Same Room Results')

results.write('B9', 'Dataset')
results.write('C9', 'English Substitution Rate')
results.write('D9', 'CMI')
results.write('E9', 'Multilingual index')
results.write('F9', 'Language Entropy')
results.write('G9', 'Integration Index')
results.write('H9', 'Burstiness')
results.write('I9', 'Memory')

results.write('B10', 'Training Data')
results.write('B11', 'Validation Data')
results.write('B12', 'Total Data')

results.write('A15', 'All Combined Results')

results.write('B16', 'Dataset')
results.write('C16', 'English Substitution Rate')
results.write('D16', 'CMI')
results.write('E16', 'Multilingual index')
results.write('F16', 'Language Entropy')
results.write('G16', 'Integration Index')
results.write('H16', 'Burstiness')
results.write('I16', 'Memory')

results.write('B17', 'Training Data')
results.write('B18', 'Validation Data')
results.write('B19', 'Total Data')

import math
def analyzer(english_arr,malay_arr):
    k = []
    for i in range(n-1):
        if english_arr[i] == 0 and malay_arr[i] == 0:
            k.append([order[i], english_arr[i], malay_arr[i], english_arr[i]+malay_arr[i], "NA", "NA", "NA", "NA"])
        else:
            P_eng = english_arr[i]/(english_arr[i] + malay_arr[i])
            P_mal = 1 - P_eng
            eng_substitution_rate = "{:.2f}".format(P_eng * 100)
            CMI = "{:.2f}".format(100 * (1 - (max(P_eng,P_mal)) ))
            M_index = "{:.2f}".format((1 - (P_eng**2 + P_mal**2))/(P_eng**2 + P_mal**2))
            LE = 0
            if P_eng == 0:
                LE = "{:.2f}".format(-(P_mal*math.log(P_mal,2)))
            elif P_mal == 0:
                LE = "{:.2f}".format(-(P_eng*math.log(P_eng,2)))
            else:
                LE = "{:.2f}".format(-(P_eng*math.log(P_eng,2) + P_mal*math.log(P_mal,2)))
            k.append([order[i], english_arr[i], malay_arr[i], english_arr[i]+malay_arr[i], eng_substitution_rate,CMI,M_index,LE])
    eng = sum(english_arr)
    mal = sum(malay_arr)
    if eng == 0 and mal == 0:
        k.append([order[-1], eng, mal, eng+mal, "NA", "NA", "NA", "NA"])
    else:
        P_eng = eng/(eng+mal)
        P_mal = 1 - P_eng
        eng_substitution_rate = "{:.2f}".format(P_eng * 100)
        CMI = "{:.2f}".format(100 * (1 - (max(P_eng,P_mal)) ))
        M_index = "{:.2f}".format((1 - (P_eng**2 + P_mal**2))/(P_eng**2 + P_mal**2))
        if P_eng == 0:
            LE = "{:.2f}".format(-(P_mal*math.log(P_mal,2)))
        elif P_mal == 0:
            LE = "{:.2f}".format(-(P_eng*math.log(P_eng,2)))
        else:
            LE = "{:.2f}".format(-(P_eng*math.log(P_eng,2) + P_mal*math.log(P_mal,2)))
        k.append([order[-1], eng, mal, eng+mal, eng_substitution_rate,CMI,M_index,LE])
    df = pd.DataFrame(k, columns = head).set_index('Part of Speech')
    return df, eng_substitution_rate, CMI, M_index, LE

def pos_tagger(filepath,filetosavetext):
    eng_span = []
    mal_span = []
    with open(filepath) as f:
        data = f.readlines()
    f.close()
    english_ar = [0]*(n-1)
    malay_ar = [0]*(n-1)
    other_lang = 0
    inter_lang = 0
    phrase_data = ""
    for line in data:
        list_phrase = []
        malay_flag = False
        eng_flag = False
        other_flag = False
        inter_flag = False
        phrase = ""
        words = line.split()
        if words[0][0] == "#":
            other_flag = True
        elif words[0][0] == "!":
            inter_flag = True
        elif words[0].startswith("<malay>"):
            malay_flag = True
        else:
            eng_flag = True
        for i in words:
            if other_flag or i[0] == "#" or i[0] == "!":
                if phrase != "" and not other_flag:
                    list_phrase.append("<english>" + phrase[:-1] + "</english>")
                    english_ar = english_pos(phrase,english_ar)
                    eng_span.append(len(phrase.split()))
                    phrase = ""
                    eng_flag = False
                other_flag = True
                other_lang += 1
                if (i[0] == "#" and i[-1] == "#"):
                    phrase = ""
                    phrase += i[1:-1]
                    list_phrase.append("<other_language>" + phrase + "</other_language>")
                    phrase = ""
                    other_flag = False
                elif i[0] == "#":
                    phrase = ""
                    phrase += i[1:] + " "
                elif i[-1] == "#":
                    phrase += i[:-1]
                    list_phrase.append("<other_language>" + phrase + "</other_language>")
                    phrase = ""
                    other_flag = False
                elif other_flag:
                    phrase += i + " "
            elif inter_flag or i[0] == "!":
                if phrase != "" and not other_flag:
                    list_phrase.append("<english>" + phrase[:-1] + "</english>")
                    english_ar = english_pos(phrase,english_ar)
                    eng_span.append(len(phrase.split()))
                    phrase = ""
                    eng_flag = False
                inter_flag = True
                inter_lang += 1
                if (i[0] == "!" and i[-1] == "!"):
                    phrase = ""
                    phrase += i[1:-1]
                    list_phrase.append("<interjection>" + phrase + "</interjection>")
                    phrase = ""
                    inter_flag = False
                elif i[0] == "!":
                    phrase = ""
                    phrase += i[1:] + " "
                elif i[-1] == "!":
                    phrase += i[:-1]
                    list_phrase.append("<interjection>" + phrase + "</interjection>")
                    phrase = ""
                    inter_flag = False
                elif inter_flag:
                    phrase += i + " "
            elif malay_flag or i.startswith("<malay>"):
                if phrase != "" and not malay_flag:
                      list_phrase.append("<english>" + phrase[:-1] + "</english>")
                      english_ar = english_pos(phrase,english_ar)
                      eng_span.append(len(phrase.split()))
                      phrase = ""
                      eng_flag = False
                malay_flag = True
                if i.startswith("<malay>") and i.endswith("</malay>"):
                    phrase = ""
                    phrase += i[7:-8]
                    list_phrase.append("<malay>" + phrase + "</malay>")
                    malay_ar = malay_pos(phrase,malay_ar)
                    mal_span.append(len(phrase.split()))
                    phrase = ""
                    malay_flag = False
                elif i.startswith("<malay>"):
                    phrase = ""
                    phrase += i[7:] + " "
                elif i.endswith("</malay>"):
                    phrase += i[:-8]
                    list_phrase.append("<malay>" + phrase + "</malay>")
                    malay_ar = malay_pos(phrase,malay_ar)
                    mal_span.append(len(phrase.split()))
                    phrase = ""
                    malay_flag = False
                elif malay_flag:
                    phrase += i + " "
            else:
                eng_flag = True
                phrase += i + " "
        if phrase != "":
            list_phrase.append("<english>" + phrase[:-1] + "</english>")
            english_ar = english_pos(phrase,english_ar)
            eng_span.append(len(phrase.split()))
            phrase = ""
            eng_flag = False
        for j in list_phrase:
            phrase_data += j + " "
        phrase_data += "\n"
    f1 = open(filetosavetext,'w+')
    f1.write(phrase_data)
    f1.close()  
    return [english_ar, malay_ar, eng_span, mal_span, other_lang, inter_lang]

import statistics
import numpy as np
def span_metrics(english_span,malay_span):
    I_index = (len(english_span) + len(malay_span) - 1)/(sum(english_span)+sum(malay_span)-1) 
    span = english_span
    span += malay_span
    std_eng = statistics.stdev(english_span)
    std_mal = statistics.stdev(malay_span)
    mean_eng = statistics.mean(english_span)
    mean_mal = statistics.mean(malay_span)
    std = statistics.stdev(span)
    mean = statistics.mean(span)
    burstiness = (std-mean)/(std+mean)
    new_eng_span = np.array(english_span)
    new_mal_span = np.array(malay_span)
    eng_len = len(english_span)
    mal_len = len(malay_span)
    if eng_len > mal_len:
      np.pad(new_mal_span,(0,eng_len-mal_len))
    elif mal_len>eng_len:
      np.pad(new_eng_span,(0,mal_len-eng_len))
    memory = np.correlate(new_eng_span, new_mal_span)[0]
    return I_index, burstiness, memory

def convert_list(elements):
  k = []
  for i in elements:
    if str(type(i)) == "<class 'int'>":
      k.append(i)
    elif str(type(i)) == "<class 'list'>":
      for j in i:
        k.append(j)
  return k

engSpan = []
malSpan = []
otherLang = 0
interjection = 0

filepath = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/normalized_train.txt"
filetosavetext = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Train_POS.txt"
[english_ar, malay_ar, eng_span, mal_span, other_lang, inter_lang] = pos_tagger(filepath,filetosavetext)
df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_ar,malay_ar)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Train_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_span) + "\n"
span_data += "Malay Span: \n" + str(mal_span) + "\n"
span_data += "No of Other Language words: \n" + str(other_lang) + "\n"
span_data += "No of Interjection words: \n" + str(inter_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Train_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
eng_span = convert_list(eng_span)
mal_span = convert_list(mal_span)
I_index, burstiness, memory = span_metrics(eng_span,mal_span)

results.write('C4', eng_substitution_rate)
results.write('D4', CMI)
results.write('E4', M_index)
results.write('F4', LE)
results.write('G4', I_index)
results.write('H4', burstiness)
results.write('I4', memory)

engSpan += eng_span
malSpan += mal_span

otherLang += other_lang
interjection += inter_lang

english_re.append(english_ar)
malay_re.append(malay_ar)
engSpa.append(eng_span)
malSpa.append(mal_span)
otherLan.append(other_lang)
interject.append(inter_lang)

filepath = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/normalized_val.txt"
filetosavetext = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Validation_POS.txt"
english_ar, malay_ar, eng_span, mal_span, other_lang, inter_lang = pos_tagger(filepath,filetosavetext)
df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_ar,malay_ar)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Validation_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_span) + "\n"
span_data += "Malay Span: \n" + str(mal_span) + "\n"
span_data += "No of Other Language words: \n" + str(other_lang) + "\n"
span_data += "No of Interjection words: \n" + str(inter_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Validation_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
eng_span = convert_list(eng_span)
mal_span = convert_list(mal_span)
I_index, burstiness, memory = span_metrics(eng_span,mal_span)

results.write('C5', eng_substitution_rate)
results.write('D5', CMI)
results.write('E5', M_index)
results.write('F5', LE)
results.write('G5', I_index)
results.write('H5', burstiness)
results.write('I5', memory)

engSpan += eng_span
malSpan += mal_span

otherLang += other_lang
interjection += inter_lang

english_re.append(english_ar)
malay_re.append(malay_ar)
engSpa.append(eng_span)
malSpa.append(mal_span)
otherLan.append(other_lang)
interject.append(inter_lang)

english_res = np.add(np.array(english_re[0]) , np.array(english_re[1]))
malay_res = np.add(np.array(malay_re[0]) , np.array(malay_re[1]))

df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_res,malay_res)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Total_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(engSpan) + "\n"
span_data += "Malay Span: \n" + str(malSpan) + "\n"
span_data += "No of Other Language words: \n" + str(otherLang) + "\n"
span_data += "No of Interjection words: \n" + str(interjection)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Different_Room/Total_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
eng_span = convert_list(engSpan)
mal_span = convert_list(malSpan)
I_index, burstiness, memory = span_metrics(engSpan,malSpan)

results.write('C6', eng_substitution_rate)
results.write('D6', CMI)
results.write('E6', M_index)
results.write('F6', LE)
results.write('G6', I_index)
results.write('H6', burstiness)
results.write('I6', memory)

engSpan = []
malSpan = []
otherLang = 0
interjection = 0

filepath = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/normalized_train.txt"
filetosavetext = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Train_POS.txt"
english_ar, malay_ar, eng_span, mal_span, other_lang, inter_lang = pos_tagger(filepath, filetosavetext)
df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_ar,malay_ar)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Train_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_span) + "\n"
span_data += "Malay Span: \n" + str(mal_span) + "\n"
span_data += "No of Other Language words: \n" + str(other_lang) + "\n"
span_data += "No of Interjection words: \n" + str(inter_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Train_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
eng_span = convert_list(eng_span)
mal_span = convert_list(mal_span)
I_index, burstiness, memory = span_metrics(eng_span,mal_span)

results.write('C10', eng_substitution_rate)
results.write('D10', CMI)
results.write('E10', M_index)
results.write('F10', LE)
results.write('G10', I_index)
results.write('H10', burstiness)
results.write('I10', memory)

engSpan += eng_span
malSpan += mal_span

otherLang += other_lang
interjection += inter_lang

english_re.append(english_ar)
malay_re.append(malay_ar)
engSpa.append(eng_span)
malSpa.append(mal_span)
otherLan.append(other_lang)
interject.append(inter_lang)

filepath = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/normalized_val.txt"
filetosavetext = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Validation_POS.txt"
english_ar, malay_ar, eng_span, mal_span, other_lang, inter_lang = pos_tagger(filepath,filetosavetext)
df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_ar,malay_ar)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Validation_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_span) + "\n"
span_data += "Malay Span: \n" + str(mal_span) + "\n"
span_data += "No of Other Language words: \n" + str(other_lang) + "\n"
span_data += "No of Interjection words: \n" + str(inter_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Validation_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
I_index, burstiness, memory = span_metrics(eng_span,mal_span)

results.write('C11', eng_substitution_rate)
results.write('D11', CMI)
results.write('E11', M_index)
results.write('F11', LE)
results.write('G11', I_index)
results.write('H11', burstiness)
results.write('I11', memory)

engSpan += eng_span
malSpan += mal_span 

otherLang += other_lang
interjection += inter_lang

english_re.append(english_ar)
malay_re.append(malay_ar)
engSpa.append(eng_span)
malSpa.append(mal_span)
otherLan.append(other_lang)
interject.append(inter_lang)

english_res = np.add(np.array(english_re[2]) , np.array(english_re[3]))
malay_res = np.add(np.array(malay_re[2]) , np.array(malay_re[3]))

df, eng_substitution_rate, CMI, M_index, LE = analyzer(english_res,malay_res)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Total_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(engSpan) + "\n"
span_data += "Malay Span: \n" + str(malSpan) + "\n"
span_data += "No of Other Language words: \n" + str(otherLang) + "\n"
span_data += "No of Interjection words: \n" + str(interjection)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Same_Room/Total_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
I_index, burstiness, memory = span_metrics(engSpan,malSpan)

results.write('C12', eng_substitution_rate)
results.write('D12', CMI)
results.write('E12', M_index)
results.write('F12', LE)
results.write('G12', I_index)
results.write('H12', burstiness)
results.write('I12', memory)

# Training Data 
eng_re = np.add(np.array(english_re[0]) , np.array(english_re[2])) 
mal_re = np.add(np.array(malay_re[0]) , np.array(malay_re[2])) 
eng_spa = engSpa[0] + engSpa[2]
mal_spa = malSpa[0] + malSpa[2]
oth_lang = otherLan[0] + otherLan[2]
int_lang = interject[0] + interject[2]

df, eng_substitution_rate, CMI, M_index, LE = analyzer(eng_re,mal_re)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_Training_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_spa) + "\n"
span_data += "Malay Span: \n" + str(mal_spa) + "\n"
span_data += "No of Other Language words: \n" + str(oth_lang) + "\n"
span_data += "No of Interjection words: \n" + str(int_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_Training_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
I_index, burstiness, memory = span_metrics(eng_spa,mal_spa)

results.write('C17', eng_substitution_rate)
results.write('D17', CMI)
results.write('E17', M_index)
results.write('F17', LE)
results.write('G17', I_index)
results.write('H17', burstiness)
results.write('I17', memory)

# Test Data 
eng_re = np.add(np.array(english_re[1]) , np.array(english_re[3])) 
mal_re = np.add(np.array(malay_re[1]) , np.array(malay_re[3])) 
eng_spa = engSpa[1] + engSpa[3]
mal_spa = malSpa[1] + malSpa[3]
oth_lang = otherLan[1] + otherLan[3]
int_lang = interject[1] + interject[3]

df, eng_substitution_rate, CMI, M_index, LE = analyzer(eng_re,mal_re)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_Validation_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_spa) + "\n"
span_data += "Malay Span: \n" + str(mal_spa) + "\n"
span_data += "No of Other Language words: \n" + str(oth_lang) + "\n"
span_data += "No of Interjection words: \n" + str(int_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_Validation_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
I_index, burstiness, memory = span_metrics(eng_spa,mal_spa)

results.write('C18', eng_substitution_rate)
results.write('D18', CMI)
results.write('E18', M_index)
results.write('F18', LE)
results.write('G18', I_index)
results.write('H18', burstiness)
results.write('I18', memory)

# Total Data 
eng_re = np.add(np.add(np.array(english_re[0]) , np.array(english_re[2])) , np.add(np.array(english_re[1]) , np.array(english_re[3])))
mal_re = np.add(np.add(np.array(malay_re[0]) , np.array(malay_re[2])), np.add(np.array(malay_re[1]) , np.array(malay_re[3]))) 
eng_spa = engSpa[0] + engSpa[2] + engSpa[1] + engSpa[3]
mal_spa = malSpa[0] + malSpa[2] + malSpa[1] + malSpa[3]
oth_lang = otherLan[0] + otherLan[2] + otherLan[1] + otherLan[3]
int_lang = interject[0] + interject[2] + interject[1] + interject[3]

df, eng_substitution_rate, CMI, M_index, LE = analyzer(eng_re,mal_re)
df.to_excel("/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_POS_results.xlsx")
span_data = ""
span_data += "English Span: \n" + str(eng_spa) + "\n"
span_data += "Malay Span: \n" + str(mal_spa) + "\n"
span_data += "No of Other Language words: \n" + str(oth_lang) + "\n"
span_data += "No of Interjection words: \n" + str(int_lang)
filetosavespan = "/content/drive/MyDrive/Thesis/IMDA_4/Text/Total_other_data.txt"
f1 = open(filetosavespan,'w+')
f1.write(span_data)
f1.close()
I_index, burstiness, memory = span_metrics(eng_spa,mal_spa)

results.write('C19', eng_substitution_rate)
results.write('D19', CMI)
results.write('E19', M_index)
results.write('F19', LE)
results.write('G19', I_index)
results.write('H19', burstiness)
results.write('I19', memory)

workbook.close()


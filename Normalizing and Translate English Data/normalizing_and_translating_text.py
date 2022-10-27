# Normalizing English Data

import contractions
from text2digits import text2digits
from deep_translator import GoogleTranslator

t2d = text2digits.Text2Digits()

english_text = []
with open('English.txt') as f:
    english_text = f.readlines()
f.close()

def text_normalize(string):
    for k in list("!#$%&()*+-.:,;<=>@[]^_`{|}~"):
        string = string.replace(k,"")
    line = ""
    for j in string.split():
        line += j + " "
    eng = contractions.fix(line)
    flag = False
    temp = ""
    line = ""
    for i in eng.split():
        if len(i) == 1:
            flag = True
            temp += i.upper()
        else:
            if flag == True:
                if temp == "I" or temp == "A":
                    temp = temp.lower()
                line += temp + " "
                temp = ""
            if i == "first":
                temp = "1st"
            elif i == "second":
                temp = "2nd"
            elif i == "third":
                temp = "3rd"
            elif i == "fourth":
                temp = "4th"
            elif i == "fifth":
                temp = "5th"
            elif i == "sixth":
                temp = "6th"
            elif i == "seventh":
                temp = "7th"
            elif i == "eighth":
                temp = "8th"
            elif i == "ninth":
                temp = "9th"
            elif i == "oh":
                temp = "ohh"
            else: 
                temp = i
            flag = False
        if flag == False:
            line += temp + " "
            temp = ""
    if flag == True:
        line += temp

    return t2d.convert(line)

english_data = ""
for i in range(len(english_text)):
    english_data += text_normalize(english_text[i]) + "\n"

f1 = open("English_Normalized.txt", "w")
f1.write(english_data)
f1.close()


# Translating English Data

english_text = []
with open('English_Normalized.txt') as f:
    english_text = f.readlines()
f.close()

malay_text = ""
for i in range(len(english_text)):
    malay_text += GoogleTranslator(source='en', target='ms').translate(english_text[i]) + "\n"

f1 = open("Malay_Normalized.txt", "w")
f1.write(malay_text)
f1.close()
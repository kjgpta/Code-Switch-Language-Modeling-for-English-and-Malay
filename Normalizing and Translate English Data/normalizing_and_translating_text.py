# Importing the required libraries
import contractions
from text2digits import text2digits
from deep_translator import GoogleTranslator

t2d = text2digits.Text2Digits()

# Reading the original english text file
english_text = []
with open('English.txt') as f:
    english_text = f.readlines()
f.close()

# Function to deal with the tags information
def word_analyzer(word, tag):
    ar = ""
    tag2= tag
    if tag == "<malay>":
        tag2 = "</malay>"
    if tag == "(":
        tag2 = ")"
    if tag == "[":
        tag2 = "]"
    if tag == "<":
        tag2 = ">"
    if tag == "{":
        tag2 = "}"
    n = len(tag)
    k = len(tag2)
    if word.startswith(tag) and word.endswith(tag2):
            ar = word[n:-k]
    elif word.startswith(tag):
            ar = word[n:]
    elif word.endswith(tag2):
            ar = word[:-k]
    return ar

# Function to clean the text file 
def data_cleanser(string):
    words = string.split()
    ar = []
    sent = ""
    for word in words:
        if "_" in word:
            wrd = ""
            for j in range(len(word)):
                if word[j] != "_":
                    wrd += word[j]
            word = wrd
        elif word.startswith("<malay>") or word.endswith("</malay>"):
            word = word_analyzer(word, "<malay>")
        elif word.startswith("(") or word.endswith(")"):
            word = word_analyzer(word, "(")
        elif word.startswith("[") or word.endswith("]"):
            word = word_analyzer(word, "[")
        elif word.startswith("<") or word.endswith(">"):
            word = word_analyzer(word, "<")
        elif word.startswith("{") or word.endswith("}"):
            word = word_analyzer(word, "{")
        elif word.startswith("!") or word.endswith("!"):
            word = word_analyzer(word, "!")
        elif word.startswith("#") or word.endswith("#"):
            word = word_analyzer(word, "#")
        elif word.endswith("~"):
            word = word[:-1]
        ar.append(word)
    return " ".join(ar)
        
# Function to normalize the text file using the above user defined functions
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

# Normalize the English text
english_data = ""
for i in range(len(english_text)):
    english_data += text_normalize(data_cleanser(english_text[i])) + "\n"

f1 = open("English_Normalized.txt", "w")
f1.write(english_data)
f1.close()


# Translating Normalized English Data to Malay
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
# Python code for converting English and Malay data into Codeswitch Sentences

# Importing the required modules
import malaya
import pandas as pd
import nltk
from nltk import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

# "english_data" stores the english sentences from "English_Data.txt" file.
# "malay_data" stores the malay sentences from "Malay_Data.txt" file.
with open('English_Data.txt') as f:
    english_data = f.readlines()
f.close()

with open('Malay_Data.txt') as f:
    malay_data = f.readlines()
f.close()

# loading the BERT model for POS tagging onto "model" variable.
# loading the large model which malay to english translator onto "translator_malay" variable.
# loading the base model which english to malay translator onto "translator_english" variable.
model = malaya.pos.transformer(model = 'bert')
translator_malay = malaya.translation.ms_en.transformer(model = 'large')
translator_english = malaya.translation.en_ms.transformer()

'''
Now, we have to convert monolingual data into Code-Switched data...
We have two kinds of data Monolingual English and Monolingual Malay Sentences
1.  Monolingual Malay Data
    Do POS tagging of a sentence and change specific POS of the malay sentence to english
2.  Monolingual English Data
    Do POS tagging of a sentence and change specific POS of the english sentence to malay
'''

# "malay_cs_text" stores code switched data made from Monolingual "malay_data" variable
malay_cs_text = ""
for sentence in malay_data:
    resulting_model = model.analyze(sentence) # Does the POS tagging of sentence and stores that information into array of dictionary which consists of words and their tags with the confidence
    # "codeswitch_malay_sentence" stores CS malay sentence form of "sentence" variable
    codeswitch_malay_sentence = ""
    length = len(resulting_model)
    index = 0
    while index < length:
        txt = list(resulting_model[index]["text"])
        '''
        We are changing only Pronouns, Nouns, Proper Nouns, Determiner, Symbols
        '''
        if resulting_model[index]["type"] == "PRON" or resulting_model[index]["type"] == "NOUN" or resulting_model[index]["type"] == "PROPN" or resulting_model[index]["type"] == "DET" or resulting_model[index]["type"] == "SYM":
            phrase = ""
            # Once we found a word which we need to translate we are checking more consecutive words and if these are Pronouns, Nouns, Proper Nouns, Determiner, Symbols
            # Then we concatenate those to "phrase" variable and after that once we no longer have more consecutive word we translate the phrase to English and add those to "codeswitch_malay_sentence" variable
            while index < length and (resulting_model[index]["type"] == "PRON" or resulting_model[index]["type"] == "NOUN" or resulting_model[index]["type"] == "PROPN" or resulting_model[index]["type"] == "DET" or resulting_model[index]["type"] == "SYM"):
                text = list(resulting_model[index]["text"])
                for word in text:
                    phrase += str(word) + ' '
                index += 1
            codeswitch_malay_sentence += translator_malay.greedy_decoder([phrase])[0] + ' '
        else:
            for word in txt:
                codeswitch_malay_sentence += word + ' '
            index += 1

    malay_cs_text += codeswitch_malay_sentence + '\n'

# Saves the "malay_cs_text" onto a "Malay_CS_Data.txt" file
f1 = open("Malay_CS_Data.txt","w+")
f1.write(malay_cs_text)
f1.close()


# "english_cs_text" stores code switched data made from Monolingual "english_data" variable
english_cs_text = ""
for sentence in english_data:
    tokenized_sentence = word_tokenize(sentence)
    resulting_model = nltk.pos_tag(tokenized_sentence)
    codeswitch_english_sentence = ""
    for index in range(len(resulting_model)):
        txt = resulting_model[index][0]
        pos = resulting_model[index][1]
        # Once we found a word is Pronouns, Nouns, Proper Nouns, Determiner, Pre-Determiner and then convert that to Malay
        if pos == "PRP" or pos =="PRP$" or pos =="NN" or pos =="NNS" or pos =="NNPS" or pos =="NNP" or pos == "PDT" or pos =="DT":
            codeswitch_english_sentence +=  translator_english.greedy_decoder([txt])[0] + ' '
        else:
            codeswitch_english_sentence += txt + ' '
    english_cs_text += codeswitch_english_sentence

# Saves the "english_cs_text" onto a "English_CS_Data.txt" file
f2 = open("English_CS_Data.txt","w+")
f2.write(english_cs_text)
f2.close()

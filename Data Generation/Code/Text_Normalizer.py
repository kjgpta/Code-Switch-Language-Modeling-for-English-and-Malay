# Python code for normalizing conversational English data and converting it to Malay

# Importing the required modules
import regex as re
import malaya

# Function for cleaning out english sentence
def sentence_normalizer(input_string):
    output_string = ""
    for word in input_string.split():
        if word[0] != "<" and word != "\n":
            output_string += " " + word
        elif word == "\n":
            output_string += '.'
        else:
            output_string += ','
    output_string = re.sub(',+', ',', output_string)
    output_string = re.sub(' +', ' ', output_string)
    return output_string.strip(', ')

# Reading the conversational speech from "imda5.txt"
with open('imda5.txt') as f:
    contents = f.readlines() #contents contains array of all sentences present in file
f.close()


# "content" array stores the sentences by removing the repeated words or phrases present in the text
content = []
for s in contents:
    content.append(re.sub(r'\b(.+)(\s+\1\b)+', r'\1', s)) #This removes the repeated words or phrases in the text

# "english_text" stores normalized english text
# "text" array stores normalized english sentence
english_data = []
english_text = ""
for string in content:
    sentence = sentence_normalizer(string)
    english_text += sentence + '\n'
    english_data.append(sentence)

# Saves the "english_text" onto a "English_data.txt" file
f1 = open("English_Data.txt","w+")
f1.write(english_text)
f1.close()

# loading the base model which english to malay translator onto translator variable.
translator = malaya.translation.en_ms.transformer(model = 'base')

# "malay_text" stores normalized malay sentence
malay_text = ""
for index in range(int(len(english_data)/100)): #
    # "subarray" stores translated malay text on batch size of 100 sentences
    subarray = translator.greedy_decoder(text[int(index*100):int((index+1)*100)])
    for sentence in subarray:
        malay_text += sentence +'\n'

# Saves the "malay_text" onto a "Malay_data.txt" file
f2 = open("Malay_Data.txt","w+")
f2.write(malay_text)
f2.close()




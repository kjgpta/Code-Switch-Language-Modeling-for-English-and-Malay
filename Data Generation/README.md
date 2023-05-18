# Data Generation

People generally generate code switched data using various methods like dependancy parsing, part of speech, etc. One of the main problem with Code-Switched data is that it is speaker dependent and not defined by rules. So, we are generating Code-Switched sentences with the help of POS tagging results.

Now, we took a step further and used pairwise POS tagging from our previous work on [NSC Code-Switching Analysis](https://github.com/kjgpta/NSC-Code-Switch-Analysis). 

## Required Libraries 
1. [h5py](https://pypi.org/project/h5py/)
2. [typing-extensions](https://pypi.org/project/typing-extensions/)
3. [wheel](https://pypi.org/project/wheel/)
4. [imgaug](https://pypi.org/project/imgaug/)
5. [malaya](https://pypi.org/project/malaya/)
6. [tensorflow==2.9.0](https://pypi.org/project/tensorflow/)
7. [tensorflow_addons](https://pypi.org/project/tensorflow-addons/)
8. [transformers](https://pypi.org/project/transformers3/)
9. [NLTK](https://pypi.org/project/nltk/)
10. [Pandas](https://pypi.org/project/pandas/)
11. [deep-translator](https://pypi.org/project/deep-translator/)


## Introduction
We propose the following data generation method using Pairwise POS tagging results and phrasewise translation.

### Pairwise POS Stats
We collected results from our previous work on [NSC Code-Switching Analysis](https://github.com/kjgpta/NSC-Code-Switch-Analysis). Our results can be found in the Data folder consisting of a excel file consisting of two sheets for **English to Malay** and 
**Malay to English**.

### Phrasewise Translation: 
We loop through every word of a sentence and detect its POS and POS of its next word and also the language of the current word. Now, based on the language and POS of left and right word we gather the threshold and then we check if it is greater than our score and we extract all the phrases which we would and wouldn't translate and then translate it using [deep-translator](https://pypi.org/project/deep-translator/) and then combine them in the correct order.


## Usage
This section describes how to use the code and scripts provided in this repository.

1. Normalizing Data:

   The `Normalization.pynb` contains the code for cleaning and preparing the NSC dataset for analysis. This includes tasks such as data cleaning, normalization. Please keep in mind that this code is written specific to English and we are converting the numbers to words and expanding the contractions.

2. Translating Data:

   The `Translation.pynb` contains the code for translation of the NSC dataset. This includes translation of the NSC Dataset from English to Malay and viceversa: using [deep-translator](https://pypi.org/project/deep-translator/).

3. Code-Switching Data Generation:

   The `CS_Generation.ipynb` contains python code for generating code-switched data. This includes generating code-switched data using pairwise POS tagging and phrasewise translation of the data.

4. Denormalization of the Data:

   The `Denormalization.ipynb` contains python code for denormalizing the data. This includes converting the words back to numbers and expanding the contractions.

**Those generated CS data can be found in *English_CS.txt* and *Malay_CS.txt*** 

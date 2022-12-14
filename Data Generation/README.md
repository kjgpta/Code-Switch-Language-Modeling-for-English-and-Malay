# Data Generation methods

People generally generate code switched data using various methods like dependancy parsing, part of speech, etc. One of the main problem with Code-Switched data is that it is speaker dependent and not defined by rules. So, we are generating Code-Switcshed sentences with the help of POS tagging results.

Now, we took a step further and did pairwise POS tagging rather than word by word POS tagging. We propose three data generation methods using Pairwise POS tagging.  

## Pairwise POS Data Generation
We collected all the pairwise POS statistics in the form of POS of left and right word. Given below are the proposed methods.

### 1. Pairwise POS Translation: 
We loop through every word of a sentence and detect its POS and POS of its next word and also the language of the current word. Now, based on the language and POS of left and right word we gather the threshold and then we check if it is greater than our score and if it is then we translate the word and obtain the CS sentence.

### 2. Pairwise POS Alignment Replacement:
One of the issue with translation method was it returns sometimes a different part of speech of a sentence, so, to deal with this issue we created a alignment model and if we were to change language of a word then we instead of translating it, replace it with all the words it aligns to and obtain the CS sentence.

### 3. Pairwise POS Alignment Replacement removing duplicates:
Now, one of the issue with the last method was that sometimes two or more words align to same word(in other langauge) and since we were replacing it so, words were repeating, so, to tackle this issue we restricted the addition to only those which have not been previously added and obtain the CS sentence.

## Packages to be installed 
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

## Contact 
- Author: Kshitij Gupta
- Email: mailguptakshitij@gmail.com
- Date: 25 August 2022

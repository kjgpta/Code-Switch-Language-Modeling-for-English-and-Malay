# Data Generation methods

People generally generate code switched data using various methods like dependancy parsing, part of speech, etc. One of the main problem with Code-Switched data is that it is speaker dependent and not defined by rules. So, we are generating Code-Switcshed sentences with the help of POS tagging results.

Now, we took a step further and did pairwise POS tagging rather than word by word POS tagging. We propose the following data generation method using Pairwise POS tagging and phrase translation.  

## Pairwise POS and Phrase based Translation: 
We loop through every word of a sentence and detect its POS and POS of its next word and also the language of the current word. Now, based on the language and POS of left and right word we gather the threshold and then we check if it is greater than our score and we extract all the phrases which we would and wouldn't translate and then translate it using deep-translate


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





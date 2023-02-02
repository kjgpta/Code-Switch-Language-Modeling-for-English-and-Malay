# Normalizing and Translate English Data
NSC consists of data with several tags. So, if we directly input this data into a translator, translation produced is incorrect. 
## Problems with English Data
- Numbers present in sentence in the text form, when using our technique converts one number into malay and not other.
Example: 
-> English: My number is nine eight two three.
-> CS:      My number is sembilan eight dua tiga.
This "eight" is a problem because in these kind of context people usually use one language

- When using Alignment tool, short forms like don't, you're, etc, these produce incorrect alignments.

We need to normalize this data and then translate the english text to malay text for further use.

## Libraries
### [text2digits](https://pypi.org/project/text2digits/):
    Library for Converting the number in text form to numeral form
### [contractions](https://pypi.org/project/contractions/):
    Library for expanding the short forms
### [deep-translator](https://pypi.org/project/deep-translator/):
    Library using Google translate API to translate between English and Malay

## Installations
- pip install text2digits
- pip install contractions
- pip install deep-translator
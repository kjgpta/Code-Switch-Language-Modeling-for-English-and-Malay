'''

Counts number of names, exclamations, discourse particles, fillers
Compute average of each per utterance

Assumes input files are already normalized for LM counting (from preprocessing script)
(python3 preporcess_text_fpr_analysis)
Prints to standard output


Usage: python3 get_text_stats.py


Author: Chaiyasait Prachaseree
Email: prac0003@e.ntu.edu.sg
Date: 14 August 2022


# TODO standard deviation for the averages

'''

import os, re

current_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_path, "..", "data", "analysis-and-lm-normalized")
files = ["combined_train_lm.txt", "combined_val_lm.txt", "combined_test_lm.txt"]
vocab = os.path.join("..", "vocab", "vocab.txt")

def get_stats(path, file):
    print("Text file Analysis on", file)
    file_path = os.path.join(path, file)
    # count words that are names (##), exclamations (!!), discourse particles ([]), fillers (())
    names = exclamations = discourse_particles = fillers = 0
    num_words = num_utterances = 0

    # get ratio of names, exclamations, discourse particles, and fillers per utterance 
    per_utterance_stats = [0, 0, 0, 0]

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            line_split = line.split()
            if len(line_split) == 0:
                continue
            prev = names, exclamations, discourse_particles, fillers
            for word in line_split:
                if re.search('#(.+?)#', word):
                    names += 1
                elif re.search('!(.+?)!', word):
                    exclamations += 1
                elif re.search('\[(.+?)\]', word):
                    discourse_particles += 1
                elif re.search('\((.+?)\)', word):
                    fillers += 1
            num_words += len(line_split)
            num_utterances += 1
            
            avg = [(new - old) / len(line_split) for new, old in zip([names, exclamations, discourse_particles, fillers], prev)]
            per_utterance_stats = [prev + update for prev, update in zip(per_utterance_stats, avg)]

        print("Absolute values:")
        print("names:", names)
        print("exclamations:", exclamations)
        print("discourse_particles:", discourse_particles)
        print("fillers:", fillers)
        print("num_words:", num_words)
        print("num_utterances:", num_utterances)
        print()
        print("Averages per utterance:")
        print("names per utterance:", names / num_utterances) 
        print("exclamations per utterance:", exclamations / num_utterances)
        print("discourse_particles per utterance:", discourse_particles / num_utterances)
        print("fillers per utterance:", fillers / num_utterances)
        print("words per utterance:", num_words / num_utterances)
        print()
        print("Average ratio per utterance")
        print("names ratio per utterance:", per_utterance_stats[0] / num_utterances) 
        print("exclamations ratio per utterance:", per_utterance_stats[1] / num_utterances)
        print("discourse_particles ratio per utterance:", per_utterance_stats[2] / num_utterances)
        print("fillers ratio per utterance:", per_utterance_stats[3] / num_utterances)

def get_vocab_stats(vocab):
    print("Vocab Analysis:")
    names = exclamations = discourse_particles = fillers = 0
    num_vocab = 0
    with open(vocab, "r") as f:
        for word in f:
            word = word.strip()
            if re.search('#(.+?)#', word):
                names += 1
            elif re.search('!(.+?)!', word):
                exclamations += 1
            elif re.search('\[(.+?)\]', word):
                discourse_particles += 1
            elif re.search('\((.+?)\)', word):
                fillers += 1
            num_vocab += 1
        
        print("names:", names)
        print("exclamations:", exclamations)
        print("discourse_particles:", discourse_particles)
        print("fillers:", fillers)
        print("num_vocab:", num_vocab)
        print()
        print("names ratio:", names / num_vocab)
        print("exclamations ratio:", exclamations / num_vocab)
        print("discourse_particles ratio:", discourse_particles / num_vocab)
        print("fillers ratio:", fillers / num_vocab)


def run(path, files, vocab):
    for file in files:
        get_stats(path, file)
    get_vocab_stats(vocab)

if __name__=="__main__":
    run(path, files, vocab)

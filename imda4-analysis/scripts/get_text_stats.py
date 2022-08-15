'''

Counts number of names, exclamations, discourse particles, fillers
Compute average of each per utterance

Assumes input files are already normalized for LM counting (from preprocessing script)
(python3 preprocess_text_fpr_analysis)
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
output_file = os.path.join("..", "stats.txt")
os.remove(output_file)

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

    with open(output_file, "a") as f:
        f.write("Text file Analysis: " +  file + "\n")

        f.write("Absolute values:\n")
        f.write("names: " + str(names) + "\n")
        f.write("exclamations: " + str(exclamations) + "\n")
        f.write("discourse_particles: " + str(discourse_particles) + "\n")
        f.write("fillers: " + str(fillers) + "\n")
        f.write("num_words: " + str(num_words) + "\n")
        f.write("num_utterances:" + str(num_utterances) + "\n\n")
        f.write("Averages per utterance:\n")
        f.write("names per utterance: " + str(names / num_utterances) + "\n") 
        f.write("exclamations per utterance: " + str(exclamations / num_utterances) + "\n")
        f.write("discourse_particles per utterance: " + str(discourse_particles / num_utterances) + "\n")
        f.write("fillers per utterance: " + str(fillers / num_utterances) + "\n")
        f.write("words per utterance: " + str(num_words / num_utterances) + "\n\n")
        f.write("Average ratio per utterance\n")
        f.write("names ratio per utterance: " + str(per_utterance_stats[0] / num_utterances) + "\n")
        f.write("exclamations ratio per utterance: " + str(per_utterance_stats[1] / num_utterances) + "\n")
        f.write("discourse_particles ratio per utterance: " + str(per_utterance_stats[2] / num_utterances) + "\n")
        f.write("fillers ratio per utterance: " + str(per_utterance_stats[3] / num_utterances) + "\n\n")
        f.write("---------------------------------------------------------------------- \n\n")

def get_vocab_stats(vocab):
    print("Vocab Analysis")
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
    
    with open(output_file, "a") as f:
        f.write("Vocab Analysis\n")
        f.write("names:" + str(names) + "\n")
        f.write("exclamations: " + str(exclamations) + "\n")
        f.write("discourse_particles: " + str(discourse_particles) + "\n")
        f.write("fillers: " + str(fillers) + "\n")
        f.write("num_vocab: " + str(num_vocab) + "\n\n")
        f.write("names ratio: " + str(names / num_vocab) + "\n")
        f.write("exclamations ratio: " + str(exclamations / num_vocab) + "\n")
        f.write("discourse_particles ratio: " + str(discourse_particles / num_vocab) + "\n")
        f.write("fillers ratio: " + str(fillers / num_vocab) + "\n")


def run(path, files, vocab):
    for file in files:
        get_stats(path, file)
    get_vocab_stats(vocab)

if __name__=="__main__":
    run(path, files, vocab)

'''
Description:
normalize train, val, and test sets by removing <malay></malay>
output to different room and same room
create combined training, val, test set that is normalized for LM experiments
create vocabulary list of all words in imda4, to be used constant in all experiments

Usage:
python3 preprocess_text_for_analysis


Author: Chaiyasait Prachaseree
Email: prac0003@e.ntu.edu.sg
Date: 14 August 2022
'''

import os, re

# reads in_unnorm_file, remove <malay></malay>, output to out_norm_file
# add "-" in between names in # # so names become one word
def normalize(in_path, out_path):
    with open(in_path, "r") as rf:
        with open(out_path, "w") as wf:
            for line in rf:
                line = line.replace("<malay>", "").replace("</malay>", "").replace("</malay", "").replace("<>/malay>", "").replace("malay>", "").lower()
                line = add_hyphen_names(line)
                wf.write(line)

# add "-" in between names in # # so names become one word
def add_hyphen_names(string):
    between_hash = re.findall('#(.+?)#', string)
    with_space = [t for t in between_hash if len(t.split()) > 1]
    if with_space:
        for ws in with_space:
            new_word = "-".join(ws.split())
            new_string = string.replace(ws, new_word)
        return new_string
    return string

# reads text from in_file, list unique vocabulary to vocab output
def create_vocabulary(in_file, vocab_path, vocab_output):
    vocab_set = set()
    with open(in_file, "r") as rf:  
        for line in rf:
            words = line.strip().split()
            vocab_set.update(words)
    if not os.path.exists(vocab_path):
        os.makedirs(vocab_path)
    with open(os.path.join(vocab_path, vocab_output), "w") as wf:
        sorted_set = sorted(vocab_set)
        for v in sorted_set:
            wf.write(v + "\n")

def combine(file1, file2, out_file):
    with open(out_file, "w") as wf:
        with open(file1, "r") as f:
            wf.writelines(f.readlines())
        with open(file2, "r") as f:
            wf.writelines(f.readlines())

# create ../data/analysis-and-lm-normalized/Different_Room and ../data/analysis-and-lm-normalized/Same_Room 
def create_out_dir(out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    different_room_norm_path = os.path.join(out_path, "Different_Room")
    same_room_norm_path = os.path.join(out_path, "Same_Room")
    if not os.path.exists(different_room_norm_path):
        os.makedirs(different_room_norm_path)
    if not os.path.exists(same_room_norm_path):
        os.makedirs(same_room_norm_path)

if __name__=="__main__":
    current_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_path, "..", "data", "Text")
    out_path = os.path.join(current_path, "..", "data", "analysis-and-lm-normalized")
    
    ori_imda4_paths = ["train.txt", "val.txt", "test.txt"]
    normalized_imda4_paths = ["train_lm.txt", "val_lm.txt", "test_lm.txt"]

    vocab_path = os.path.join("..", "vocab")

    create_out_dir(out_path)
    
    for in_unnorm_file, out_norm_file in zip(ori_imda4_paths, normalized_imda4_paths):
        for room in ["Different_Room", "Same_Room"]:
            in_path = os.path.join(path, room, in_unnorm_file)
            output_path = os.path.join(out_path, room, out_norm_file)
            normalize(in_path, output_path)

    for out_norm_file in normalized_imda4_paths:
        different_room_file = os.path.join(out_path, "Different_Room", out_norm_file)
        same_room_file = os.path.join(out_path, "Same_Room", out_norm_file)
        combined_file = os.path.join(out_path, "combined_" + out_norm_file)
        combine(different_room_file, same_room_file, combined_file)

    create_vocabulary(os.path.join(out_path, "combined_train_lm.txt"), vocab_path, "vocab.txt")
import os, re

'''
Partitions code to eng mono or eng-malay cs
'''

current_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_path, "..", "data", "Text")

different_room_path = os.path.join(path, "Different_Room")
same_room_path = os.path.join(path, "Same_Room")

monoeng_path = os.path.join(path, "monoeng")
engmalaycs_path = os.path.join(path, "engmalaycs")

def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def run():
    # create output directories
    make_dir(monoeng_path)
    make_dir(engmalaycs_path)

    for train_val_test in ["train", "val", "test"]:
        out_monoeng_file = os.path.join(monoeng_path, train_val_test + ".txt")
        out_engmalaycs_file = os.path.join(engmalaycs_path, train_val_test + ".txt")

        # for different room
        with open(os.path.join(different_room_path, train_val_test + ".txt"), "r") as f:
            with open(out_monoeng_file, "w") as monoeng_f:
                with open(out_engmalaycs_file, "w") as engmalaycs_f:
                    for line in f:
                        if re.search("<malay>", line):
                            engmalaycs_f.write(line)
                        else:
                            monoeng_f.write(line)

        # for same room
        with open(os.path.join(same_room_path, train_val_test + ".txt"), "r") as f:
            with open(out_monoeng_file, "a") as monoeng_f:
                with open(out_engmalaycs_file, "a") as engmalaycs_f:
                    for line in f:
                        if re.search("<malay>", line):
                            engmalaycs_f.write(line)
                        else:
                            monoeng_f.write(line)


if __name__=="__main__":
    run()
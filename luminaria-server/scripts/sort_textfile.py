import os

from constants import STATIC_DIR
from vars import ROOT_DIR


def sort_file(filename):

    file_path = os.path.join(ROOT_DIR, STATIC_DIR, filename)
    lst = []
    s = set()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if line not in s:
                lst.append(line)
                s.add(line)

    lst.sort()

    with open(file_path, 'w+') as f:
        for word in lst:
            f.write(word + '\n')


if __name__ == "__main__":
    sort_file('blacklist.txt')

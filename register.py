import os
import time
import shutil
from getch import getch, pause
import numpy as np

WIN_SIZE = shutil.get_terminal_size((80, 20))
WIN_SIZE = (WIN_SIZE.columns, WIN_SIZE.lines)
sentence = "Cybersecurity is also one of the significant challenges in the contemporary world, due to the complexity of information systems, both in terms of political usage and technology. Its primary goal is to ensure the system's dependability, integrity, and data privacy."

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
SHADE = "\033[2;4m"

def cls():
    print("\033c")

def typing():
    sum = np.zeros((128, 128))
    count = np.zeros((128, 128))
    last_ch = ''
    i = 0
    print(sentence)
    start = time.time()
    while i < len(sentence):
        x = getch()
        stop = time.time()
        elasped = stop - start
        if ord(x) in [3, 26]:    # CTRL+C, CTRL+Z
            raise KeyboardInterrupt
        if x != sentence[i]:
            continue
        if i > 0:
            sum[ord(last_ch), ord(x)] += elasped
            count[ord(last_ch), ord(x)] += 1
        cls()
        print(SHADE + sentence[:i + 1] + RESET + sentence[i + 1:])
        print()
        print("-" * WIN_SIZE[0])
        print("Digraph (%s, %s): %.4f sec" % (last_ch, x, elasped))
        i += 1
        last_ch = x
        start = time.time()
    print(RESET, end='')
    return np.divide(sum, count, out=np.zeros_like(sum), where=count!=0)

def main():
    cls()
    print(BOLD + "Keystoke Identification Registration" + RESET)
    name = input("Your name: ")
    cls()
    print(BOLD + "Instruction:" + RESET)
    print("You will be prompted with a sentence, you must copy the prompted sentence correctly.")
    print("Backspace/Deleting is prohibited. If you somehow type an incorrect character, please try a new character until it becomes correct.")
    print("Press CTRL+C or CTRL+Z if you need to exit the program.")
    print()
    print(BOLD + "You will be prompted with following sentence:" + RESET)
    print("-" * WIN_SIZE[0])
    print(sentence)
    print("-" * WIN_SIZE[0])
    print()
    pause("Press any key when you are ready. The timer will start when you type the first character.")
    cls()
    avg_digraph = typing()
    cls()
    print("Saving...")
    filepath = os.path.join("db", "%s.npy" % name)
    np.save(filepath, avg_digraph)
    print("Your identity has been saved to", filepath)

if __name__ == "__main__":
    main()

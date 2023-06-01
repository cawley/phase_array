import random as rand
import numpy as np
def generate_bin():
    f = open("in.txt", "w")
    c = 1
    for _ in range(256):
        s = ""
        for _ in range(6):
            r = rand.uniform(0, 1)
            if r > .5:
                s += "1"
            else:
                s += "0"        
        f.write(s)
        f.write(" ")
        if c % 16 == 0:
            f.write("\n")
        c +=1

if __name__ == "__main__":
    generate_bin()
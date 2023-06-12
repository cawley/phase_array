import numpy as np

def main():
    pop = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    s1, s2, s3 = int(len(pop)/4), int(2 * len(pop)/4), int(3 * (len(pop)/4))

    p1 = pop[:s1]
    p2 = pop[s1:s2]
    p3 = pop[s2:s3]
    p4 = pop[s3:]

    p = np.concatenate((p1, p2, p3, p4))

    print(p1, p2, p3, p4)
    print(p)


if __name__ == "__main__":
    main()
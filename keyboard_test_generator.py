import random

seed = int(input("seed: "))
n = int(input("nombre participants: "))
fpath = input("arxiu amb paraules: ")

words = []

with open(fpath, "r") as f:
    # a l'arxiu de paraules n'hi ha una per línia
    words = f.readlines()


random.seed(seed)
for i in range(n):
    time = random.randint(30, 120)
    cpywords = words.copy()

    with open(f"id{i}_{time}s.csv", "w") as out:
        while len(cpywords) != 0:
            out.write(cpywords.pop(random.randint(0, len(cpywords) - 1)))
            out.write(" ")

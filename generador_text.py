import random

seed = int(input("seed: "))
n = int(input("nombre de textos: "))
fpath = input("arxiu amb paraules: ")

words = []

with open(fpath, "r") as f:
    # a l'arxiu de paraules n'hi ha una per línia
    words = f.readlines()


random.seed(seed)
for i in range(n):
    cpywords = words.copy()

    with open(f"id{i}.txt", "w") as out:
        while len(cpywords) != 0:
            out.write(cpywords.pop(random.randint(0, len(cpywords) - 1)))

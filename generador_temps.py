import random

seed = int(input("seed: "))
n = int(input("quantitat de nombres a generar: "))

with open(f"temps_seed{seed}.txt", "w") as out:
    for i in range(n):
        out.write("{},{}\n".format(i, random.randint(15, 90)))

class Hanoi:
    def __init__(self):
        pass

    def c1(self, halghe: str) -> int:
        d = {}

        for i in range(0, len(inp), 2):
            if inp[i+1] in d:
                d[inp[i+1]].append(inp[i])
            else:
                d[inp[i+1]] = [inp[i]]


        s = sum(list(map((lambda i: len(set(d[i]))==3), d)))

        return s




inp = input()

h = Hanoi()
print(h.c1(inp))

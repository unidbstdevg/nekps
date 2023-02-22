from pprint import pp
import csv

DATA_FILENAME = "data/my.csv"


def parse_csv(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        it = iter(reader)
        # this is header
        alts = next(it, None)

        alts = {x: [] for x in alts[1:] if x != ""}

        for row in it:
            # skip empty delimiter line
            if row[0] == "":
                continue

            # skip attribute name
            row = row[1:]

            for attrib, alt in zip(row, alts.keys()):
                alts[alt].append(int(attrib))

    return alts


def init_matrix(n, m):
    return [[-1 for _ in range(n)] for _ in range(m)]


def make_matrix(alts, f):
    N = len(alts)
    r = init_matrix(N, N)
    for i in range(N):
        for j in range(N):
            # if i == j:
            #     r[i][j] = 0
            #     continue

            alt1 = alts[i]
            alt2 = alts[j]
            r[i][j] = sum([f(a, b) for a, b in zip(alt1, alt2)])
    return r


def calc_H(p11, p10):
    # yapf: disable
    return [
            [
                round(x / (x + y), 2)
                for x, y in zip(row1, row2)
            ]
            for row1, row2 in zip(p11, p10)
        ]


def calc_G(p11, p00):
    # yapf: disable
    return [
            [
                round(x / y, 2)
                for x, y in zip(row1, row2)
            ]
            for row1, row2 in zip(p11, p00)
        ]


alts = list(parse_csv(DATA_FILENAME).values())

p10 = make_matrix(alts, lambda a, b: a if a != b else 0)
p01 = make_matrix(alts, lambda a, b: b if a != b else 0)
p11 = make_matrix(alts, lambda a, b: 1 if (a == 1 and b == 1) else 0)
p00 = make_matrix(alts, lambda a, b: 0 if (a == 0 and b == 0) else 1)
# pp(p01)


H = calc_H(p11, p10)
G = calc_G(p11, p00)

pp(G)

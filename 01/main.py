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
            alt1 = alts[i]
            alt2 = alts[j]
            r[i][j] = sum([f(a, b) for a, b in zip(alt1, alt2)])
    return r


def apply_f_to_2_matrix(a, b, f):
    # yapf: disable
    return [
            [
                f(x, y)
                for x, y in zip(row1, row2)
            ]
            for row1, row2 in zip(a, b)
        ]


def binarize(ar, threshold):
    N = len(ar)

    # yapf: disable
    return [
            [
                0 if i == j else
                (1 if ar[i][j] >= threshold
                 else 0)
                for j in range(N)
            ]
            for i in range(N)
        ]


alts = list(parse_csv(DATA_FILENAME).values())

p10 = make_matrix(alts, lambda a, b: a if a != b else 0)
p01 = make_matrix(alts, lambda a, b: b if a != b else 0)
p11 = make_matrix(alts, lambda a, b: 1 if (a == 1 and b == 1) else 0)
p00 = make_matrix(alts, lambda a, b: 0 if (a == 0 and b == 0) else 1)

H = apply_f_to_2_matrix(p11, p10, lambda x, y: round(x / (x + y), 2))
G = apply_f_to_2_matrix(p11, p00, lambda x, y: round(x / y, 2))

bH = binarize(H, 0.9)
bG = binarize(G, 0.8)

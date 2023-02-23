import itertools
import csv

DATA_FILENAME = "data/my.csv"


def parse_csv(filename):
    """Returns attribute columns

    File format:

               name1   name2  ...
    attr_name1 attrib  attrib ...
    attr_name2 attrib  attrib ...
    ...
    """

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        # skip header row
        reader = itertools.islice(reader, 1, None)
        # yes, transpose
        reader = zip(*reader)
        # skip column with attribute names
        reader = itertools.islice(reader, 1, None)

        # yapf: disable
        return [
                [
                    int(attrib)
                    for attrib in col
                    # skip empty cells
                    if attrib != ""
                    ]
                for col in reader
                ]

    return None


def make_matrix(alts, f):
    # yapf: disable
    return [
            [
                sum([f(a, b) for a, b in zip(alt1, alt2)])
                for alt2 in alts]
            for alt1 in alts
        ]


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


alts = parse_csv(DATA_FILENAME)

p10 = make_matrix(alts, lambda a, b: a if a != b else 0)
p01 = make_matrix(alts, lambda a, b: b if a != b else 0)
p11 = make_matrix(alts, lambda a, b: 1 if (a == 1 and b == 1) else 0)
p00 = make_matrix(alts, lambda a, b: 0 if (a == 0 and b == 0) else 1)

H = apply_f_to_2_matrix(p11, p10, lambda x, y: round(x / (x + y), 2))
G = apply_f_to_2_matrix(p11, p00, lambda x, y: round(x / y, 2))

bH = binarize(H, 0.9)
bG = binarize(G, 0.8)

print("bH:")
[print(*row) for row in bH]
print("\nbG:")
[print(*row) for row in bG]

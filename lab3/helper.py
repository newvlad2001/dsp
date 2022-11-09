from math import pi, sin


def spectrum_x(n):
    labels = []
    for i in range(n // 2):
        labels.append(i)

    return labels


def sin_table(n):
    sin_table = []
    for i in range(n):
        sin_table.append(sin(2 * pi * i / n))

    return sin_table

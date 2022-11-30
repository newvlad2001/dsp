from math import sin, pi, sqrt, cos, atan
from random import random

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20, 15), dpi=100)
spec = fig.add_gridspec(4, 2)

ax00 = fig.add_subplot(spec[0, 0])
ax01 = fig.add_subplot(spec[0, 1])
ax10 = fig.add_subplot(spec[1, 0])
ax11 = fig.add_subplot(spec[1, 1])
ax20 = fig.add_subplot(spec[2, 0])
ax21 = fig.add_subplot(spec[2, 1])
ax30 = fig.add_subplot(spec[3, 0])
ax31 = fig.add_subplot(spec[3, 1])


def signal(B1, B2, i, N):
    return B1 * sin(2 * pi * i / N) + sum(
        (-1 if random() > 0.5 else 1) * B2 * sin(2 * pi * i * j / N) for j in range(50, 70))


def A_cos_j(signal, j, N):
    return 2 * sum([signal[i] * cos(2 * pi * j * i / N) for i in range(N)]) / N


def A_sin_j(signal, j, N):
    return 2 * sum([signal[i] * sin(2 * pi * j * i / N) for i in range(N)]) / N


def get_spectrum(signal):
    A_cos = [A_cos_j(signal, j, len(signal)) for j in range(0, len(signal) // 2)]
    A_sin = [A_sin_j(signal, j, len(signal)) for j in range(0, len(signal) // 2)]
    return [sqrt(A_cos[j] ** 2 + A_sin[j] ** 2) for j in range(len(signal) // 2)], \
           [atan(A_sin[j] / A_cos[j]) for j in range(len(signal) // 2)]


def avg_smoothing(signal, N, K):
    res = []
    for i in range(N):
        leftEdge = max(i - (K - 1) // 2, 0)
        rightEdge = min(i + (K - 1) // 2 + 1, N)
        res.append(sum(signal[leftEdge:rightEdge]) / (rightEdge - leftEdge))
    return res


def parabola_smoothing(signal, N):
    res = []

    def get(j):
        return signal[j] if j in range(0, N) else 0

    for i in range(0, N):
        res.append((110 * get(i - 6) - 198 * get(i - 5) - 135 * get(i - 4)
                    + 110 * get(i - 3) + 390 * get(i - 2) + 600 * get(i - 1)
                    + 677 * get(i) + 600 * get(i + 1) + 390 * get(i + 2)
                    + 110 * get(i + 3) - 135 * get(i + 4) - 198 * get(i + 5)
                    + 110 * get(i + 6)) / 2431)
    return res


def median_smoothing(signal, N, windowSize):
    res = []
    for i in range(N):
        leftEdge = max(i - (windowSize - 1) // 2, 0)
        rightEdge = min(i + (windowSize - 1) // 2 + 1, N)
        res.append(sorted(signal[leftEdge:rightEdge])[(rightEdge - leftEdge) // 2 + 1])
    return res


def main():
    B1 = 50
    B2 = 1
    N = 1024

    MAX_X = N
    MAX_SPECTRUM_X = N // 2

    X = range(N)
    SPECTRUM_X = range(N // 2)
    S = [signal(B1, B2, i, N) for i in range(N)]

    avg = avg_smoothing(S, N, 5)
    parabola = parabola_smoothing(S, N)
    median = median_smoothing(S, N, 7)

    signal_spectrum = get_spectrum(S)
    avg_spectrum = get_spectrum(avg)
    parabola_spectrum = get_spectrum(parabola)
    median_spectrum = get_spectrum(median)

    ax00.set_title('Without smoothing')
    ax00.plot(X, S)
    ax00.set_xlim((0, MAX_X))
    ax01.plot(SPECTRUM_X, signal_spectrum[0])
    ax01.set_xlim((0, MAX_SPECTRUM_X))

    ax10.set_title('Moving avg')
    ax10.plot(X, avg)
    ax10.set_xlim((0, MAX_X))
    ax11.plot(SPECTRUM_X, avg_spectrum[0])
    ax11.set_xlim((0, MAX_SPECTRUM_X))

    ax20.set_title('Parabola')
    ax20.plot(X, parabola)
    ax20.set_xlim((0, MAX_X))
    ax21.plot(SPECTRUM_X, parabola_spectrum[0])
    ax21.set_xlim((0, MAX_SPECTRUM_X))

    ax30.set_title('Median')
    ax30.plot(X, median)
    ax30.set_xlim((0, MAX_X))
    ax31.plot(SPECTRUM_X, median_spectrum[0])
    ax31.set_xlim((0, MAX_SPECTRUM_X))

    plt.show()


main()

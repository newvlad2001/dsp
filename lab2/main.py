import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi, sqrt

N = 1024
K = N // 4
phase = pi / 16

fig = plt.figure(figsize=(20, 10), dpi=100)
spec = fig.add_gridspec(1, 2)

ax00 = fig.add_subplot(spec[0, 0])
ax01 = fig.add_subplot(spec[0, 1])

fig.supxlabel('M')
fig.supylabel('Error')


def f(x):
    return sin(2 * pi * x / N)


def f2(x):
    return sin(2 * pi * x / N + phase)


def get_aqv_v1(M, function):
    _sum = 0
    for i in range(M):
        _sum += function(i) ** 2
    return sqrt(_sum / (M + 1))


def get_aqv_v2(M, function):
    sum_1 = 0
    sum_2 = 0
    for i in range(M):
        sum_1 += function(i) ** 2
        sum_2 += function(i)
    return sqrt(sum_1 / (M + 1) - (sum_2 / (M + 1)) ** 2)


def get_ampl_py(M, function):
    y = [function(i) for i in range(M)]
    fft = np.fft.fft(y)
    amplitudes = (2 / M) * np.abs(fft)
    return max(amplitudes)


def get_ampl(M, function):
    cos_sum = 0
    sin_sum = 0
    for i in range(M):
        y = function(i)
        cos_sum += y * cos((2 * pi * i) / M)
        sin_sum += y * sin((2 * pi * i) / M)
    ampl = sqrt(((2 / M) * cos_sum) ** 2 + ((2 / M) * sin_sum) ** 2)
    return ampl


def build(function, axes):
    x = []
    d_1s = []
    d_2s = []
    d_as = []
    for M in range(K, 2 * N):
        x_aqv_1 = get_aqv_v1(M, function)
        x_aqv_2 = get_aqv_v2(M, function)
        a = get_ampl(M, function)
        d_1 = 0.707 - x_aqv_1
        d_2 = 0.707 - x_aqv_2
        d_a = 1 - a
        # print("-----------")
        # print(f"x_aqv_1: {x_aqv_1}")
        # print(f"x_aqv_2: {x_aqv_2}")
        # print(f"A: {a}")
        # print(f"d_1: {d_1}")
        # print(f"d_2: {d_2}")
        # print(f"d_a: {d_a}")
        x.append(M)
        d_1s.append(d_1)
        d_2s.append(d_2)
        d_as.append(d_a)

    axes.plot(x, d_1s, label='d_aqv_1')
    axes.plot(x, d_2s, label='d_aqv_2')
    axes.plot(x, d_as, label='d_a')
    axes.legend()


build(f, ax00)
build(f2, ax01)
plt.show()

from math import pi, sin, cos, sqrt, atan, floor
from random import random
from matplotlib import pyplot as plt, use
import helper

# use('TkAgg')

fig = plt.figure(figsize=(20, 15), dpi=100)
spec = fig.add_gridspec(4, 3)

ax00 = fig.add_subplot(spec[0, 0])
ax01 = fig.add_subplot(spec[0, 1])
ax02 = fig.add_subplot(spec[0, 2])
ax10 = fig.add_subplot(spec[1, 0])
ax11 = fig.add_subplot(spec[1, 1])
ax12 = fig.add_subplot(spec[1, 2])
ax20 = fig.add_subplot(spec[2, 0])
ax21 = fig.add_subplot(spec[2, 1])
ax22 = fig.add_subplot(spec[2, 2])
ax30 = fig.add_subplot(spec[3, 0])
ax31 = fig.add_subplot(spec[3, 1])
ax32 = fig.add_subplot(spec[3, 2])

N = 1024
X = range(N)
SPECTRUM_X = helper.spectrum_x(N)
SIN_TABLE = helper.sin_table(N)
AMPLITUDES = [1, 2, 5, 7, 9, 13, 18]
PHASES = [pi / 6, pi / 4, pi / 3, pi / 2, 3 * pi / 4, pi]
EPS = 0.0001

X_LIM = (0, N // 20)


def test_signal():
    signal = []
    for i in range(N):
        signal.append(10 * cos(2 * pi * i / N - pi / 2))

    return signal


def calculate_ac_as(signal, j):
    Ac = 0
    As = 0
    for i in range(N):
        Ac += signal[i] * SIN_TABLE[(i * j + N // 4) % N]
        As += signal[i] * SIN_TABLE[(i * j) % N]

    if Ac <= EPS:
        Ac = 0

    if As <= EPS:
        As = 0

    return [Ac * 2 / N, As * 2 / N]


def get_spectrum(signal):
    spectrum = {
        'amplitudes': [],
        'phases': []
    }

    for j in range(N // 2):
        AcAndAs = calculate_ac_as(signal, j)
        spectrum['amplitudes'].append(sqrt(AcAndAs[0] ** 2 + AcAndAs[1] ** 2))

        if AcAndAs[0] == 0 and AcAndAs[1] == 0:
            phase = 0
        elif AcAndAs[0] == 0 and AcAndAs[1] != 0:
            phase = pi / 2
        else:
            phase = atan(AcAndAs[1] / AcAndAs[0])

        spectrum['phases'].append(phase)

    return spectrum


def recover_signal(spectrum):
    signal = []
    for i in range(N):
        signal_value = 0
        for j in range(N // 2):
            signal_value += spectrum['amplitudes'][j] * cos(2 * pi * i * j / N - spectrum['phases'][j])

        signal.append(signal_value)

    return signal


def polyharmonic_signal():
    n = 30
    amplitudes = []
    phases = []
    for i in range(n):
        amplitudes.append(AMPLITUDES[floor(random() * len(AMPLITUDES))])
        phases.append(PHASES[floor(random() * len(PHASES))])

    signal = []
    for i in range(N):
        signal_value = 0
        for j in range(1, n + 1):
            signal_value += amplitudes[j - 1] * cos(2 * pi * i * j / N - phases[j - 1])

        signal.append(signal_value)

    return signal


def recover_polyharmonic_signal(spectrum):
    signal = []
    for i in range(N):
        signal_value = 0
        for j in range(1, N // 2):
            signal_value += spectrum['amplitudes'][j] * cos(2 * pi * i * j / N - spectrum['phases'][j])

        signal.append(signal_value + spectrum['amplitudes'][0] / 2)

    return signal


def recover_polyharmonic_signal_wo_phases(spectrum):
    signal = []
    for i in range(N):
        signal_value = 0
        for j in range(1, N // 2):
            signal_value += spectrum['amplitudes'][j] * cos(2 * pi * i * j / N)

        signal.append(signal_value + spectrum['amplitudes'][0] / 2)

    return signal


def w(k, n):
    arg = -2 * pi * k / n
    return {'cos': cos(arg), 'sin': sin(arg)}


def complex_sum(a, b):
    return {'cos': a['cos'] + b['cos'], 'sin': a['sin'] + b['sin']}


def complex_sub(a, b):
    return {'cos': a['cos'] - b['cos'], 'sin': a['sin'] - b['sin']}


def complex_mult(a, b):
    return {'cos': a['cos'] * b['cos'] - a['sin'] * b['sin'], 'sin': a['cos'] * b['sin'] + a['sin'] * b['cos']}


def fft(signal):
    n = len(signal)
    if n == 1:
        result = [signal[0]]
    else:
        x_even = [None] * (n // 2)
        x_odd = [None] * (n // 2)
        for i in range(n // 2):
            x_even[i] = signal[2 * i]
            x_odd[i] = signal[2 * i + 1]

        result_even = fft(x_even)
        result_odd = fft(x_odd)
        result = [None] * n
        for i in range(n // 2):
            result[i] = complex_sum(result_even[i], complex_mult(w(i, n), result_odd[i]))
            result[i + (n // 2)] = complex_sub(result_even[i], complex_mult(w(i, n), result_odd[i]))

    return result


def round(result):
    for i in range(len(result)):
        if result[i]['cos'] < EPS:
            result[i]['cos'] = 0
        if result[i]['sin'] < EPS:
            result[i]['sin'] = 0

    return result


def normalize_fft(spectrum):
    n = len(spectrum)
    result = [None] * n
    for i in range(n // 2):
        result[i] = spectrum[n // 2 + i]
        result[n // 2 + i] = spectrum[i]

    return result


def convert_spectrum(spectrum):
    result = [{'cos': 0, 'sin': 0}]
    for i in range(len(spectrum) // 2 - 1, 0, -1):
        result.append(spectrum[i])

    return result


def convert_to_ampls_phases(spectrum):
    result = {
        'amplitudes': [],
        'phases': []
    }

    for i in range(len(spectrum)):
        value = spectrum[i]
        result['amplitudes'].append(sqrt(value['cos'] ** 2 + value['sin'] ** 2))

        if value['cos'] == 0 and value['sin'] == 0:
            phase = 0
        elif value['cos'] == 0 and value['sin'] != 0:
            phase = pi / 2
        else:
            phase = atan(value['sin'] / value['cos'])

        result['phases'].append(phase)

    return result


def signal_to_complex(signal):
    result = []
    for i in range(len(signal)):
        result.append({
            'cos': signal[i] * 2 / len(signal),
            'sin': 0
        }
        )

    return result


def conjugate(a):
    return {
        'cos': a['cos'],
        'sin': -a['sin']
    }


def scale(a, alpha):
    return {
        'cos': alpha * a['cos'],
        'sin': alpha * a['sin']
    }


def ift(spectrum):
    result = []
    for i in range(len(spectrum)):
        result.append(conjugate(spectrum[i]))

    result = fft(result)
    for i in range(len(result)):
        result[i] = (conjugate(result[i]))

    for i in range(len(result)):
        result[i] = (scale(result[i], 1 / len(spectrum)))

    return result


def low_filter(signal, threshold):
    fft_transformed = normalize_fft(fft(signal))
    for i in range(len(fft_transformed) // 2 - threshold, 0, -1):
        fft_transformed[i] = {'cos': 0, 'sin': 0}

    for i in range(len(fft_transformed) // 2 - 1 + threshold, len(fft_transformed)):
        fft_transformed[i] = {'cos': 0, 'sin': 0}

    return ift(normalize_fft(fft_transformed))


def high_filter(signal, threshold):
    fft_transformed = normalize_fft(fft(signal))
    for i in range(len(fft_transformed) // 2 - threshold, len(fft_transformed) // 2 + threshold):
        fft_transformed[i] = {'cos': 0, 'sin': 0}

    return ift(normalize_fft(fft_transformed))


def band_filter(signal, low, high):
    return high_filter(low_filter(signal, high), low)


def task_2a(axes):
    spectrum = get_spectrum(test_signal())
    axes.set_xlim(X_LIM)
    axes.plot(SPECTRUM_X, spectrum['amplitudes'], label='amplitudes')
    axes.plot(SPECTRUM_X, spectrum['phases'], label='phases')

    axes.set_title('2a')
    axes.legend()


def task_2b(axes):
    signal = test_signal()
    spectrum = get_spectrum(signal)
    recovered_signal = recover_signal(spectrum)
    axes[0].plot(X, signal)
    axes[1].plot(X, recovered_signal)

    axes[0].set_title('2b_signal')
    axes[1].set_title('2b_recovered')


def task_3(axes):
    signal = polyharmonic_signal()
    spectrum = get_spectrum(signal)
    recovered_signal = recover_polyharmonic_signal(spectrum)
    recovered_wo_phases = recover_polyharmonic_signal_wo_phases(spectrum)
    axes[0].set_xlim(X_LIM)
    axes[0].plot(SPECTRUM_X, spectrum['amplitudes'], label='amplitudes')
    axes[0].plot(SPECTRUM_X, spectrum['phases'], label='phases')
    axes[1].plot(X, signal)
    axes[2].plot(X, recovered_signal)
    axes[3].plot(X, recovered_wo_phases)

    axes[0].set_title('3a')
    axes[0].legend()
    axes[1].set_title('3b_signal')
    axes[2].set_title('3b_recovered')
    axes[3].set_title('3c')


def draw_fft(axes):
    signal = polyharmonic_signal()
    complex_signal = signal_to_complex(signal)
    spectrum = convert_to_ampls_phases(convert_spectrum(round(normalize_fft(fft(complex_signal)))))
    axes.set_xlim(X_LIM)
    axes.plot(SPECTRUM_X, spectrum['amplitudes'], label='amplitudes')
    axes.plot(SPECTRUM_X, spectrum['phases'], label='phases')

    axes.set_title('4')
    axes.legend()


def draw_filtered(axes):
    signal = polyharmonic_signal()
    low_filtered = low_filter(signal_to_complex(signal), 10)
    high_filtered = high_filter(signal_to_complex(signal), 10)
    band_filtered = band_filter(signal_to_complex(signal), 5, 10)
    for i in range(len(signal)):
        low_filtered[i] = low_filtered[i]['cos']
        high_filtered[i] = high_filtered[i]['cos']
        band_filtered[i] = band_filtered[i]['cos']

    axes[0].plot(X, signal)
    axes[1].plot(X, low_filtered)
    axes[2].plot(X, high_filtered)
    axes[3].plot(X, band_filtered)

    axes[0].set_title('w/o filter')
    axes[1].set_title('low filter')
    axes[2].set_title('high filter')
    axes[3].set_title('band filter')


task_2a(ax00)
task_2b([ax01, ax02])
task_3([ax10, ax11, ax12, ax20])
draw_fft(ax21)
draw_filtered([ax22, ax30, ax31, ax32])
plt.show()

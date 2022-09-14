import matplotlib.pyplot as plt
import numpy as np

N = 1024

fig = plt.figure(figsize=(30, 15), constrained_layout=True, dpi=100)
spec = fig.add_gridspec(2, 4)

ax00 = fig.add_subplot(spec[0, 0])
ax01 = fig.add_subplot(spec[0, 1])
ax02 = fig.add_subplot(spec[0, 2])
ax03 = fig.add_subplot(spec[0, 3])
ax10 = fig.add_subplot(spec[1, :])


def harmonic_plot(ampl, freq, amount, phase, axes):
    n = np.arange(0, amount + 1, 1)
    func = (ampl * np.sin(((2 * np.pi * freq * n) / amount) + phase))
    axes.plot(n, func)


def polyharmonic_plot(ampls, freqs, amount, phases, harmonics_am, axes):
    n = np.arange(0, amount + 1, 1)

    def func():
        result = 0
        for i in range(harmonics_am):
            result += (ampls[i] * np.sin(((2 * np.pi * freqs[i] * n) / amount) + phases[i]))
        return result

    axes.plot(n, func())


def polyharmomic_plot_with_linear_law(ampls, freqs, phases, max_change, amount, harmonics_am, axes):
    n = np.arange(0, amount + 1, 1)

    def increase_linear_law(start, x):
        return max_change * start * x + start

    def func():
        result = 0
        for i in range(harmonics_am):
            result += increase_linear_law(ampls[i], n / amount) * np.sin(((2 * np.pi * increase_linear_law(freqs[i], n / amount) * n) / amount) + increase_linear_law(phases[i], n / amount))
        return result

    axes.plot(n, func())


def task2_a():
    ampl = 5
    phases = [np.pi / 4, np.pi / 2, 3 * np.pi / 4, 0, np.pi]
    freq = 1
    for phase in phases:
        harmonic_plot(ampl, freq, N, phase, ax00)
    ax00.set_title('A=%d, φ=%s, f=%d' % (ampl, ["%.2f" % phase for phase in phases], freq))


def task2_b():
    ampl = 1
    phase = np.pi
    frequencies = [1, 3, 2, 4, 10]
    for freq in frequencies:
        harmonic_plot(ampl, freq, N, phase, ax01)
    ax01.set_title('A=%d, φ=%.2f, f=%s' % (ampl, phase, frequencies))


def task2_c():
    amplitudes = [3, 5, 10, 4, 8]
    phase = np.pi
    freq = 4
    for ampl in amplitudes:
        harmonic_plot(ampl, freq, N, phase, ax02)
    ax02.set_title('A=%s, φ=%.2f, f=%d' % (amplitudes, phase, freq))


def task2():
    task2_a()
    task2_b()
    task2_c()


def task3():
    harmonics_amount = 5
    amplitudes = [5, 5, 5, 5, 5]
    frequencies = [1, 2, 3, 4, 5]
    phases = [np.pi / 9, np.pi / 4, np.pi / 3, np.pi / 6, 0]
    polyharmonic_plot(amplitudes, frequencies, N, phases, harmonics_amount, ax03)
    ax03.set_title('A=%s, φ=%s, f=%s' % (amplitudes, ["%.2f" % phase for phase in phases], frequencies))


def task4():
    harmonics_amount = 5
    amplitudes = [5, 5, 5, 5, 5]
    frequencies = [10, 20, 30, 40, 50]
    phases = [np.pi / 9, np.pi / 4, np.pi / 3, np.pi / 6, 0]
    max_change = 0.2
    polyharmomic_plot_with_linear_law(amplitudes, frequencies, phases, max_change, N, harmonics_amount, ax10)


task2()
task3()
task4()
plt.show()

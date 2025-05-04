import numpy as np
from collections import Counter
from L4.cubic_congruential import CubicCongruentialGenerator
from L4.numpy_multinomial import generate_sequence
import matplotlib.pyplot as plt


def frequency_test_multinomial(pvals, n, trials):
    """
    Проводит частотный тест для генератора, использующего мультиномиальное распределение.
    
    Параметры:
      pvals (list): Список вероятностей для исходов.
      n (int): Длина каждой сгенерированной цепочки.
      trials (int): Количество экспериментов.
      
    Возвращает:
      numpy.ndarray: Массив наблюдаемых относительных частот для каждого исхода.
    """
    counts = np.zeros(len(pvals))
    for _ in range(trials):
        seq = generate_sequence(pvals, n)
        counts += np.bincount(seq, minlength=len(pvals))
    total = n * trials
    freqs = counts / total
    return freqs

def frequency_test_cubic(generator, n):
    """
    Проводит частотный тест для кубического конгруэнтного генератора.
    
    Параметры:
      generator (CubicCongruentialGenerator): Экземпляр генератора.
      n (int): Количество чисел для генерации.
      
    Возвращает:
      dict: Словарь, где ключ – сгенерированное число, значение – его относительная частота.
    """
    seq = generator.generate_sequence(n)
    counter = Counter(seq)
    total = sum(counter.values())
    freq_dict = {value: count / total for value, count in sorted(counter.items())}
    return freq_dict

def get_plots():
    """
    Строит графики для частотного теста обоих генераторов и возвращает объекты matplotlib.figure.
    
    Возвращает:
      tuple: (fig_multinomial, fig_cubic)
    """
    pvals = [0.3, 0.7]
    n = 1000
    trials = 100 
    freq_multinomial = frequency_test_multinomial(pvals, n, trials)

    fig1, ax1 = plt.subplots()
    indices = np.arange(len(pvals))
    ax1.bar(indices, freq_multinomial, tick_label=[f"Исход {i}" for i in indices], color='skyblue')
    for i, expected in enumerate(pvals):
        ax1.axhline(y=expected, color='red', linestyle='--', label=f"Ожидаемая частота {i}" if i == 0 else "")
    ax1.set_title("Частотный тест для мультиномиального генератора")
    ax1.legend()

    cubic_gen = CubicCongruentialGenerator(a=53668, b=400144, c=12211, k=15, x0=1, d=0)
    n_cubic = 1000
    freq_cubic = frequency_test_cubic(cubic_gen, n_cubic)
    
    fig2, ax2 = plt.subplots()
    ax2.bar(list(freq_cubic.keys()), list(freq_cubic.values()), color='lightgreen')
    ax2.set_title("Частотный тест для кубического конгруэнтного генератора")
    ax2.set_xlabel("Значения")
    ax2.set_ylabel("Частота")

    return fig1, fig2
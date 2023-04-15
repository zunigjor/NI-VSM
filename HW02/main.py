# NI-VSM Domaci ukol 02
# LS 2022/23
# Clenove
# Kristýna Janovská - janovkri (reprezentant)
# Jakub Rigoci - rigocjak
# Jorge Zuňiga - zunigjor
import math
from collections import Counter
from typing import Dict
import numpy as np
from plotting import *
from scipy import stats
import pandas as pd


########################################################################################################################
# 1. Z obou datových souborů načtěte texty k analýze. Pro každý text zvlášť odhadněte
# základní charakteristiky délek slov, tj. střední hodnotu a rozptyl. Graficky znázorněte
# rozdělení délek slov.
########################################################################################################################
def get_word_lengths(file_str: str) -> list[int]:
    return [len(x) for x in file_str.split(" ")]


def characteristics(file_str: str) -> (float, float):
    lengths = get_word_lengths(file_str)
    return np.mean(lengths), np.var(lengths)


########################################################################################################################
# 2. Pro každý text zvlášť odhadněte pravděpodobnosti písmen (symbolů mimo mezery),
# které se v textech vyskytují. Výsledné pravděpodobnosti graficky znázorněte.
########################################################################################################################
def char_probabilities(text: str) -> Dict[str, float]:
    """
    Z textu vypocita odhadovanou pravdepodobnost vyskytu pismen.
    :param text: Text
    :return: Slovnik znaku a jejich pravdepodobnosti
    """
    char_prob = dict(Counter(text))
    for key in char_prob.keys():
        char_prob[key] /= len(text)
    char_prob.pop(" ")  # odstraneni mezer
    return char_prob


########################################################################################################################
# 3. Na hladině významnosti 5% otestujte hypotézu, že rozdělení délek slov nezávisí na tom,
# o který jde text. Určete také p-hodnotu testu.
########################################################################################################################
def word_dependency_test(file_1_name: str, file_1_str: str, file_2_name: str, file_2_str: str) -> None:
    """
    H0: rozdeleni delek slov je nezavisle na textu
    HA: rozdeleni delek slov je zavisle na textu

    Z kapitoly 10.7:
    Diskretni nahodna velicina X s k hodnotami 1...k s pravdepodobnostmi p1...pk
    rozdeleni X: p = (p1...pk)^T
    -> nahodny vyber X1...Xn o velikosti n z rozdeleni p -> vysledky zaznamenany pomoci CETNOSTI
    -> Nahodne veliciny N1...Nk: Ni=|{j |Xj = i}
    -> Multinomicke rozdeleni M(n, p): Sdruzene diskretni rozdeleni nahodneho vektoru N = (N1...Nk)
    -> PEARSONOVA STATISTIKA -> Chi^2

    Testujeme shodnost diskretnich rozdeleni f1, f2
    """
    H0 = "H0: Rozdělení délek slov nezávisí na tom, o který jde text."
    HA = "HA: Rozdělení délek slov závisí na tom, o který jde text."
    print(H0)
    print(HA)
    alpha = 0.05

    file_1_counts = Counter(get_word_lengths(file_1_str))
    file_2_counts = Counter(get_word_lengths(file_2_str))

    max_word_len = max(max(file_1_counts), max(file_2_counts))

    cont_table = pd.DataFrame(
        [file_1_counts, file_2_counts],
        index=[file_1_name, file_2_name],
        columns=range(1, max_word_len + 1)
    ).fillna(0).astype(int)

    test_chi2, test_p, test_dof, test_expected = stats.chi2_contingency(cont_table)

    # Percent point function -> hodnota z rozdeleni bude mensi rovna hodnote vracene PPF s danou psti
    # -> vraci kritickou hodnotu
    ppf = stats.chi2.ppf(1 - alpha, test_dof)

    print(f'Testová statistika χ² = {test_chi2:.4g}')
    print(f'p-hodnota = {test_p:.4g}')
    print(f'PPF = {ppf:.4g}')
    if test_chi2 < ppf:
        print("Nezamítáme nulovou hypotézu H0.")
        print(H0)
    else:
        print("Zamítáme nulovou hypotézu H0 ve prospěch alternativní hypotézy HA.")
        print(HA)
    return

########################################################################################################################
# 4. Na hladině významnosti 5% otestujte hypotézu, že se střední délky slov v obou textech rovnají.
# Určete také p-hodnotu testu.
########################################################################################################################


def medium_length_test(file_1_str: str, file_2_str: str) -> None:
    """
    H0: Střední délky slov v obou textech se rovnají
    HA: Střední délky slov v obou textech se nerovnají
    ->
        H0: μ1 = μ2
        HA: μ1 != μ2
    - mame znamy rozptyl
    - pouzijeme dvouvyberovy t-test
    """
    H0 = "H0: Střední délky slov v obou textech se rovnají."
    HA = "HA: Střední délky slov v obou textech se nerovnají."
    print(H0)
    print(HA)
    alpha = 0.05
    file1_mean, file_1_var = characteristics(file_1_str)
    file2_mean, file_2_var = characteristics(file_2_str)
    file_1_counts = get_word_lengths(file_1_str)
    file_2_counts = get_word_lengths(file_2_str)

    test_var_stat, test_var_p = stats.levene(file_1_counts, file_2_counts)

    # H0 = var1 = var2
    # HA = var1 != var2
    test_equal_variances = test_var_p > alpha
    print(f'Levenův test: p-hodnota = {test_var_p}')
    print(f'Rozptyly jsou si rovny = {test_equal_variances}')

    # testovaci statistika a p-hodnota
    test_stat, test_p = stats.ttest_ind(file_1_counts, file_2_counts, equal_var=test_equal_variances)

    n = len(file_1_counts)
    m = len(file_2_counts)
    s2_X = file_1_var
    s2_Y = file_2_var
    s2_X_div_n = s2_X / n
    s2_Y_div_m = s2_Y / m
    s_d = math.sqrt(s2_X_div_n + s2_Y_div_m)
    n_d = (s_d ** 4) / ((1/(n-1)) * (s2_X_div_n ** 2) + (1/(m-1)) * (s2_Y_div_m ** 2))
    q = 1 - 0.05 / 2
    critical_val = stats.t.ppf(q, n_d)

    print(f'PPF = {critical_val}')
    print(f'Testová statistika = {test_stat:.4g}')
    print(f'p-hodnota = {test_p:.4g}')

    if abs(test_stat) < critical_val:
        print("Nezamítáme nulovou hypotézu H0.")
        print(H0)
    else:
        print("Zamítáme nulovou hypotézu H0 ve prospěch alternativní hypotézy HA.")
        print(HA)
    return


########################################################################################################################
# 5. Na hladině významnosti 5% otestujte hypotézu, že rozdělení písmen nezávisí na tom, o který jde text.
# Určete také p-hodnotu testu.
########################################################################################################################
def char_count(text: str) -> Dict[str, int]:
    return Counter("".join(text.split(" ")))


def char_dependency_test(file_1_name: str, file_1_str: str, file_2_name: str, file_2_str: str) -> None:
    H0 = "H0: Rozdělení písmen nezávisí na tom, o který jde text."
    HA = "HA: Rozdělení písmen závisí na tom, o který jde text."
    print(H0)
    print(HA)

    alpha = 0.05

    file_1_counts = char_count(file_1_str)
    file_2_counts = char_count(file_2_str)

    cont_table = pd.DataFrame(
        [file_1_counts, file_2_counts],
        index=[file_1_name, file_2_name]
    ).fillna(0).astype(int)
    test_chi2, test_p, test_dof, test_expected = stats.chi2_contingency(cont_table)
    ppf = stats.chi2.ppf(1 - alpha, test_dof)

    print(f'Testová statistika χ² = {test_chi2:.5g}')
    print(f'p-hodnota = {test_p:.5g}')
    print(f'PPF = {ppf:.5g}')
    if test_chi2 < ppf:
        print("Nezamítáme nulovou hypotézu H0.")
        print(H0)
    else:
        print("Zamítáme nulovou hypotézu H0 ve prospěch alternativní hypotézy HA.")
        print(HA)
    return

########################################################################################################################
# Main
########################################################################################################################
if __name__ == '__main__':
    # Spocitame parametry
    K = 20
    L = len("Janovska")
    X = ((K * L * 23) % 20) + 1
    Y = ((X + ((K * 5 + L * 7) % 19)) % 20) + 1
    file_1_name = str(X).zfill(3) + ".txt"
    file_2_name = str(Y).zfill(3) + ".txt"
    file_1_path = "../inputs/" + file_1_name
    file_2_path = "../inputs/" + file_2_name
    # Cteme pouze 2. radek
    file_1_str = open(file_1_path).readlines()[1:][0]
    file_2_str = open(file_2_path).readlines()[1:][0]
    # 1
    print("="*30 + " 1 " + "="*30)
    file_1_characteristics = characteristics(file_1_str)
    file_2_characteristics = characteristics(file_2_str)
    length_distribution(file_1_str, file_1_name, "./results")
    length_distribution(file_2_str, file_2_name, "./results")
    print(f'Mean {file_1_name} = {file_1_characteristics[0]}')
    print(f'Var. {file_1_name} = {file_1_characteristics[1]}')
    print(f'Mean {file_2_name} = {file_2_characteristics[0]}')
    print(f'Var. {file_2_name} = {file_2_characteristics[1]}')
    print()
    # 2
    print("=" * 30 + " 2 " + "=" * 30)
    file_1_char_probs = char_probabilities(file_1_str)
    file_2_char_probs = char_probabilities(file_2_str)
    plot_char_prob(file_1_char_probs, file_1_name, "./results")
    plot_char_prob(file_2_char_probs, file_2_name, "./results")
    print()
    # 3
    print("=" * 30 + " 3 " + "=" * 30)
    word_dependency_test(file_1_name, file_1_str, file_2_name, file_2_str)
    print()
    # 4
    print("=" * 30 + " 4 " + "=" * 30)
    medium_length_test(file_1_str, file_2_str)
    print()
    # 5
    print("=" * 30 + " 5 " + "=" * 30)
    char_dependency_test(file_1_name, file_1_str, file_2_name, file_2_str)
    print()

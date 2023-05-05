# NI-VSM Domaci ukol 02
# LS 2022/23
# Clenove
# Kristýna Janovská - janovkri (reprezentant)
# Jakub Rigoci - rigocjak
# Jorge Zuňiga - zunigjor
from collections import Counter
from typing import Dict
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
import scipy.stats as stats
from typing import Dict


########################################################################################################################
# Z obou datových souborů načtěte texty k analýze.
# Pro každý text zvlášť zjistěte absolutní četnosti jednotlivých znaků (symbolů včetně mezery),
# které se v textech vyskytují.
# Dále předpokládejme, že první text je vygenerován z homogenního markovského řetězce s diskrétním časem.
########################################################################################################################
#(2b) Za předpokladu výše odhadněte matici přechodu markovského řetězce pro první text.
# Pro odhad matice přechodu vizte přednášku 17.
# Odhadnuté pravděpodobnosti přechodu vhodně graficky znázorněte, např. použitím heatmapy.
########################################################################################################################
def toInt(char: str) -> int:
    if char == '␣':
        return 0
    return int(ord(char) - 96)


def char_count(text: str) -> Dict[str, int]:
    return dict(sorted(dict(Counter(text)).items()))


def transitionMatrix(file_str: str):
    file_char_counts = char_count(file_str)
    # Mame 27 znakov
    P = np.zeros((len(file_char_counts), len(file_char_counts)))
    # z kapitoly 15: matice prechodu lze odhadnout pomoci cetnosti prechodu - pro kazdou dvojici
    # Z prednasky: Maximálne verohodným odhadem matice prechodu P je matice P^ s prvky:
    # P^_ij = n_ij / n_i., kde n_i. = sum_j( n_ij )
    for i in range(len(file_str) - 1):
        char = file_str[i]
        nextChar = file_str[i+1]
        P[toInt(char)][toInt(nextChar)] += 1

    for i in range(len(file_char_counts)):
        sum = 0
        for j in range(len(file_char_counts)):
            sum += P[i][j]
        for j in range(len(file_char_counts)):
            P[i][j] = P[i][j] / sum

    plt.imshow(P, cmap='Reds')
    plt.colorbar()
    plt.savefig('results/heatmap')
    return P


########################################################################################################################
#(2b) Na základě matice z předchozího bodu najděte stacionární rozdělení π tohoto řetězce pro první text.
########################################################################################################################
def stationaryDistribution(P):
    """
    vektor pi = (pi1, pi2, ...) je stacionarni rozdeleni, pokud resi soustavu rovnic
    pi * P = pi
    sum_i pi_i = 1
    ---------------
    pi = pi * P
    0 = pi * ( P - I )
    0^T = (P - I)^T * pi^T
    ker(P-I)^T => null space
    """
    I = np.eye(P.shape[0])
    W = np.transpose(P - I)
    pi = la.null_space(W)
    # normalizace
    pi = np.transpose(pi/sum(pi))
    return pi[0]


########################################################################################################################
#(2b) Porovnejte rozdělení znaků druhého textu se stacionárním rozdělením π,
# tj. na hladině významnosti 5 % otestujte hypotézu, že rozdělení znaků
# druhého testu se rovná rozdělení π z předchozího bodu.
########################################################################################################################


def test(pi, text):
    # 1. rozdeleni textu
    text_dist = char_count(text)
    # 2. priprava rozdeleni pro chisquare
    # This test is invalid when the observed or expected frequencies in each category are too small.
    # A typical rule is that all of the observed and expected frequencies should be at least 5.
    # src: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
    n = sum(text_dist.values())
    npi = n*pi
    sortedNpi = sorted(npi)
    mergedNpi = [sortedNpi[0] + sortedNpi[1]] + sortedNpi[2:]
    # 3. chisquare test
    # H0: Rozdeleni znaku se rovna stacionarnimu rozdeleni pi.
    # HA: Rozdeleni znaku se nerovna stacionarnimu rozdeleni pi.
    alpha = 0.05
    dist_arr = np.array(list(text_dist.values()))
    sortedDist_arr = sorted(dist_arr)
    merged_dist_arr = [sortedDist_arr[0] + sortedDist_arr[1]] + sortedDist_arr[2:]
    chi2, p = stats.chisquare(merged_dist_arr, mergedNpi)
    print(f'Testová statistika χ² = {chi2:.4g}')
    print(f'P-hodnota = {p:.4g}')
    if(p > alpha):
        print('H0 nezamítáme.')
    else:
        print('H0 zamítáme ve prospěch HA.')
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
    # Cteme pouze 2 radek a nahrazujeme mezery za symbol ␣
    file_1_str = open(file_1_path).readlines()[1:][0].replace(" ", "␣")
    file_2_str = open(file_2_path).readlines()[1:][0].replace(" ", "␣")
    # 0
    print("=" * 80)
    print("File 1 counts:")
    print(char_count(file_1_str))
    print("=" * 80)
    print("File 2 counts:")
    print(char_count(file_2_str))
    print("=" * 80)
    # 1
    file_1_transition_matrix = transitionMatrix(file_1_str)
    # 2
    file_1_stationary_distribution = stationaryDistribution(file_1_transition_matrix)
    print("Stationary distribution:")
    print(file_1_stationary_distribution)
    print("=" * 80)
    # 3
    test(file_1_stationary_distribution, file_2_str)
    print("=" * 80)

# NI-VSM Domaci ukol 01
# LS 2022/23
# Clenove
# Kristýna Janovská - janovkri (reprezentant)
# Jakub Rigoci - rigocjak
# Jorge Zuňiga - zunigjor
import math
from collections import Counter
from typing import Dict
from plotting import plot_char_prob


########################################################################################################################
# (1)(1b) Z obou datových souborů načtěte texty k analýze. Pro každý text zvlášť odhadněte pravděpodobnosti znaků
# (symbolů včetně mezery), které se v textech vyskytují. Výsledné pravděpodobnosti graficky znázorněte.
########################################################################################################################
def char_probability(input_str: str) -> Dict[str, float]:
    """
    Z textu vypocita odhadovanou pravdepodobnost vyskytu znaku.
    :param input_str: Text
    :return: Slovnik znaku a jejich pravdepodobnosti
    """
    char_prob = dict(Counter(input_str))
    for key in char_prob.keys():
        char_prob[key] /= len(input_str)
    return char_prob


########################################################################################################################
# (2)(1b) Pro každý text zvlášť spočtěte entropii rozdělení znaků.
########################################################################################################################
def get_entropy(input_char_prob: {}) -> float:
    """
    Entropy = - sum_x(p(x)*logp(x))
    :return: Entropie daného textu
    """
    entropy = 0
    for i in input_char_prob:
        entropy += -(input_char_prob[i] * math.log2(input_char_prob[i]))
    return entropy


########################################################################################################################
# (3)(2b) Nalezněte optimální binární instantní kód C pro kódování znaků prvního z textů.
########################################################################################################################
class Node:
    def __init__(self, char:str=None, prob:float=0, left=None, right=None):
        self.char = char
        self.prob = prob
        self.left = left
        self.right = right


def get_sorted_list(file):
    pst_1 = char_probability(file)
    sorted_list = sorted(pst_1.items(), key=lambda item: item[1])
    return sorted_list


def construct_code(node, allCodes, code=''):
    if len(node.char) == 1:
        allCodes[node.char] = code
    else:
        # pro x, ktere vzniklo spojenim hodnot u a v vytvorime kodove slovo mene pravdepodobne hodnoty
        # pripojenim symbolu 1 za kodove slovo C(x) a kodove slovo vice pravdepod. hodnoty pripojenim
        # symbolu 0 za C(x)
        construct_code(node.left, allCodes, code + '0')
        construct_code(node.right, allCodes, code + '1')


def binary_code(file) -> Dict[str, str]:
    """
    Věta 6.17 - Huffmanův kód je optimální.
    :param file:
    :return:
    """
    sorted_pst_nodes = [Node(char, prob) for char, prob in get_sorted_list(file)]

    if len(sorted_pst_nodes) % 2:
        sorted_pst_nodes.append(Node('', 0))
    # 1. spojit 2 nejmin pravdepodobne hodnoty do 1
    # 2. spajame, dokud nezustane jedina hodnota
    while len(sorted_pst_nodes) > 1:
        sorted_pst_nodes = sorted(sorted_pst_nodes, key=lambda node: node.prob)
        node1 = sorted_pst_nodes.pop(0)
        node2 = sorted_pst_nodes.pop(0)

        sorted_pst_nodes.append(Node(char=node1.char + node2.char, prob=node1.prob + node2.prob, left=node1, right=node2 ))

    # 3. konstrukce kodoveho slova
    codes = {}
    construct_code(sorted_pst_nodes[0], codes)

    return codes


########################################################################################################################
# (4)(2b) Pro každý text zvlášť spočtěte střední délku kódu C a porovnejte ji s entropií rozdělení znaků.
# Je kód C optimální i pro druhý text?
########################################################################################################################
def encoding_mean(input_char_prob: Dict[str, float], encoding: Dict[str, str]) -> float:
    """
    L(C) = sum_x(l(x)*p(x))
    l(x) ... délka kódoveho slova příslušejícího prvku x
    :return: Střední délka kódového slova
    """
    mean_length = 0
    for key in encoding.keys():
        mean_length += len(encoding[key])*input_char_prob[key]
    return mean_length


def is_code_optimal(entropy: float, mean: float) -> bool:
    """
    Věta 6.14: Pokud je kód optimální, platí H_d(X) <= L(C*) < H_d(X) + 1
    = optimálním kódem se můžeme od dolní meze dané entropií vzdálit max. o 1
    :param entropy: entropie daného textu
    :param mean: střední délka daného kódu
    :return: True, pokud je kód optimální
    """
    return entropy <= mean < entropy + 1


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
    # 1
    char_pst_file_1 = char_probability(file_1_str)
    char_pst_file_2 = char_probability(file_2_str)
    # 2
    entropy_file_1 = get_entropy(char_pst_file_1)
    entropy_file_2 = get_entropy(char_pst_file_2)
    # 3
    C = binary_code(file_1_str)
    # 4
    file_1_encoding_mean = encoding_mean(char_pst_file_1, C)
    file_2_encoding_mean = encoding_mean(char_pst_file_2, C)
    # 4.5
    optimality_1 = is_code_optimal(entropy_file_1, file_1_encoding_mean)
    optimality_2 = is_code_optimal(entropy_file_2, file_2_encoding_mean)
    # Plot
    plot_char_prob(char_pst_file_1, file_1_name, "results")
    plot_char_prob(char_pst_file_2, file_2_name, "results")
    # Results
    # File 1
    print(f"File 1: {file_1_name}")
    print(f"Entropy: {entropy_file_1}")
    print(f"L(C): {file_1_encoding_mean}")
    if optimality_1:
        print(f"Code is optimal for {file_1_name}")
    else:
        print(f"Code is NOT optimal for {file_1_name}")
    print()
    # File 2
    print(f"File 2: {file_2_name}")
    print(f"Entropy: {entropy_file_2}")
    print(f"L(C): {file_2_encoding_mean}")
    if optimality_2:
        print(f"Code is optimal for {file_2_name}")
    else:
        print(f"Code if NOT optimal for {file_2_name}")

    print()
    print("Code: ")
    print(sorted(C.items()))

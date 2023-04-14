from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict


def length_distribution(file_str: str, caption: str, save_folder: str) -> None:
    lengths_count = Counter([len(x) for x in file_str.split(" ")])
    sorted_data = dict(sorted(lengths_count.items()))
    x_values = list(sorted_data.keys())
    y_values = list(sorted_data.values())
    fig, axs = plt.subplots()
    fig.suptitle(f'Rozdělení délky slov souboru {caption}')
    plt.bar(x_values, y_values)
    plt.xticks(x_values)
    plt.xlabel('Délky slov')
    plt.ylabel('Frekvence výskytu')
    plt.grid()
    plt.savefig(save_folder + '/' + "word_lens_" + caption[0:3] + '.png')
    print(save_folder + '/' + "word_lens_" + caption[0:3] + '.png')


def plot_char_prob(char_prob: Dict[str, float], caption, save_folder):
    # Abecedni serazeni
    char_prob = dict(sorted(char_prob.items()))
    # Nastaveni plotu
    fig, axs = plt.subplots(1, 2, figsize=(15, 3))
    fig.suptitle(f"Pravděpodobnosti písmen souboru {caption}")
    bar_x_locations = np.arange(len(char_prob))
    # Abecedni
    plt.sca(axs[0])
    plt.bar(bar_x_locations, char_prob.values(), align='center')
    plt.xticks(bar_x_locations, char_prob.keys())
    plt.grid()
    # Pravdepodobnostni
    plt.sca(axs[1])
    char_prob = dict(sorted(char_prob.items(), key=lambda item: item[1], reverse=True))
    bar_x_locations = np.arange(len(char_prob))
    plt.bar(bar_x_locations, char_prob.values(), align='center')
    plt.xticks(bar_x_locations, char_prob.keys())
    plt.grid()
    plt.savefig(save_folder + '/' + "char_prob_" + caption[0:3] + '.png')
    print(save_folder + '/' + "char_prob_" + caption[0:3] + '.png')


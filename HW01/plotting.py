import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

def plot_char_prob(char_prob: Dict[str, float], caption, save_folder):
    # Abecedni serazeni
    char_prob = dict(sorted(char_prob.items()))
    # Nastaveni plotu
    fig, axs = plt.subplots(1, 2, figsize=(15, 3))
    fig.suptitle(caption)
    bar_x_locations = np.arange(len(char_prob))
    # Abecedni
    plt.sca(axs[0])
    plt.bar(bar_x_locations, char_prob.values(), align = 'center')
    plt.xticks(bar_x_locations, char_prob.keys())
    plt.grid()
    # Pravdepodobnostni
    plt.sca(axs[1])
    char_prob = dict(sorted(char_prob.items(), key=lambda item: item[1], reverse=True))
    bar_x_locations = np.arange(len(char_prob))
    plt.bar(bar_x_locations, char_prob.values(), align = 'center')
    plt.xticks(bar_x_locations, char_prob.keys())
    plt.grid()
    plt.savefig(save_folder + '/' + caption[0:3] + '.png')

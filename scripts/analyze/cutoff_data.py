from collections import defaultdict
from statistics import median
import os

import matplotlib.pyplot as plt


def mkdir_safe(pathdir):
    try:
        os.mkdir(pathdir)
    except FileExistsError:
        pass


def read_data(filename):
    data = defaultdict(list)

    with open(filename) as f:
        for line in f:
            cutoff, time = [int(num) for num in line.split()]
            data[cutoff] += [time]
    
    for cutoff in data:
        data[cutoff] = median(data[cutoff])
    
    return data


def plot_and_save(x, y, saveto):
    plt.plot(x, y, linestyle='-', marker='o')
    
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel(r'Cutoff', fontsize=12)
    plt.ylabel(r'Execution time [$\mu s$]', fontsize=12)
    plt.xscale('log')
    
    plt.savefig(saveto)
    plt.clf()


def analyze_cutoff(path, outpath, pngpath):
    data = read_data(path)
    cutoffs, times = zip(*sorted(data.items()))
    plot_and_save(cutoffs, times, pngpath)    
    
    to_write = zip(cutoffs, times)
    with open(outpath, 'w') as f:
        for cutoff, time in to_write:
            print(f'{cutoff}\t\t{time}', file=f)


if __name__ == '__main__':
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    mkdir_safe('results/txt')
    mkdir_safe('results/img')

    analyze_cutoff(
        'results/raw/cutoff_merge.txt', 
        'results/txt/cutoff_merge.txt', 
        'results/img/cutoff_merge.png')
    analyze_cutoff(
        'results/raw/cutoff_sort.txt',
        'results/txt/cutoff_sort.txt',
        'results/img/cutoff_sort.png')

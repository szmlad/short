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
    data_ser = defaultdict(list)
    data_par = defaultdict(list)
    data_stl = defaultdict(list)

    with open(filename) as f:
        for line in f:
            size, ser, par, stl = [float(num) for num in line.split()]
            data_ser[size] += [ser]
            data_par[size] += [par]
            data_stl[size] += [stl]

    for size in data_ser:
        data_ser[size] = median(data_ser[size])
    for size in data_par:
        data_par[size] = median(data_par[size])
    for size in data_stl:
        data_stl[size] = median(data_stl[size])

    return dict(data_ser), dict(data_par), dict(data_stl)


def plot_and_save(x, y1, y2, y3, saveto):
    plt.plot(x, y1, linestyle='-', marker='o', label='Serial')
    plt.plot(x, y2, linestyle='-', marker='x', label='Parallel')
    plt.plot(x, y3, linestyle='-', marker='d', label='STL')

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel(r'Vector size', fontsize=12)
    plt.ylabel(r'Execution time [$\mu s$]', fontsize=12)
    plt.xscale('log')
    plt.legend(loc='upper left')
    
    plt.savefig(saveto)
    plt.clf()


def analyze_perf(path, outpath, pngpath):
    ser, par, stl = read_data(path)
    sizes, ser = zip(*sorted(ser.items()))
    _    , par = zip(*sorted(par.items()))
    _    , stl = zip(*sorted(stl.items()))
    plot_and_save(sizes, ser, par, stl, pngpath)
    
    to_write = zip(sizes, ser, par, stl)
    with open(outpath, 'w') as f:
        for sizes, ser, par, stl in to_write:
            print(f'{sizes}\t\t{ser}\t\t{par}\t\t{stl}', file=f)


if __name__ == '__main__':
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    mkdir_safe('results/txt')
    mkdir_safe('results/img')

    analyze_perf(
        'results/raw/perf_merge_s.txt',
        'results/txt/perf_merge_s.txt',
        'results/img/perf_merge_s.png')
    analyze_perf(
        'results/raw/perf_merge_l.txt',
        'results/txt/perf_merge_l.txt',
        'results/img/perf_merge_l.png')
    analyze_perf(
        'results/raw/perf_sort_s.txt',
        'results/txt/perf_sort_s.txt',
        'results/img/perf_sort_s.png')
    analyze_perf(
        'results/raw/perf_sort_l.txt',
        'results/txt/perf_sort_l.txt',
        'results/img/perf_sort_l.png')

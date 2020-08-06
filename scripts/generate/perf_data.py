import os
import pathlib

merge_small = 'build/short m resources/merge/test/{}.txt >> results/raw/perf_merge_s.txt'
merge_large = 'build/short m resources/merge/test/{}.txt >> results/raw/perf_merge_l.txt'
sort_small  = 'build/short s resources/sort/test/{}.txt >> results/raw/perf_sort_s.txt'
sort_large  = 'build/short s resources/sort/test/{}.txt >> results/raw/perf_sort_l.txt'
bifur_pt    = 50000


def mkdir_safe(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


def main():
    mkdir_safe('results')
    mkdir_safe('results/raw')

    for file in pathlib.Path('resources/merge/test').iterdir():
        file = file.stem
        if int(file) <= bifur_pt:
            os.system(merge_small.format(file))
        else:
            os.system(merge_large.format(file))

    for file in pathlib.Path('resources/sort/test').iterdir():
        file = file.stem
        if int(file) <= bifur_pt:
            os.system(sort_small.format(file))
        else:
            os.system(sort_large.format(file))


if __name__ == '__main__':
    main()
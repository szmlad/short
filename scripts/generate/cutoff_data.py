import os
import pathlib


merge_data = 'build/short mc resources/merge/test/{}.txt > results/raw/cutoff_merge.txt'
sort_data  = 'build/short sc resources/sort/test/{}.txt > results/raw/cutoff_sort.txt'


def mkdir_safe(pathdir):
    try:
        os.mkdir(pathdir)
    except FileExistsError:
        pass


def find_longest_vec(path):
    return max(int(size) for size in map(lambda f: f.stem, path.iterdir()))


if __name__ == '__main__':
    mkdir_safe('results')
    mkdir_safe('results/raw')
    
    longest_vec_merge = find_longest_vec(pathlib.Path('resources/merge/test'))
    longest_vec_sort  = find_longest_vec(pathlib.Path('resources/sort/test'))

    os.system(merge_data.format(longest_vec_merge))
    os.system(sort_data.format(longest_vec_sort))
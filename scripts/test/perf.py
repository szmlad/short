import os
import sys


merge_proc = 'build/short m resources/merge/test/{}.txt'
sort_proc  = 'build/short s resources/sort/test/{}.txt'


def get_sizes(filename):
    sizes = []
    with open(filename) as f:
        for line in f:
            sizes.append(int(line))
    sizes.sort()
    length = len(sizes)
    return sizes[length//3], sizes[2*length//3], sizes[length-1]


if __name__ == '__main__':
    s, m, l = get_sizes('resources/sizes.txt')
    if sys.argv[1] == 's':
        print(f'Testing for {s} element vectors...')
        print('Merge\t\tSerial\t\tParallel\tSTL')
        os.system(merge_proc.format(s))
        print()
        print('Sort\t\tSerial\t\tParallel\tSTL')
        os.system(sort_proc.format(s))
    elif sys.argv[1] == 'm':
        print(f'Testing for {m} element vectors...')
        print('Merge\t\tSerial\t\tParallel\tSTL')
        os.system(merge_proc.format(m))
        print()
        print('Sort\t\tSerial\t\tParallel\tSTL')
        os.system(sort_proc.format(m))
    else:
        print(f'Testing for {l} element vectors...')
        print('Merge\t\tSerial\t\tParallel\tSTL')
        os.system(merge_proc.format(l))
        print()
        print('Sort\t\tSerial\t\tParallel\tSTL')
        os.system(sort_proc.format(l))
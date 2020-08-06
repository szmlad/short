import os
import sys


merge_proc = 'build/short m resources/merge/test/{0}.txt resources/merge/ref/{0}.txt'
sort_proc  = 'build/short s resources/sort/test/{0}.txt resources/sort/ref/{0}.txt'


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
        os.system(merge_proc.format(s))
        os.system(sort_proc.format(s))
    elif sys.argv[1] == 'm':
        print(f'Testing for {m} element vectors...')
        os.system(merge_proc.format(m))
        os.system(sort_proc.format(m))
    else:
        print(f'Testing for {l} element vectors...')
        os.system(merge_proc.format(l))
        os.system(sort_proc.format(l))
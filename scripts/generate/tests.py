from itertools import chain
import os
import random


lower = 0
upper = 1000000


def mkdir_safe(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


def generate_tests(size, lower, upper):
    xs = []
    for _ in range(size):
        xs.append(random.randint(lower, upper))

    left  = xs[:size//2]
    right = xs[size//2:]

    with open(f'resources/merge/test/{size}.txt', 'w') as f:
        for e in chain(sorted(left), sorted(right)):
            print(e, file=f)

    with open(f'resources/merge/ref/{size}.txt', 'w') as f:
        for e in sorted(xs):
            print(e, file=f)

    with open(f'resources/sort/test/{size}.txt', 'w') as f:
        for e in xs:
            print(e, file=f)

    with open(f'resources/sort/ref/{size}.txt', 'w') as f:
        for e in sorted(xs):
            print(e, file=f)


def create_dir_structure():
    mkdir_safe('resources')

    mkdir_safe('resources/merge')
    mkdir_safe('resources/merge/test')
    mkdir_safe('resources/merge/ref')

    mkdir_safe('resources/sort')
    mkdir_safe('resources/sort/test')
    mkdir_safe('resources/sort/ref')

    mkdir_safe('resources/trivial')
    
    mkdir_safe('resources/trivial/sort')
    mkdir_safe('resources/trivial/sort/test')
    mkdir_safe('resources/trivial/sort/ref')

    mkdir_safe('resources/trivial/merge')
    mkdir_safe('resources/trivial/merge/test')
    mkdir_safe('resources/trivial/merge/ref')


def performance_tests(sizes_path):
    with open(sizes_path) as f:
        for line in f:
            size = int(line)
            generate_tests(size, lower, upper)     


def empty():
    open('resources/trivial/merge/test/empty.txt', 'w').close()
    open('resources/trivial/merge/ref/empty.txt', 'w').close()
    open('resources/trivial/sort/test/empty.txt', 'w').close()
    open('resources/trivial/sort/ref/empty.txt', 'w').close()


def one():
    n = random.randint(lower, upper)
    with open('resources/trivial/merge/test/one.txt', 'w') as f:
        print(n, file=f)

    with open('resources/trivial/merge/ref/one.txt', 'w') as f:
        print(n, file=f)

    with open('resources/trivial/sort/test/one.txt', 'w') as f:
        print(n, file=f)

    with open('resources/trivial/sort/ref/one.txt', 'w') as f:
        print(n, file=f)


def same():
    n = random.randint(lower, upper)
    with open('resources/trivial/merge/test/same.txt', 'w') as f:
        for _ in range(1000000):
            print(n, file=f)

    with open('resources/trivial/merge/ref/same.txt', 'w') as f:
        for _ in range(1000000):
            print(n, file=f)

    with open('resources/trivial/sort/test/same.txt', 'w') as f:
        for _ in range(1000000):
            print(n, file=f)

    with open('resources/trivial/sort/ref/same.txt', 'w') as f:
        for _ in range(1000000):
            print(n, file=f)


def trivial_tests():
    empty()
    one()
    same()


if __name__ == '__main__':
    create_dir_structure()
    performance_tests('resources/sizes.txt')
    trivial_tests()

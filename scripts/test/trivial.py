import os


merge_proc = 'build/short m resources/trivial/merge/test/{0}.txt resources/trivial/merge/ref/{0}.txt'
sort_proc  = 'build/short s resources/trivial/sort/test/{0}.txt resources/trivial/sort/ref/{0}.txt'


if __name__ == '__main__':
    print('Empty vector')
    os.system(merge_proc.format('empty'))
    os.system(sort_proc.format('empty'))

    print('One element vector')
    os.system(merge_proc.format('one'))
    os.system(sort_proc.format('one'))

    print('Vector of 1,000,000 equal elements')
    os.system(merge_proc.format('same'))
    os.system(merge_proc.format('same'))
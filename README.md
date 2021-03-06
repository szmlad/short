# Short

This repository contains an implementation of the parallel merge sort algorithm in C++ using [Intel Thread Building Blocks](https://github.com/oneapi-src/oneTBB) library for task-based parallelism and a series of scripts to test its correctness and performance. The algorithm is tested against its serial version and against the C++17 parallel `std::sort` (which, in the gcc implementation, also uses TBB in the backend). The implementation and performance analysis were subject of my 2019 Parallel Programming class project at the University of Novi Sad, Faculty of Technical Sciences.

## The algorithm

For a quick overview of the relevant algorithms (namely, [merging](https://en.wikipedia.org/wiki/Merge_algorithm) and [sorting](https://en.wikipedia.org/wiki/Merge_sort#Parallel_merge_sort)), take a look at their respective Wikipedia articles. For a more in-depth explanation, refer to [the documentation PDF in this repository](https://github.com/szmlad/short/blob/master/doc/documentation.pdf). The algorithm itself, both in its serial and parallel versions, is implemented in as generic a way as possible, basically having the same type requirements as `std::sort` (namely, it accepts two random access iterators for the range of elements to sort, and optionally a comparison function in the form of `(U const&, V const&) -> bool`, defaulting to `std::less<>`).

## Repository structure

- `doc` - documents relevant to the project.
    - `documentation.pdf` - documentation detailing the algorithm and its implementation, as well as results of performance testing on one particular machine. It is in Serbian, but the quantitative results should transcend the language barrier.
    - `spec.pdf` - contains the requirements of the original class project.
- `include` - header files.
    - `common` - some utility type aliases and functions, useful across implementations.
    - `serial` - serial implementation of the merge sort algorithm.
    - `parallel` - parallel implementation of the merge sort algorithm.
- `resources` - resources used during testing of the algorithms. Most of the files in this directory are to be generated by scripts.
    - `sizes.txt` - contains sizes of arrays for which performance is tested.
- `scripts` - scripts used for testing.
    - `analyze` - scripts for analyzing and plotting test results.
    - `generate` - scripts for generating array data for correctness and performance tests.
    - `test` - scripts for running tests for correctness and performance.
- `src` - source code of the main, runnable program. The program itself simply calls the appropriate algorithm and prints time elapsed based on commandline arguments.

## Running

A makefile is provided to simplify running the project. Run `make` to generate test cases, perform the tests and plot the results. For a full list of build commands, consult the makefile itself.
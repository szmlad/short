#include <algorithm>
#include <chrono>
#include <execution>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "common/iter.hpp"
#include "parallel/sort.hpp"
#include "parallel/merge.hpp"
#include "serial/sort.hpp"
#include "serial/merge.hpp"

constexpr auto MEASUREMENTS = 10;

template <typename T>
auto from_file(std::string filename) -> std::vector<T> {
    auto f     = std::ifstream{std::move(filename)};
    auto begin = std::istream_iterator<T>{f};
    auto end   = std::istream_iterator<T>{};
    return std::vector<T>{begin, end};
}

template <typename F>
auto timeit(F&& f) -> long long {
    namespace chrono = std::chrono;
    auto const start = chrono::steady_clock::now();
    f();
    auto const end = chrono::steady_clock::now();
    return chrono::duration_cast<chrono::microseconds>(end - start).count();
}

template <typename F>
void test(std::vector<int> xs, std::vector<int> const& ref, F&& func) {
    func(xs);
    std::cout << (xs == ref ? "correct" : "incorrect") << '\n';
}

template <typename SF, typename PF>
void correctness(std::string ser_msg, SF&& ser_fn, 
                 std::string par_msg, PF&& par_fn, 
                 int argc, char *argv[]) {
    auto xs  = from_file<int>(argv[2]);
    auto ref = from_file<int>(argv[3]);
    std::cout << ser_msg;
    test(xs, ref, ser_fn);
    std::cout << par_msg;
    test(xs, ref, par_fn);
}

template <typename SF, typename PF, typename STLF, typename T>
void performance(SF&& ser_fn, PF&& par_fn, STLF&& stl_fn, std::vector<T>& xs) {
    for (auto m = 0; m < MEASUREMENTS; ++m)
        std::cout << xs.size()
            << "\t\t" << timeit([xs, ser_fn]() mutable { ser_fn(xs); }) 
            << "\t\t" << timeit([xs, par_fn]() mutable { par_fn(xs); }) 
            << "\t\t" << timeit([xs, stl_fn]() mutable { stl_fn(xs); }) << '\n';
}

template <typename Fn, typename T>
void cutoff(Fn&& f, size_t& co, std::vector<T>& xs) {
    for (auto cutoff = size_t{2}; cutoff < xs.size(); cutoff *= 2) {
        co = cutoff;
        for (auto m = 0; m < MEASUREMENTS; ++m)
            std::cout << cutoff << "\t\t" << timeit([xs, f]() mutable { f(xs); }) << '\n';
    }
}

void merge_correctness(int argc, char *argv[]) {
    using namespace common;
    correctness(
        "Serial merge: ",
        [](std::vector<int>& v) { serial::merge(first(v), mid(v), last(v)); },
        "Parallel merge: ",
        [](std::vector<int>& v) { parallel::merge(first(v), mid(v), last(v)); },
        argc, argv
    );
}

void merge_performance(int argc, char *argv[]) {
    using namespace common;
    auto xs = from_file<int>(argv[2]);
    performance(
        [](std::vector<int>& xs) { serial::merge(first(xs), mid(xs), last(xs)); },
        [](std::vector<int>& xs) { parallel::merge(first(xs), mid(xs), last(xs)); },
        [](std::vector<int>& xs) { std::inplace_merge(std::execution::par, first(xs), mid(xs), last(xs)); },
        xs
    );
}

void sort_correctness(int argc, char *argv[]) {
    using namespace common;
    correctness(
        "Serial sort: ",
        [](std::vector<int>& v) { serial::sort(first(v), last(v)); },
        "Parallel sort: ",
        [](std::vector<int>& v) { parallel::sort(first(v), last(v)); },
        argc, argv
    );
}

void sort_performance(int argc, char *argv[]) {
    using namespace common;
    auto xs = from_file<int>(argv[2]);
    performance(
        [](std::vector<int>& xs) { serial::sort(first(xs), last(xs)); },
        [](std::vector<int>& xs) { parallel::sort(first(xs), last(xs)); },
        [](std::vector<int>& xs) { std::stable_sort(std::execution::par, first(xs), last(xs)); },
        xs
    );
}

void show_merge(int argc, char *argv[]) {
    if (argc == 4) merge_correctness(argc, argv);
    else merge_performance(argc, argv);
}

void show_sort(int argc, char *argv[]) {
    if (argc == 4) sort_correctness(argc, argv);
    else sort_performance(argc, argv);
}

void merge_cutoff(int argc, char *argv[]) {
    using namespace common;
    auto xs = from_file<int>(argv[2]);
    cutoff(
        [](std::vector<int>& xs) { parallel::merge(first(xs), mid(xs), last(xs)); },
        parallel::merge_cutoff,
        xs
    );
}

void sort_cutoff(int argc, char *argv[]) {
    using namespace common;
    auto xs = from_file<int>(argv[2]);
    cutoff(
        [](std::vector<int>& xs) { parallel::sort(first(xs), last(xs)); },
        parallel::sort_cutoff,
        xs
    );
}

int main(int argc, char *argv[]) {
    using namespace std::string_literals;
    const auto opts = std::map<std::string, std::function<void()>>{
        {"m"s,   [argc, argv] { show_merge(argc, argv);   }},
        {"s"s,   [argc, argv] { show_sort(argc, argv);    }},
        {"mc"s,  [argc, argv] { merge_cutoff(argc, argv); }},
        {"sc"s,  [argc, argv] { sort_cutoff(argc, argv);  }}
    };
    
    if (argc < 3 || argc > 4)
        return 1;
    else
        opts.at(argv[1])();
}
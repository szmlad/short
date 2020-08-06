#ifndef SHORT_SERIAL_MERGE_HPP_
#define SHORT_SERIAL_MERGE_HPP_

#include <functional>

#include "common/iter.hpp"

namespace serial {
    template <typename It, typename Out, typename P = std::less<>>
    void merge_impl(It lf, It ll, It rf, It rl, Out of, P&& p) {
        while (lf != ll && rf != rl)
            if (!p(*rf, *lf))
                *of++ = std::move(*lf++);
            else
                *of++ = std::move(*rf++);
        of = std::move(lf, ll, of);
        std::move(rf, rl, of);
    }

    template <typename It, typename P = std::less<>>
    void merge(It first, It mid, It last, P&& p = {}) {
        auto const size = static_cast<size_t>(last - first);
        auto alloc = std::allocator<common::value_t<It>>{};
        auto *into = alloc.allocate(size); 
        merge_impl(first, mid, mid, last, into, p);
        std::move(into, into + size, first);
        alloc.deallocate(into, size);
    }
}

#endif // SHORT_SERIAL_MERGE_HPP_
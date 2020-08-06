#ifndef SHORT_SERIAL_SORT_HPP_
#define SHORT_SERIAL_SORT_HPP_

#include <functional>

#include "merge.hpp"

namespace serial {
    template <typename It, typename P = std::less<>>
    void sort(It first, It last, P&& p = {}) {
        auto const size = static_cast<size_t>(last - first);
        if (size < 2)
            return;

        auto const mid = first + size/2;
        serial::sort(first, mid, p);
        serial::sort(mid, last, p);
        serial::merge(first, mid, last, p);
    }
}

#endif // SHORT_SERIAL_SORT_HPP_
#ifndef SHORT_PARALLEL_SORT_HPP_
#define SHORT_PARALLEL_SORT_HPP_

#include <functional>

#include <tbb/task.h>

#include "serial/sort.hpp"
#include "merge.hpp"

namespace parallel {
    auto sort_cutoff = size_t{2048u};

    template <typename It, typename P>
    class sort_impl : public tbb::task {
    private:
        It first, last;
        P p;

        struct sort_continuation : tbb::task {
            It first, mid, last;
            P p;

            sort_continuation(It f, It m, It l, P p)
                : first(std::move(f))
                , mid(std::move(m))
                , last(std::move(l))
                , p(std::move(p)) { }

            auto execute() -> tbb::task* {
                parallel::merge(first, mid, last, p);
                return nullptr;
            }
        };
    public:
        sort_impl(It f, It l, P p)
            : first(std::move(f)), last(std::move(l)), p(std::move(p)) { }

        auto execute() -> tbb::task* {
            auto const size = static_cast<size_t>(last - first);
            if (size <= sort_cutoff) {
                serial::sort(first, last, p);
                return nullptr;
            }

            auto const mid = first + size/2;

            auto& c = *new (allocate_continuation()) sort_continuation{
                first, mid, last, p
            };
            c.set_ref_count(2);

            auto& left = *new (c.allocate_child()) sort_impl{first, mid, p};
            spawn(left);

            recycle_as_child_of(c);
            first = mid;
            return this;
        }
    };

    template <typename It, typename P = std::less<>>
    void sort(It first, It last, P&& p = {}) {
        if (last - first <= sort_cutoff) {
            serial::sort(first, last, p);
            return;
        }
        
        auto& task = *new (tbb::task::allocate_root()) sort_impl{
            first, last, p
        };
        tbb::task::spawn_root_and_wait(task);
    }
}

#endif // SHORT_PARALLEL_SORT_HPP_
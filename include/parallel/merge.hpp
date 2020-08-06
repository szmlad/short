#ifndef SHORT_PARALLEL_MERGE_HPP_
#define SHORT_PARALLEL_MERGE_HPP_

#include <functional>
#include <vector>

#include <tbb/parallel_for.h>
#include <tbb/task.h>

#include "common/iter.hpp"
#include "serial/merge.hpp"

namespace parallel {
    auto merge_cutoff = size_t{2048u};

    template <typename It, typename Out, typename P>
    class merge_impl : public tbb::task {
    private:
        It l_first, l_last;
        It r_first, r_last;
        Out o_first;
        P p;

        struct merge_continuation : tbb::empty_task { };
    public:
        merge_impl(It lf, It ll, It rf, It rl, Out of, P p)
            : l_first(std::move(lf))
            , l_last(std::move(ll))
            , r_first(std::move(rf))
            , r_last(std::move(rl))
            , o_first(std::move(of))
            , p(std::move(p)) { }

        auto execute() -> tbb::task* {
            auto l_size = static_cast<size_t>(l_last - l_first);
            auto r_size = static_cast<size_t>(r_last - r_first);

            if (l_size < r_size) {
                std::swap(l_first, r_first);
                std::swap(l_last, r_last);
                std::swap(l_size, r_size);
            }

            if (l_size == 0)
                return nullptr;

            if (l_size + r_size <= merge_cutoff) {
                serial::merge_impl(
                    l_first, l_last, 
                    r_first, r_last, 
                    o_first, 
                    p
                );
                return nullptr;
            }

            auto const midpt = l_first + l_size/2;
            auto const parpt = std::lower_bound(r_first, r_last, *midpt, p);
            auto const inspt = o_first + (midpt - l_first) + (parpt - r_first);
            *inspt = *midpt;

            auto& c = *new (allocate_continuation()) merge_continuation;
            c.set_ref_count(2);

            auto& right = *new (c.allocate_child()) merge_impl{
                midpt + 1, l_last,
                parpt, r_last,
                inspt + 1, 
                p 
            };
            spawn(right);

            recycle_as_child_of(c);
            l_last = midpt;
            r_last = parpt;

            return this;
        }
    };

    template <typename It, typename P = std::less<>>
    void merge(It first, It mid, It last, P&& p = {}) {
        auto const size = static_cast<size_t>(last - first);

        if (size <= merge_cutoff) {
            serial::merge(first, mid, last, p);
            return;
        }

        auto alloc = std::allocator<common::value_t<It>>{};
        auto *into = alloc.allocate(size);
        auto& task = *new (tbb::task::allocate_root()) merge_impl{
            first, mid,
            mid, last,
            into, 
            p
        };
        tbb::task::spawn_root_and_wait(task);

        tbb::parallel_for(
            tbb::blocked_range<size_t>{0, size},
            [&] (tbb::blocked_range<size_t> const& range) {
                for (auto i = range.begin(); i != range.end(); ++i) {
                    auto pos = first + i;
                    *pos = std::move(into[i]);
                }
            }
        );
        alloc.deallocate(into, size);
    }
}

#endif // SHORT_PARALLEL_MERGE_HPP_
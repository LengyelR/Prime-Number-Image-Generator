from line_profiler import LineProfiler
from generate import cuda_shades10
import timeit
import numpy as np


def benchmark(f, *args, **kwargs):
    lp = LineProfiler()
    wrapper = lp(f)
    res = wrapper(*args, **kwargs)
    lp.print_stats()
    return res


def measure_cuda(grid, thread):
    mtx = np.random.randint(1, 250, size=(128, 128), dtype='int16')
    t = timeit.Timer(lambda: cuda_shades10[grid, thread](mtx.copy()))
    res = t.repeat(repeat=3, number=2000)
    return min(res)/2000


def measure_func(f):
    mtx = np.random.randint(1, 250, size=(128, 128), dtype='int16')
    t = timeit.Timer(lambda: f(mtx.copy()))
    res = t.repeat(repeat=3, number=2000)
    return min(res)/2000


def bw_round(px):
    d = int((px / 255.0) * 10)
    if d > 9:
        return 9
    if d < 0:
        return 0
    return d


if __name__ == "__main__":
    # from generate import get_candidates
    # benchmark(get_candidates, r'pic_128.jpg')

    quantize = np.vectorize(bw_round, otypes=[np.int16])
    print('vectorised', measure_func(quantize))
    print('32', measure_cuda((32, 32), (4, 4)))

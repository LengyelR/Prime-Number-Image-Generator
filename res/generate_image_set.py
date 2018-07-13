import numpy as np
from PIL import Image
import tqdm
from numba import cuda, int16


IMG_PATH = r'pic_128.jpg'
OUTPUT_PATH = r'prime_candidates.txt'
# ubiquity of primes: ln(10) ~ 2.3
# only generating odd numbers, this is more than enough
LIMIT = int(128 * 128 * 2.3)


@cuda.jit(argtypes=[int16[:, :]], target='gpu')
def _bw(image):
    x, y = cuda.grid(2)
    image[x, y] = int(image[x, y] / 25.5) if image[x, y] < 255 else 9


def bw_cuda(mtx):
    return _bw[(4, 4), (32, 32)](mtx)


def get_candidates():
    img = Image.open(IMG_PATH)
    seen_before = set()
    to_string = [str(i) for i in range(10)]
    to_int = {str(i): i for i in range(10)}

    for _ in tqdm.trange(LIMIT):
        while True:
            bw_img = img.convert('L')
            bw_mtx = np.array(bw_img, dtype='int16')
            bw_mtx += np.random.randint(0, 3, size=(128, 128), dtype='int16')

            bw_cuda(bw_mtx)
            digits = bw_mtx.flatten()
            num = "".join(to_string[d] for d in digits)

            n = to_int[num[-1]]
            if n % 2 == 0:
                n = n + 1 if np.random.rand() > 0.5 else n - 1
            num = num[:-1] + to_string[n]

            if len(num) == 128*128 and num not in seen_before:
                seen_before.add(num)
                break

    return seen_before


if __name__ == "__main__":
    candidates = get_candidates()
    with open(OUTPUT_PATH, 'w') as f:
        f.writelines((str(num) + '\n' for num in candidates))

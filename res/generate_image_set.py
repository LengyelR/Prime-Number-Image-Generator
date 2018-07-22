import numpy as np
from PIL import Image
import tqdm
from numba import cuda, int16


IMG_PATH = r'pic_128.jpg'
OUTPUT_PATH = r'prime_candidates.bin'
# ubiquity of primes: ln(10) ~ 2.3
# only generating odd numbers, this is more than enough
LIMIT = int(128 * 128 * 2.3)


@cuda.jit(argtypes=[int16[:, :]], target='gpu')
def _bw(image):
    x, y = cuda.grid(2)
    image[x, y] = int(image[x, y] / 25.5) if image[x, y] < 255 else 9


def bw_cuda(mtx):
    return _bw[(16, 16), (8, 8)](mtx)


def get_candidates():
    img = Image.open(IMG_PATH)
    seen_before = set()

    for _ in tqdm.trange(LIMIT):
        while True:
            bw_img = img.convert('L')
            bw_mtx = np.array(bw_img, dtype='int16')
            bw_mtx += np.random.randint(0, 3, size=(128, 128), dtype='int8')

            bw_cuda(bw_mtx)
            digits = bw_mtx.flatten()

            n = digits[-1]
            if n % 2 == 0:
                n = n + 1 if np.random.rand() > 0.5 else n - 1
                digits[-1] = n

            candidate = digits.tobytes()

            if len(candidate) == 128*128*2 and candidate not in seen_before:
                seen_before.add(candidate)
                break

    return seen_before


if __name__ == "__main__":
    candidates = get_candidates()
    with open(OUTPUT_PATH, 'wb') as f:
        f.writelines((num[::2] + b'\x0A' for num in candidates))

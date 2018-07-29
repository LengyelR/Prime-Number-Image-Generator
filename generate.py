import numpy as np
from PIL import Image
import tqdm
from numba import cuda, int16

OUTPUT_PATH = r'prime_candidates.bin'


@cuda.jit(argtypes=[int16[:, :]], target='gpu')
def cuda_shades10(image):
    x, y = cuda.grid(2)
    image[x, y] = int(image[x, y] / 25.5) if image[x, y] < 255 else 9


def bw_shades10(mtx):
    return cuda_shades10[(16, 16), (8, 8)](mtx)


def get_candidates(img_path):
    img = Image.open(img_path)
    h = img.height
    w = img.width

    assert h == w and h < 256
    limit = int(h * w * 2.3)  # ubiquity of primes: ln(10) ~ 2.3

    seen_before = set()

    for _ in tqdm.trange(limit):
        while True:
            bw_img = img.convert('L')
            bw_mtx = np.array(bw_img, dtype='int16')
            bw_mtx += np.random.randint(0, 3, size=(h, w), dtype='int8')

            bw_shades10(bw_mtx)
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
    import sys
    use_compression = int(sys.argv[1])


    def compress(num_bytes):
        num_bytes = iter(num_bytes[::2])
        return bytes((b1 * 10 + b2 for b1, b2 in zip(num_bytes, num_bytes)))

    candidates = get_candidates(r'pic_128.jpg')

    if use_compression:
        with open('compressed_' + OUTPUT_PATH, 'wb') as f:
            f.writelines((compress(num) + b'\x0A' for num in candidates))
    else:
        with open(OUTPUT_PATH, 'wb') as f:
            f.writelines((num[::2] + b'\x0A' for num in candidates))

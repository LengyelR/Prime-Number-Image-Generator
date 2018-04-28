import numpy as np
from PIL import Image
import time
import tqdm

IMG_PATH = r'pic_128.jpg'
OUTPUT_PATH = r'prime_candidates.txt'
# ubiquity of primes: ln(10) ~ 2.3
# only generating odd numbers, this is more than enough
LIMIT = int(128 * 128 * 2.3)  


def odd_round(s):
    n = int(s[-1])
    if n % 2 == 0:
        n = n+1 if np.random.rand() > 0.5 else n-1
    return s[:-1] + str(n)


def bw_round(px):
    d = int((px / 255.0) * 10)
    if d > 9:
        return 9
    if d < 0:
        return 0
    return d


img = Image.open(IMG_PATH)
seen_before = set()
quantize = np.vectorize(bw_round, otypes=[np.uint8])

started = time.time()
for _ in tqdm.trange(LIMIT):
    while True:
        bw_img = img.convert('L')
        bw_mtx = np.array(bw_img, dtype='int16')
        bw_mtx += np.random.randint(-2, 3, size=(128, 128), dtype='int16')

        bw_mtx = quantize(bw_mtx)
        digits = bw_mtx.flatten()

        num = odd_round("".join(str(d) for d in digits))
        num = num if len(num) == 128*128 else num[1:]

        if len(num) == 128*128 and num not in seen_before:
            seen_before.add(num)
            break

finished = time.time()
print('generation took', (finished - started) / 60, 'minutes')

with open(OUTPUT_PATH, 'w') as f:
    f.writelines((str(num) + '\n' for num in seen_before))
write_end = time.time()
print('writing took:', (write_end - finished) / 60, 'minutes')

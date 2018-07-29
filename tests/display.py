import numpy as np
from generate import OUTPUT_PATH
from matplotlib import pyplot as plt


def show_image_from_buffer(np_bytes):
    array = np.frombuffer(np_bytes, dtype='uint8')
    array = array.reshape((128, 128))

    plt.imshow(array)
    plt.show()


if __name__ == "__main__":
    import os
    with open(os.path.join('..', OUTPUT_PATH), 'rb') as f:
        lines = f.readlines()

    show_image_from_buffer(lines[0][:-1])

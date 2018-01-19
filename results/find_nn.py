import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import glob

path_celebA = '/home/jester/data/dcgan/data/celebA/*.jpg'
path_runs = '/home/jester/Documents/dcgan_runs/**/test/train_00_0000.png'


def from_path_to_image(paths, resize=False):
    print('start to read in images')
    paths = paths[:100]
    img_celebA = []
    for cel in paths:
        t = Image.open(cel)
        if resize:
            t = t.resize((88, 108))
            t = t.crop((88/2 - 32, 108/2 - 32, 88/2 + 32, 108/2 + 32))
        img_celebA.append(t)

    print len(img_celebA)
    return img_celebA


if __name__ == '__main__':
    celebA_paths = glob.glob(path_celebA)
    img_celebA = from_path_to_image(celebA_paths, resize=True)

    run_paths = glob.glob(path_runs)
    img_runs = from_path_to_image(run_paths)

    min_dist = 1000000
    min_imag = None

    for i, run in enumerate(img_runs):
        min_dist = 1000000
        min_imag = None
        for i_c in img_celebA:
            next_min_dist = np.sqrt(np.sum(np.subtract(run, i_c)**2))
            if min_dist >= next_min_dist:
                # print('next min dist: ', next_min_dist)
                min_dist = next_min_dist
                min_imag = i_c

        print(run_paths[i])
        plt.imsave(str(i) + 'min_imag.png ', min_imag)
        plt.imsave(str(i) + 'run.png ', run)
        print('smallest distance: ', min_dist)

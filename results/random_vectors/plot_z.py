import numpy as np
import matplotlib.pyplot as plt

f1 = plt.figure(1)
unif = np.random.uniform(-1, 1, size=(64,100))
plt.title('Uniform Distribution - Vector Z')

plt.imshow(unif)
plt.colorbar()
plt.savefig('uniform.png')

f2 = plt.figure(2)
mu, sigma = 0, 0.2
sample_z = np.random.normal(mu, sigma, size=(64,100))
plt.title('Normal Distribution - Vector Z (mu=0, sigma=0.2)')

plt.imshow(sample_z)
plt.colorbar()
plt.savefig('normal.png')

f1 = plt.figure(3)
unif = np.random.uniform(-100, 100, size=(64,100))
plt.title('Uniform Distribution - Vector Z')

plt.imshow(unif)
plt.colorbar()
plt.savefig('uniform100.png')

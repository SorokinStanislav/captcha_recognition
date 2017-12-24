import PIL
import imutils
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as misc
import cv2

# turn a letter using eigenvectors
FILE_NAME = 'roi-1.png'

img = misc.imread(FILE_NAME, flatten=True)
new_img = np.zeros([img.shape[0], img.shape[1]])
y, x = np.nonzero(img)

x = x - np.mean(x)
y = y - np.mean(y)
coords = np.vstack([x, y])

cov = np.cov(coords)
evals, evecs = np.linalg.eig(cov)

sort_indices = np.argsort(evals)[::-1]
evec1, evec2 = evecs[:, sort_indices]
x_v1, y_v1 = evec1  # Eigenvector with largest eigenvalue
x_v2, y_v2 = evec2


plt.axis('equal')
plt.gca().invert_yaxis()  # Match the image system with origin at top left


theta = np.tanh((x_v1)/(y_v1))


rotation_mat = np.matrix([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
transformed_mat = rotation_mat * coords
# plot the transformed blob
x_transformed, y_transformed = transformed_mat.A

plt.plot(x_transformed, y_transformed, 'ks', markersize=10)
plt.savefig('test.png')


scale_index_x = round(max(x_transformed) - min(x_transformed), 0) / img.shape[1]
scale_index_y = round(max(y_transformed) - min(y_transformed), 0) / img.shape[0]

norm_x = []
norm_y = []
for x in x_transformed:
    norm_x.append(int(round(x * scale_index_x, 0)))
for y in y_transformed:
    norm_y.append(int(round(y * scale_index_y, 0)))

for x in norm_x:
    for y in norm_y:
        new_img[y][x] = 255

cv2.imwrite("new.png", new_img)

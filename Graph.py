# from pylab import *
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.cbook import get_sample_data
# from matplotlib.png import read_png
# fn = get_sample_data("./Client/AV45/OAS30001_AV45_d2430_p0_t.jpg", asfileobj=False)
# img = read_png(fn)
# x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
# ax = gca(projection='3d')
# ax.plot_surface(x, y, 10, rstride=5, cstride=5, facecolors=img)
# show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import cv2

# #read image
# img = cv2.imread("./Client/AV45/OAS30001_AV45_d2430_p0_t.jpg")

# #convert from BGR to RGB
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# #get rgb values from image to 1D array
# r, g, b = cv2.split(img)
# r = r.flatten()
# g = g.flatten()
# b = b.flatten()

# #plotting 
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter(r, g, b)
# plt.show()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread("./Client/AV45/OAS30001_AV45_d2430_p0_t.jpg")
# plt.imshow(img)
# plt.show()

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
ax = gca(projection='3d')
ax.plot_surface(x, y, 10, rstride=5, cstride=5, facecolors=img)
show()
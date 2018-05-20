import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def histeq(image_array, image_bins=256):
    # 将图像矩阵转化成直方图数据，返回元组(频数，直方图区间坐标)
    image_array2, bins = np.histogram(image_array.flatten(), image_bins)

    # 计算直方图的累积函数
    cdf = image_array2.cumsum()

    # 将累积函数转化到区间[0,255]
    cdf = (255.0 / cdf[-1]) * cdf

    # 原图像矩阵利用累积函数进行转化，插值过程
    image2_array = np.interp(image_array.flatten(), bins[:-1], cdf)

    # 返回均衡化后的图像矩阵和累积函数
    return image2_array.reshape(image_array.shape), cdf


image = Image.open("/Users/diamond/PycharmProjects/bishe/test/大地保险/jcaptcha.jpeg")
image_array = np.array(image)
plt.subplot(2, 2, 1)
plt.hist(image_array.flatten(), 256)
plt.subplot(2, 2, 2)
plt.imshow(image, cmap=cm.gray)
plt.axis("off")

a = histeq(image_array)  # 利用刚定义的直方图均衡化函数对图像进行均衡化处理
plt.subplot(2, 2, 3)
plt.hist(a[0].flatten(), 256)
plt.subplot(2, 2, 4)
plt.imshow(Image.fromarray(a[0]), cmap=cm.gray)
plt.axis("off")

plt.show()
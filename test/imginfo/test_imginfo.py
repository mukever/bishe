


#get img info
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.cm as cm

#打开图像
image = Image.open("/Users/diamond/PycharmProjects/bishe/test/大地保险/jcaptcha.jpeg")
image_array = np.array(image)

plt.subplot(2,1,1)
plt.imshow(image)
plt.axis("off")
plt.subplot(2,1,2)
plt.hist(image_array.flatten(),256) #flatten可以将矩阵转化成一维序列
plt.savefig('filename.png')
plt.show()
import matplotlib.pyplot as plt

#打开图像，并转化成灰度图像
image = Image.open("/Users/diamond/PycharmProjects/bishe/test/大地保险/jcaptcha.jpeg").convert("L")
image_array = np.array(image)

plt.subplot(2,1,1)
plt.imshow(image,cmap=cm.gray)
plt.axis("off")
plt.subplot(2,1,2)
plt.hist(image_array.flatten(),256) #flatten可以将矩阵转化成一维序列
plt.show()
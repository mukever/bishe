import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

image = Image.open("/Users/diamond/PycharmProjects/bishe/test/大地保险/jcaptcha.jpeg")
image_array = np.array(image)

x = np.arange(255)

# 反相
plt.subplot(3,2,1)
plt.plot(x,255-x) # 画出变换函数图像
plt.subplot(3,2,2)
plt.imshow(Image.fromarray(255-image_array),cmap=cm.gray)
plt.axis("off")

# # 转换到 100-200
# plt.subplot(3,2,3)
# plt.plot(x,(x/255.0)*100+100) # 画出变换函数图像
# plt.subplot(3,2,4)
# plt.imshow( Image.fromarray((image_array/255.0)*100+100), cmap=cm.gray )
# plt.axis("off")
#
# # 像素平方
# plt.subplot(3,2,5)
# plt.plot(x,255*(x/255.0)**2) # 画出变换函数图像
# plt.subplot(3,2,6)
# plt.imshow( Image.fromarray(255*(image_array/255.0)**2), cmap=cm.gray )
# plt.axis("off")

plt.show()
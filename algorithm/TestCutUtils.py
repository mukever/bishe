import cv2

from algorithm.CutUtils import *
from algorithm.Clean import Clean

if __name__ == '__main__':
    img_path = "/Users/diamond/PycharmProjects/bishe/test/大地保险/train/"

    picname = '2*6__.jpg'
    # read img
    cv2_img = cv2.imread(img_path + picname)
    clean = Clean(cv2_img)
    clean.deleteblackByRGB()
    clean.addImage()
    cv2_img = clean.binaryzation(power=1.0)

    cututils = CutUtils(cv2_img,5,picname,3)
    cututils.cut()
    cututils.save()
    print(len(cututils.dataofnumber))
    print(cututils.labelofnumber)

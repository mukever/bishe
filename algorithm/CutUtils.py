import cv2


class CutUtils():

    def __init__(self,cv2_img,charnumber,labelstring,neednumber):

        self.cv2_img = cv2_img
        self.charnumber = charnumber
        self.labelstring = labelstring
        self.neednumber  =neednumber
        self.dataofnumber = []
        self.labelofnumber = []
        self.im_list = []

        self.h = self.cv2_img.shape[0]
        self.w = self.cv2_img.shape[1]

        self.onepart = int(self.w /self.charnumber)


    def cut(self):

        #cut to list

        for i in range(self.charnumber):
            im = self.cv2_img[0:self.h, i * self.onepart:(i + 1) * self.onepart]
            self.im_list.append(im)

        for k in range(self.neednumber):
            im_i = self.im_list[k]
            imh = im_i.shape[0]
            imw = im_i.shape[1]
            # t.printcv2(im_i)
            tmp_data = [0 for i in range(imh * imw)]
            for i in range(imh):
                for j in range(imw):
                    # print im_i
                    if im_i[i, j] != 0:
                        tmp_data[i * j + j] = 1

            self.dataofnumber.append(tmp_data)
            if self.labelstring != "":
                self.labelofnumber.append(self.labelstring[k])
    def save(self):
        self.savepath=[]

        for i in range(len(self.im_list)):
            picname =str(i)+".jpg"
            cv2.imwrite(picname, self.im_list[i])
            self.savepath.append(picname)
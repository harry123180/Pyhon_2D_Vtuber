import cv2
import numpy as np
img1 = cv2.imread('background.png')
img2 = cv2.imread('fig_2//open_mouth.png')
    #引入两个图片，第二个是logo
r1,c1,ch1 = img1.shape
r2,c2,ch2 = img2.shape
tar_x,tar_y = 1000,0
#roi = img1[r1+tar_x:r1+r2+tar_x, c1 +tar_y:c1+c2+tar_y]
roi = img1[0+tar_y:r2+tar_y, 0+tar_x:c2+tar_x]
    #设定jiemi图的roi，注意：对roi的操作就是对img1的操作
gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    #得到灰度图
ret, ma1 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
fg1 = cv2.bitwise_and(roi,roi,mask=ma1)
    #ma1是黑化logo，黑的地方可以通过bitwise_and把其他黑掉，所以ma1是黑roi的
ret, ma2 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
fg2 = cv2.bitwise_and(img2,img2,mask = ma2)
    #ma2是黑化周边，所以ma2是黑logo的
    #ma2=cv2.bitwise_not(ma1) 也可以这样对其反转
roi[:] = cv2.add(fg1, fg2)
    #这里终于合体了

cv2.namedWindow("Image2", 0)
cv2.resizeWindow("Image2", 700, 600)
cv2.imshow("Image2",img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
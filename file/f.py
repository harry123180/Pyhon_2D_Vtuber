import numpy as np
import cv2
class object:
    # 建構式
    def __init__(self, image):
        self.image = image  # 顏色屬性
        self.x,self.y,self.a = image.shape
        self.half_x,self.half_y = int(self.x/2),int(self.y/2)
        self.px_array = [[],[]]
        self.mask =np.zeros([self.x,self.y],dtype=np.uint8)
        for i in range(self.x):
            for j in range(self.y):
                if (self.image[i][j][0] == 255 and self.image[i][j][1] == 255 and self.image[i][j][2] == 255):
                    # 都是背景 沿用
                    self.mask[i][j] = 0
                    pass
                else:
                    self.mask[i][j]=1
                    self.px_array[0].append(i)
                    self.px_array[1].append(j)
        #self.px_array = np.array(self.px_array)
        #print(self.px_array.shape)

        self.indx_len = len(self.px_array[0])#不是透明的像素總數
        self.y_len =min(self.px_array[1])
        self.x_len = min(self.px_array[0])
class background:
    def __init__(self,back):
        self.back = back
def putOBJ(background,logo_obj,tar_x,tar_y):
    cnt = 0
    #print("chaeck f type",type(background),type(logo_obj.image))
    q,w,e = background.shape
    for i in range(logo_obj.indx_len):
        cnt+=1
        bg_x = logo_obj.px_array[0][i]+tar_y-logo_obj.y_len#最後實際在背景上的x
        bg_y = logo_obj.px_array[1][i]+tar_x-logo_obj.x_len#最後實際在背景上的y
        if((bg_x>q and bg_x <0) or (bg_y>w and bg_y <0)):
            pass
        else:
            #print(background[logo_obj.px_array[0][i]+tar_y-logo_obj.y_len][logo_obj.px_array[1][i]+tar_x-logo_obj.x_len])
            background[logo_obj.px_array[0][i]+tar_y-logo_obj.y_len][logo_obj.px_array[1][i]+tar_x-logo_obj.x_len] =\
                logo_obj.image[logo_obj.px_array[0][i]][logo_obj.px_array[1][i]]
            #print((logo_obj.px_array[0][i] + tar_y - logo_obj.y_len),(logo_obj.px_array[1][i] + tar_x - logo_obj.x_len),logo_obj.image[logo_obj.px_array[0][i]][logo_obj.px_array[1][i]])
    #print(cnt,bg_x,bg_y,"             ",(bg_x>q and bg_x <0),"   ",(bg_y>w and bg_y <0),"       ",(bg_x>q and bg_x <0) or (bg_y>w and bg_y <0))
    return background
def d(p1,p2):
    a= pow(p2[0]-p1[0],2)
    b = pow(p2[1]-p1[1],2)
    return pow(a+b,0.5)
def return_right_eyes( ih, iw,frame):
    # 386 右上眼374右下眼 446右左 463 右右
    p1= (int(frame[386].x * iw), int(frame[386].y * ih))
    p2 =( int(frame[374].x * iw), int(frame[374].y * ih))
    p3 = (int(frame[446].x * iw), int(frame[446].y * ih))
    p4 = (int(frame[463].x * iw), int(frame[463].y * ih))
    #print(d(p1,p2)/d(p3,p4))
    if(d(p3, p4)!=0):
        val = int(d(p1, p2) / d(p3, p4) * 10)
        if (val >= 2):
            return 1
        else:
            return 0
    else:
        return 0
def return_left_eyes(ih,iw,frame):
    # 159左上眼 145左下眼 33,133
    p1 = (int(frame[159].x * iw), int(frame[159].y * ih))
    p2 = (int(frame[145].x * iw), int(frame[145].y * ih))
    p3 = (int(frame[33].x * iw), int(frame[33].y * ih))
    p4 = (int(frame[133].x * iw), int(frame[133].y * ih))
    #print(d(p1, p2) / d(p3, p4))
    if(d(p3, p4)!=0):
        val = int(d(p1, p2) / d(p3, p4) * 10)
        if (val >= 3):
            return 1
        else:
            return 0
    else:
        return 0
def return_mouth_state(ih,iw,frame):
    p1 = (int(frame[13].x * iw), int(frame[13].y * ih))
    p2 = (int(frame[15].x * iw), int(frame[15].y * ih))
    val = d(p1,p2)
    #print("VAl= " ,val)
    if (val <= 10):
        return 0
    else:
        return 1
def putOBJm(img1,img2,tar_x,tar_y):
    r2, c2, ch2 = img2.image.shape
    roi = img1[0+tar_y:r2+tar_y, 0+tar_x:c2+tar_x]
    gray = cv2.cvtColor(img2.image, cv2.COLOR_BGR2GRAY)
    ret, ma1 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
    fg1 = cv2.bitwise_and(roi, roi, mask=ma1)
    ret, ma2 = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
    fg2 = cv2.bitwise_and(img2.image, img2.image, mask=ma2)
    # ma2=cv2.bitwise_not(ma1) 也可以用Not對其反轉
    roi[:] = cv2.add(fg1, fg2)
    # mix
    return img1
def rotate(image, angle, center, scale = 1.0):
    if(center ==None):
        x, y, a = image.shape
    M = cv2.getRotationMatrix2D((y/2,x/2), angle, scale)
    rotated = cv2.warpAffine(image, M, (y,x))
    return rotated
K=1
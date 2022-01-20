import cv2
img_path  ="im1.png"
img2_path = "w.png"
image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
logo = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
#讀近來都是矩陣
#final = image
#複製一張矩陣當作最後矩陣
x_of_image,y_of_image,a_of_image = image.shape#取得原始圖尺寸
x,y,a = logo.shape#取得物件尺寸
x_of_moveable,y_of_moveable = x_of_image - x , y_of_image - y#x_of_moveable,y_of_moveable物件可移動的X跟Y範圍
x_move =0
y_move = 0
deg = 0
def rotate(image, angle, center, scale = 1.0):
    if(center ==None):
        x, y, a = image.shape
    M = cv2.getRotationMatrix2D((y/2,x/2), angle, scale)
    rotated = cv2.warpAffine(image, M, (y,x))
    return rotated
while True:
    final = image.copy()
    apply_logo =rotate(logo.copy(),deg,None,1)
    #ro = rotate(logo.copy(),deg,int(x/2+x_move),int(y/2+y_move),1)
    #cv2.imshow("ro",ro)
    for i in range(x):
        for j in range(y):
            if(apply_logo[i][j][0]==255 and apply_logo[i][j][1]==255 and apply_logo[i][j][2] ==255):
                #都是背景 沿用
                pass
            elif(apply_logo[i][j][0]==0 and apply_logo[i][j][1]==0 and apply_logo[i][j][2] ==0):
                pass
            else:
                final[i+x_move][j+y_move]=apply_logo[i][j]
    cv2.imshow("final",final)
    x_move += 4
    y_move += 2
    deg +=10
    if(x_move>x_of_moveable or y_move>y_of_moveable or cv2.waitKey(1) & 0xFF == ord('q')):
        break
    #cv2.waitKey(0)
#
cv2.destroyAllWindows()
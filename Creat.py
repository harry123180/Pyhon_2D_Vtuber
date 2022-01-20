import cv2
img_path  ="im1.png"
img2_path = "w.png"
image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
logo = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
#讀近來都是矩陣
final = image
#複製一張矩陣當作最後矩陣
x,y,a = logo.shape#取得物件尺寸
for i in range(x):
    for j in range(y):
        if(logo[i][j][0]==255 and logo[i][j][1]==255 and logo[i][j][2] ==255):
            #都是背景 沿用
            pass
        else:
            final[i][j]=logo[i][j]
cv2.imshow("final",final)

cv2.waitKey(0)
#
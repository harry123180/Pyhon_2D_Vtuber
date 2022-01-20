import cv2
import f


face_path = "face.png"
bg_path = "background.png"
open_eyes_path = "open eyes.png"
close_eyes_path = "close eyes.png"
mouth_path = "mouth.png"

face = cv2.imread(face_path, cv2.IMREAD_UNCHANGED)
open_eye = cv2.imread(open_eyes_path,cv2.IMREAD_UNCHANGED)
close_eye = cv2.imread(close_eyes_path,cv2.IMREAD_UNCHANGED)
mouth = cv2.imread(mouth_path,cv2.IMREAD_UNCHANGED)
background = cv2.imread(bg_path, cv2.IMREAD_UNCHANGED)

face_o = f.object(face)
open_eye_o = f.object(open_eye)
close_eye_o = f.object(close_eye)
mouth_o = f.object(mouth)
final = background.copy()
print(final.shape)
final = f.putOBJ(final,face_o,500,500)
cv2.namedWindow("Image2", 0)
cv2.resizeWindow("Image2", 700, 600)
cv2.imshow("Image2",final)
cv2.waitKey(0)
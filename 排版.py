import cv2
import f

face_path = "face.png"
bg_path = "background.png"
open_eyes_path = "open eyes.png"
close_eyes_path = "close eyes.png"
mouth_path = "mouth.png"
close_mouth_path = "close_mouth.png"
face = cv2.imread(face_path, cv2.IMREAD_UNCHANGED)
open_eye = cv2.imread(open_eyes_path, cv2.IMREAD_UNCHANGED)
close_eye = cv2.imread(close_eyes_path, cv2.IMREAD_UNCHANGED)
mouth = cv2.imread(mouth_path, cv2.IMREAD_UNCHANGED)
background = cv2.imread(bg_path, cv2.IMREAD_UNCHANGED)
close_mouth = cv2.imread(close_mouth_path, cv2.IMREAD_UNCHANGED)
print(background.shape)
face_o = f.object(face)
open_eye_o = f.object(open_eye)
close_eye_o = f.object(close_eye)
mouth_o = f.object(mouth)
close_mouth_o = f.object(close_mouth)
eye_list = [close_eye_o, open_eye_o]  # 眼清單
mouth_list = [close_mouth_o, mouth_o]  # 嘴清單

def process(X,Y,state):
    face_state,left_eye, right_eye, mouth_state = state[0],state[1],state[2],state[3]
    final = background.copy()
    if(face_state):
        final = f.putOBJ(final,face_o,X,Y)
        final = f.putOBJ(final,eye_list[left_eye],X+0,Y+40)
        final = f.putOBJ(final,eye_list[right_eye],X+240,Y+40)
        final = f.putOBJ(final,mouth_list[mouth_state],X+240,Y+140)
        return final
    else:
        return final
"""
img = process(0,0,[1,1,1,1])
cv2.namedWindow("Image2", 0)
cv2.resizeWindow("Image2", 700, 600)
cv2.imshow("Image2",img)
cv2.waitKey(0)
"""
"""
cv2.namedWindow("Image2", 0)
cv2.resizeWindow("Image2", 700, 600)
cv2.imshow("Image2",final)
cv2.waitKey(0)
"""
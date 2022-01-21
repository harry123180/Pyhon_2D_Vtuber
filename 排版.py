import cv2
import f
"""
face_path = "face.png"

open_eyes_path = "open eyes.png"
close_eyes_path = "close eyes.png"
mouth_path = "mouth.png"
close_mouth_path = "close_mouth.png"

face = cv2.imread(face_path, cv2.IMREAD_UNCHANGED)
open_eye = cv2.imread(open_eyes_path, cv2.IMREAD_UNCHANGED)
close_eye = cv2.imread(close_eyes_path, cv2.IMREAD_UNCHANGED)
mouth = cv2.imread(mouth_path, cv2.IMREAD_UNCHANGED)

close_mouth = cv2.imread(close_mouth_path, cv2.IMREAD_UNCHANGED)
#print(background.shape)
face_o = f.object(face)
open_eye_o = f.object(open_eye)
close_eye_o = f.object(close_eye)
mouth_o = f.object(mouth)
"""
bg_path = "background.png"
background = cv2.imread(bg_path, cv2.IMREAD_UNCHANGED)
##
open_mouth_path = "fig_2//open_mouth.png"
close_mouth_path="fig_2//close_mouth.png"
open_eyes_path="fig_2//open_eyes.png"
close_eyes_path="fig_2//close_eyes.png"
open_mouth = cv2.imread(open_mouth_path, cv2.IMREAD_UNCHANGED)
close_mouth=cv2.imread(close_mouth_path, cv2.IMREAD_UNCHANGED)
open_eyes = cv2.imread(open_eyes_path, cv2.IMREAD_UNCHANGED)
close_eyes=cv2.imread(close_eyes_path, cv2.IMREAD_UNCHANGED)
obj_list = [open_mouth,close_mouth,open_eyes,close_eyes]
obj_cood =[]
for i in range(len(obj_list)):
    obj_cood.append(obj_list[i].shape)
#print(obj_cood[0])
########
K=1
KX=1
KY=0
open_mouth = cv2.resize(open_mouth, (obj_cood[0][KX]*K, obj_cood[0][KY]*K), interpolation=cv2.INTER_AREA)
close_mouth=cv2.resize(close_mouth, (obj_cood[1][KX]*K, obj_cood[1][KY]*K), interpolation=cv2.INTER_AREA)
open_eyes = cv2.resize(open_eyes, (obj_cood[2][KX]*K, obj_cood[2][KY]*K), interpolation=cv2.INTER_AREA)
close_eyes=cv2.resize(close_eyes, (obj_cood[3][KX]*K, obj_cood[3][KY]*K), interpolation=cv2.INTER_AREA)
background=cv2.resize(background, (int(2976/4), int(2147/4)), interpolation=cv2.INTER_AREA)
########
open_mouth_o=f.object(open_mouth)
close_mouth_o=f.object(close_mouth)
open_eyes_o=f.object(open_eyes)
close_eyes_o=f.object(close_eyes)
close_mouth_o = f.object(close_mouth)
eye_list = [close_eyes_o, open_eyes_o]  # 眼清單
mouth_list = [close_mouth_o, open_mouth_o]  # 嘴清單
cod_mo=[[110,0],[100,20]]
cod_ey =[[-57,150],[-57,145]]
print(cod_ey[1][1])
def process(X,Y,state):
    face_state,left_eye, right_eye, mouth_state = state[0],state[1],state[2],state[3]
    final = background.copy()
    if(face_state):
        #final = mouth_list[face_state].copy()
        final = f.putOBJ(final,mouth_list[mouth_state],X+cod_mo[mouth_state][0],Y+cod_mo[mouth_state][1])
        final = f.putOBJ(final,eye_list[left_eye],X+255+cod_ey[left_eye][0],Y+cod_ey[left_eye][1]+int(0.5*cod_mo[mouth_state][1]))
        print(X+255+cod_mo[mouth_state][0],Y+cod_mo[mouth_state][1])
        #final = f.putOBJ(final,eye_list[right_eye],X+240,Y+40)
        #final = f.putOBJ(final,mouth_list[mouth_state],X+240,Y+140)
        return final
    else:
        return final
#face_state,left_eye, right_eye, mouth_state
"""
img = process(0,0,[1,0,1,1])
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
import cv2
import f
read_3h = cv2.IMREAD_COLOR
bg_path = "background.png"
background = cv2.imread(bg_path, read_3h)
##
open_mouth_path = "G://kinematic//fig_2//open_mouth.png"
close_mouth_path="G://kinematic//fig_2//close_mouth.png"
open_eyes_path="G://kinematic//fig_2//open_eyes.png"
close_eyes_path="G://kinematic//fig_2//close_eyes.png"
open_mouth = cv2.imread(open_mouth_path,read_3h)
close_mouth=cv2.imread(close_mouth_path, read_3h)
open_eyes = cv2.imread(open_eyes_path, read_3h)
close_eyes=cv2.imread(close_eyes_path,read_3h)
obj_list = [open_mouth,close_mouth,open_eyes,close_eyes]
obj_cood =[]
for i in range(len(obj_list)):
    obj_cood.append(obj_list[i].shape)
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
cod_mo=[[115,10],[100,20]] #[[閉嘴的圖x,閉嘴的圖y],[張嘴的圖x,張嘴的圖y]]
cod_ey =[[-57,160],[-57,155]] #[[閉眼的圖x,閉眼的圖y],[開眼的圖x,開眼的圖y]]

def process(X,Y,state):
    face_state,left_eye, right_eye, mouth_state = state[0],state[1],state[2],state[3]
    final =background.copy()
    if(face_state):
        final = f.putOBJm(final,mouth_list[mouth_state],X+cod_mo[mouth_state][0],Y+cod_mo[mouth_state][1])
        final = f.putOBJm(final,eye_list[left_eye],X+255+cod_ey[left_eye][0],Y+cod_ey[left_eye][1]+int(0.5*cod_mo[mouth_state][1]))
        return final
    else:
        return final
#face_state,left_eye, right_eye, mouth_state
"""
img = process(0,0,[1,1,1,1])
cv2.namedWindow("Image2", 0)
cv2.resizeWindow("Image2", 700, 600)
cv2.imshow("Image2",img)
cv2.waitKey(0)

"""
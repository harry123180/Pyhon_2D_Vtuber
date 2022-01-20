import cv2
import numpy as np
import mediapipe as mp
import f
img =cv2.imread("2.jpg", cv2.IMREAD_UNCHANGED)
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
b_channel, g_channel, r_channel = cv2.split(img)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)
alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
# 最小值爲0
alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100
K=1
img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
results = faceMesh.process(imgRGB)
if results.multi_face_landmarks:
    for faceLms in results.multi_face_landmarks:
        #mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                              #drawSpec,drawSpec)
        ih, iw, ic = img_BGRA.shape
        print(faceLms.landmark[463].x*iw,faceLms.landmark[463].y*ih)
        for id,lm in enumerate(faceLms.landmark):
            #print(lm)

            x,y = int(lm.x*iw), int(lm.y*ih)
            # 2,10頭
            # 159左上眼 145左下眼 33,133
            # 386 右上眼374右下眼 446右左 463 右右
            if(id ==13):
                cv2.circle(img, (x, y), 6, (0,0,0), 0)
                print(x,y)
                p1 = (x*K,y*K)
            elif(id==15):
                cv2.circle(img, (x, y), 6, (255, 0, 0), 0)
                p2 = (x*K,y*K)
            elif(id==51):
                cv2.circle(img, (x, y), 6, (0,255, 0), 0)
                p3 = (x*K,y*K)
            elif(id == 187):
                cv2.circle(img, (x, y), 6, (0, 0, 255), 0)
                p4 = (x*K,y*K)
        #print(f.d(p3,p4)/f.d(p1,p2),f.d(p1,p2),f.d(p3,p4))
        print(f.return_right_eyes(ih,iw,faceLms.landmark))
        print(f.return_left_eyes(ih, iw, faceLms.landmark))
        print(f.return_mouth_state(ih, iw, faceLms.landmark))

cv2.namedWindow("Image", 0)
cv2.resizeWindow("Image", 700, 600)
cv2.imshow("Image", img)
cv2.waitKey(0)

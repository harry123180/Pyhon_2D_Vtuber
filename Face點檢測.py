import cv2
import mediapipe as mp
import time
import math
import numpy as np
import f
#env = VE
cap = cv2.VideoCapture(1)
pTime = 0
img2_path = "w.png"
bg_path = "background.png"
logo = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
background = cv2.imread(bg_path, cv2.IMREAD_UNCHANGED)
bg_x,bg_y,bg_a = background.shape
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)
def rotate(image, angle, center, scale = 1.0):
    if(center ==None):
        x, y, a = image.shape
    M = cv2.getRotationMatrix2D((y/2,x/2), angle, scale)
    rotated = cv2.warpAffine(image, M, (y,x))
    return rotated
K=1
while True:
    success, img = cap.read()
    img = cv2.resize(img,(int(bg_y/K), int(bg_x/K)), interpolation=cv2.INTER_AREA)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    b_channel, g_channel, r_channel = cv2.split(img)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # 最小值爲0
    alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    results = faceMesh.process(imgRGB)
    final = background.copy()
    if results.multi_face_landmarks:
        deg = 0
        for faceLms in results.multi_face_landmarks:
            #mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                                  #drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                #print(lm)
                ih, iw, ic = img_BGRA.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                if(id ==2):
                    cv2.circle(final, (x, y), 60, (0,0,0), 0)
                    p1 = (x*K,y*K)
                elif(id==10):
                    cv2.circle(final, (x, y), 60, (0, 0, 0), 0)
                    p2 = (x*K,y*K)
                    cv2.line(final, p1, p2, (0, 0, 255), 5)
                    if(p2[0]-p1[0]!=0):
                        deg = math.degrees(math.atan((p1[1]-p2[1])/(p2[0]-p1[0])))
                        if(deg <0):
                            deg = 180+deg
                #print(id,x,y)
        apply_logo = rotate(logo.copy(), deg, None, 1)
        logo_obj = f.object(apply_logo)
        final = f.putOBJ(final,logo_obj,p1[0],p1[1])


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(final, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.namedWindow("Image", 0)
    cv2.resizeWindow("Image", 700, 600)
    cv2.namedWindow("Image2", 0)
    cv2.resizeWindow("Image2", 700, 600)
    cv2.imshow("Image", final)
    cv2.imshow("Image2",img_BGRA)
    cv2.waitKey(1)
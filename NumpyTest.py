import cv2
import mediapipe as mp
import time
import numpy as np
#env = VE
cap = cv2.VideoCapture(0)
pTime = 0
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
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    b_channel, g_channel, r_channel = cv2.split(img)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # 最小值爲0
    alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:

        for faceLms in results.multi_face_landmarks:
            #mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                                  #drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                #print(lm)
                ih, iw, ic = img_BGRA.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                if(id ==13):
                    cv2.circle(img, (x, y), 60, (0,0,0), 0)
                    p1 = (x*10,y*10)
                elif(id==14):
                    cv2.circle(img, (x, y), 60, (0, 0, 0), 0)
                    p2 = (x*10,y*10)
                    cv2.line(img, p1, p2, (0, 0, 255), 5)




    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.namedWindow("Image2", 0)
    cv2.resizeWindow("Image2", 700, 600)
    cv2.imshow("Image2",img)
    cv2.waitKey(1)
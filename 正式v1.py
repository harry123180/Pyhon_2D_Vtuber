import cv2
import mediapipe as mp
import time
import numpy as np
import f
import 排版 as pp
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
K=1
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # 最小值爲0
    alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    results = faceMesh.process(imgRGB)
    state = [0,0,0,0]
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            ih, iw, ic = img_BGRA.shape
    #face_state,left_eye, right_eye, mouth_state
            state = [1,f.return_left_eyes(ih, iw, faceLms.landmark),f.return_right_eyes(ih, iw, faceLms.landmark),f.return_mouth_state(ih, iw, faceLms.landmark)]
    #print(int(faceLms.landmark[21].x * 2147)-500,int( faceLms.landmark[21].y * 2976)-500)
        final = pp.process(0,0, state)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(final, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.namedWindow("Image", 0)
    cv2.resizeWindow("Image", 1000, 800)
    cv2.namedWindow("Image2", 0)
    cv2.resizeWindow("Image2", 700, 600)
    cv2.imshow("Image", final)
    cv2.imshow("Image2",img_BGRA)
    cv2.waitKey(1)
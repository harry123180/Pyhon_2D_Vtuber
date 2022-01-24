import cv2
import mediapipe as mp
import numpy as np
import f
import layout as pp
import os
#env = VE
cap = cv2.VideoCapture(0)
pTime = 0
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)
print("按Q結束程式")
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
            state = [1,f.return_left_eyes(ih, iw, faceLms.landmark),f.return_right_eyes(ih, iw, faceLms.landmark),f.return_mouth_state(ih, iw, faceLms.landmark)]
    final = pp.process(0,0, state)
    cv2.namedWindow("Image", 0)
    cv2.resizeWindow("Image", 1000, 800)
    cv2.namedWindow("webcam", 0)
    cv2.resizeWindow("webcam", 700, 600)
    cv2.imshow("Image", final)
    cv2.imshow("webcam",img_BGRA)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
os.system("pause")
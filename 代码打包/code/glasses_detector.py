import numpy as np
import dlib
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import statistics

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


def has_glasses(path):
    

    #plt.imshow(img)
    #plt.show()

    try:
        img = dlib.load_rgb_image(path)
        rect = detector(img)[0]
        sp = predictor(img, rect)
        landmarks = np.array([[p.x, p.y] for p in sp.parts()])
    except:
        #识别不到人脸
        return -1
    #print(landmarks)

    nose_bridge_x = []
    nose_bridge_y = []
    for i in [28,29,30,31,33,34,35]:
            nose_bridge_x.append(landmarks[i][0])
            nose_bridge_y.append(landmarks[i][1])
            
            
    ### x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)
    ### ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[20][1]
    y_max = landmarks[31][1]
    img2 = Image.open(path)

    img2 = img2.crop((x_min,y_min,x_max*0.99,y_max*0.95))

    #plt.imshow(img2)
    #plt.show()
    #高斯滤波
    img_blur = cv2.GaussianBlur(np.array(img2),(3,3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image =img_blur, threshold1=100, threshold2=200)
    #plt.imshow(edges, cmap =plt.get_cmap('gray'))
    #plt.show()
    #center strip
    #print(edges)
    edges_center = edges.T[(int(len(edges.T)/2))]
    #print(edges_center)

    if 255 in edges_center:
        return True
    else:
        return False

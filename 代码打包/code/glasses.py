import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import cv2
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
#初始化Mediapipe的FaceMesh模型
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
    
def has_glasses(image):
    # 加载图像
    #image = cv2.imread("1.PNG")
    #plt.imshow(image)
    #plt.show()
    
    # 检测人脸
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # 获取人脸关键点的位置
    landmarks = results.multi_face_landmarks[0].landmark
    points = []
    for landmark in landmarks:
        x = int(landmark.x * image.shape[1])
        y = int(landmark.y * image.shape[0])
        points.append([x, y])

    landmarks = np.array(points)
    
    nose_bridge_x = []
    nose_bridge_y = []
    for i in [4,5,1,2,0,198,14]:
            nose_bridge_x.append(landmarks[i][0])
            nose_bridge_y.append(landmarks[i][1])
            
            
    # x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)
    # ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[246][1]
    y_max = landmarks[2][1]
    #img2 = Image.open(image_path)
    # print(x_min,x_max,y_min,y_max)
    #img2 = img2.crop((x_min*1.05,y_min*0.9,x_max*1.08,y_max*0.94))
    img2 = image[int(y_min*0.9):int(y_max*0.95),int(x_min*1.15):int(x_max*1.1)]
    
    plt.imshow(img2)
    plt.show()
    #高斯滤波
    img_blur = cv2.GaussianBlur(np.array(img2),(3,3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image =img_blur, threshold1=30, threshold2=200)
    plt.imshow(edges, cmap =plt.get_cmap('gray'))
    plt.show()
    #center strip
    center = edges.shape[1] // 2
    # print(edges)
    # print((int(len(edges.T)/2)))
    edges_center = edges.T[(int(len(edges.T)/2))]

    #if(any(255 in i for i in [edges.T[center],edges.T[center+1],edges.T[center-1]])):
        
    #if (255 in edges.T[center],edges.T[center+1],edges.T[center-1]).any()):
    if 255 in edges_center:
        return True
    else:
        return False

import insightface
import cv2
import time
import numpy as np
from sklearn.decomposition import PCA

# 初始化模型并加载参数
model = insightface.app.FaceAnalysis()

model.prepare(ctx_id=0, det_thresh=0.45,det_size=(128, 128))

pca = PCA(n_components=4)


def get_feature_data(data):

    face = model.get(np.array(data))[0]

    embedding = face.embedding

    feature = embedding.reshape(32, -1)

    reduced_feature = pca.fit_transform(feature)

    return list(reduced_feature.reshape(-1))

def get_feature(image_path):
    face_img = cv2.imread(image_path)

    faces = model.get(face_img)[0]

    return faces

    

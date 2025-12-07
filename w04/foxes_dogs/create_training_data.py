import numpy as np
import pickle
import random
import os
from tqdm import tqdm
import cv2

DATADIR = "./data"
CATEGORIES = ["fox", "dog"]
IMG_SIZE = 50

training_data = []
def create_tr_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for img_name in tqdm(os.listdir(path)):
            try:
                img_path = os.path.join(path, img_name)
                img_array = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                resized_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append((resized_array, class_num))
            except Exception as e:
                pass
            
create_tr_data()
print(len(training_data))

random.shuffle(training_data)

X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)
    
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

with open('X.pkl', 'wb') as f:
    pickle.dump(X, f)
    
with open('y.pkl', 'wb') as f:
    pickle.dump(y, f)
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time

model = YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsBGR = [x, y]
        print(colorsBGR)
        
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('car_park.mp4')

coco_classes = open("coco.txt", "r")
data = coco_classes.read()
class_list = data.split("\n")

ret, frame = cap.read()
width, height = frame.shape[1], frame.shape[0]

area = [(width - 1050, height - 190), (width - 900, height - 30), (width - 820, height - 100), (width - 960, height - 220)]

while True:
    ret, frame  = cap.read()
    if not ret:
        break
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a.cpu()).astype("float")
    
    area_list = []
    
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5]) # car
        c = class_list[d]
        if ("car" in c) or ("cell phone" in c) or ("truck" in c) or ("bus" in c):
            center_x = int(x1 + x2) // 2
            center_y = int(y1 + y2) // 2
            results_area = cv2.pointPolygonTest(np.array(area, dtype=np.int32), ((center_x, center_y)), False)
            if results_area == 1:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)
                area_list.append((center_x, center_y))
                
    al = (len(area_list))
    
    if al > 0:
        cv2.polylines(frame, [np.array(area, dtype=np.int32)], True, (0, 0, 255), 2)
    else:
        cv2.polylines(frame, [np.array(area, dtype=np.int32)], True, (0, 255, 0), 2)
            
    cv2.imshow('RGB', frame)
    
    if cv2.waitKey(20) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

image_path = "lastofus.jpg"
img = cv2.imread(image_path)
reader = easyocr.Reader(['en'])
result = reader.readtext(img)
threshold = 0.5
for detection in result:
    bbox = detection[0]
    text = detection[1]
    confidence = detection[2]
    if confidence > threshold:
        start_point = tuple(map(int, bbox[0]))
        end_point = tuple(map(int, bbox[2]))
        print(f"Detected Text: {text}, Confidence: {confidence}")
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
        cv2.putText(img, text, (start_point[0], start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
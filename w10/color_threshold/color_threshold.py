import cv2
import numpy as np

video_path = "containers.mp4"

WIDTH = 800
HEIGHT = 600

def holder(x):
    pass

cv2.namedWindow("Color Threshold", cv2.WINDOW_NORMAL)

cv2.createTrackbar("min_blue", "Color Threshold", 0, 255, lambda x: None)
cv2.createTrackbar("min_green", "Color Threshold", 0, 255, lambda x: None)
cv2.createTrackbar("min_red", "Color Threshold", 0, 255, lambda x: None)
cv2.createTrackbar("max_blue", "Color Threshold", 255, 255, lambda x: None)
cv2.createTrackbar("max_green", "Color Threshold", 255, 255, lambda x: None)
cv2.createTrackbar("max_red", "Color Threshold", 255, 255, lambda x: None)
cv2.createTrackbar("area_threshold", "Color Threshold", 100, 5000, lambda x: None)

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_blue = cv2.getTrackbarPos("min_blue", "Color Threshold")
    min_green = cv2.getTrackbarPos("min_green", "Color Threshold")
    min_red = cv2.getTrackbarPos("min_red", "Color Threshold")
    max_blue = cv2.getTrackbarPos("max_blue", "Color Threshold")
    max_green = cv2.getTrackbarPos("max_green", "Color Threshold")
    max_red = cv2.getTrackbarPos("max_red", "Color Threshold")
    area_threshold = cv2.getTrackbarPos("area_threshold", "Color Threshold")

    lower_bound = np.array([min_blue, min_green, min_red])
    upper_bound = np.array([max_blue, max_green, max_red])

    mask = cv2.inRange(frame, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Color Threshold", result)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if contours:
        seg_contours = contours[:12]
        for i in seg_contours:
            area = cv2.contourArea(i)
            if area < area_threshold:
                continue
            (xmin, ymin, w, h) = cv2.boundingRect(i)
            cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 2)
            label = "Detected Object"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    cv2.imshow("Original", frame)
    
    # for contour in contours:
    #     area = cv2.contourArea(contour)
    #     # if area > 500:/
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
    # loop video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 
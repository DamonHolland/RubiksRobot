import cv2

cap = cv2.VideoCapture(0)
tracker = cv2.TrackerMOSSE_create()
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)

while True:
    timer = cv2.getTickCount()
    ret, img = cap.read()

    ret, bbox = tracker.update()

    fps = cv2.getTickFrequency()/(cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Tracking", img)

    if (cv2.waitKey(1) & 0xff == ord('q')):
        break

cap.release()
cap.destroyAllWindows()
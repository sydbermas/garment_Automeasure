import cv2
import numpy as np

class getpos:

    # Setup camera
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # Set a smaller resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    # Read logo and resize
    logo = cv2.imread('contours.png')
    # size = 400
    logo = cv2.resize(logo, (640, 480))

    # Create a mask of logo
    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Flip the frame
            frame = cv2.flip(frame, 1)

            # Region of Image (ROI), where we want to insert logo
            roi = frame

            # Set an index of where the mask is
            roi[np.where(mask)] = 0
            roi += logo

            cv2.imshow('WebCam', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

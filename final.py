import cv2
import imutils

images,names = utility.readImages()
descriptors = utility.getDescriptors(images)
# cap=cv2.VideoCapture("test.mp4")	#using video
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)				#Runtime camera
while(cap.isOpened()):
	success,frame=cap.read()
	if success:
		frame=imutils.resize(frame,width=400)
		gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		name = utility.findMatch(gray_frame,descriptors,names)
		# cv2.putText(frame,name,(20,20),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,255),2)
		# cv2.imshow("frame",frame)
		if cv2.waitKey(1)==ord('q'):
			break
	else:
		break

cap.release()
cv2.destroyAllWindows()
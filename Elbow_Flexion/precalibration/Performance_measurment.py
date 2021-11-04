
# coding: utf-8

# In[3]:


import cv2
import numpy as np
import time
import Pose_Module as pm

import os


path_current= os.path.abspath(os.getcwd())


## Reading video

#cap = cv2.VideoCapture(r"../left_hand.mp4")
cap = cv2.VideoCapture(0)
hasFrame, framee =cap.read()
frameeWidth= framee.shape[1]
frameeHeight= framee.shape[0]
os.path.abspath(os.getcwd())



vid_writer= cv2.VideoWriter(path_current+ '\\prediction\hand_angle.avi', cv2.VideoWriter_fourcc('M','J','P','G'),5, (framee.shape[1],framee.shape[0]))
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

## empty the text file
f = open("angle_file.txt","w")

f.close()
		
angle_calculation = []
while True:
	success, img = cap.read()
	img = cv2.resize(img, (1280, 720))
	# img = cv2.imread("AiTrainer/test.jpg")
	img = detector.findPose(img, False)
	lmList = detector.findPosition(img, False)
	# print(lmList)
	if len(lmList) != 0:
		# Right Arm
		angle , difference = detector.findAngle(img, 14, 12, 24)
		# # Left Arm

		#angle1 , difference1 = detector.findAngle(img, 13, 11, 23)
		
		# rounding the angle to put it in a text file
		rounded_angle= int(angle) 
		
		
		
		if rounded_angle > 9:
			f = open("angle_file.txt","a")
			
			f.write(str(rounded_angle))
			f.write(",")
			f.write("\n")
			f.close()
		
		per = np.interp(angle, (212, 326), (0, 100))
		bar = np.interp(angle, (212, 326), (650, 100))
		# print(angle, per)
		

		# Check for the curls
		color = (255, 0, 255)
		if per == 100:
			color = (0, 255, 0)
			if dir == 0:
				count += 0.5
				dir = 1
		if per == 0:
			color = (0, 255, 0)
			if dir == 1:
				count += 0.5
				dir = 0
		#print(count)
 
		# Draw Bar
		cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
		cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
		cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
					color, 4)
 
		# Draw Curl Count
		cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
		
		## controlling the counter here
		cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
					(255, 0, 0), 25)
 
	cTime = time.time()
	fps = 1 / (cTime - pTime)
	pTime = cTime
	cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
				(255, 0, 0), 5)
	vid_writer.write(img)
	
	if difference >0.25:
		img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
		cv2.putText(img, str("please correct posture"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
				(255, 0, 0), 5)
		cv2.imshow("Image", img)
		#print("PLEASE PRINT difference",difference)
		
	else:	 
		
		cv2.imshow("Image", img)
	
	#cv2.waitKey(1)
	

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()


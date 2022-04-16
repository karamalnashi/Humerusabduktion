import cv2
import mediapipe as mp
import time
import math
 
class poseDetector():
 
	def __init__(self, mode=False, upBody=False, smooth=True,
				 detectionCon=0.5, trackCon=0.5):
 
		self.mode = mode
		self.upBody = upBody
		self.smooth = smooth
		self.detectionCon = detectionCon
		self.trackCon = trackCon

		self.mpDraw = mp.solutions.drawing_utils
		self.mpPose = mp.solutions.pose
		self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
									 self.detectionCon, self.trackCon)
		self.angel=0
		self.difference=0
		self.position=True


	def findPerson(self,image):
		mp_drawing = mp.solutions.drawing_utils
		mp_holistic = mp.solutions.holistic

		with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

				results = holistic.process(image)
				# Draw landmark annotation on the image.

				#image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				#mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
				print(results.pose_landmarks)
				if results.pose_landmarks!=None:
					result= True
				else:
					result=False

				#cv2.imshow('MediaPipe Holistic', image)

		return result


	def findPose(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.pose.process(imgRGB)
		if self.results.pose_landmarks:
			if draw:
				self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
										   self.mpPose.POSE_CONNECTIONS)
		return img
 
	def findPosition(self, img, draw=True):
		self.lmList = []
		if self.results.pose_landmarks:
			for id, lm in enumerate(self.results.pose_landmarks.landmark):
				h, w, c = img.shape
				#print("the id and lm is : ",id, lm)
				cx, cy,cz = int(lm.x * w), int(lm.y * h), lm.z
				self.lmList.append([id, cx, cy,cz])
				if draw:
					cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
		return self.lmList
 
	def findAngle(self, img, p1, p2, p3, draw=True):

		try:
			x1, y1, z1 = self.lmList[p1][1:]
			x2, y2, z2 = self.lmList[p2][1:]
			# x3, y3,z3 = self.lmList[p3][1:]
			cx3, cy3, cz3 = self.lmList[p3][1:]
			# x3,y3,z3=((x2+cx3)//2)-40, (y2+cy3) // 2 , (z2+cz3) //2

			# z=100
			self.difference = abs(z2 - z1)
			# print("the value of z1 axis is ",z1)
			# Calculate the Angle

			if p1 == 14:
				# Right Arm
				x3, y3, z3 = ((x2 + cx3) // 2) - 40, (y2 + cy3) // 2, (z2 + cz3) // 2
				self.angle = math.degrees(math.atan2(y1 - y2, x1 - x2) -
								 math.atan2(y3 - y2, x3 - x2))
			else:
				# # Left Arm
				x3, y3, z3 = ((x2 + cx3) // 2) + 30, (y2 + cy3) // 2, (z2 + cz3) // 2
				self.angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
								 	math.atan2(y1 - y2, x1 - x2))

			if self.angle < 0:
				self.angle += 360

			# print(angle)

			# Draw
			if draw:
				cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
				cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
				cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
				cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
				cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
				cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
				cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
				cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
				cv2.putText(img, str(int(self.angle)), (x2 - 50, y2 + 50),
							cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
		# cv2.putText(img, str(difference), (x2 - 350, y2 + 50),
		# cv2.FONT_HERSHEY_PLAIN, 2, (0, 211, 255), 2)

		except:
			print("list index out of range")
			self.position=False
		# Get the landmarks

		return self.angle,self.difference, self.position
 


# In[ ]:


def main():
	cap = cv2.VideoCapture(0)
	pTime = 0
	detector = poseDetector()
	while True:
		success, img = cap.read()
		img = detector.findPose(img)
		lmList = detector.findPosition(img, draw=False)
		if len(lmList) != 0:
			#print(lmList[12])
			cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 0, 255), cv2.FILLED)
 
		cTime = time.time()
		fps = 1 / (cTime - pTime)
		pTime = cTime
 
		cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
					(255, 0, 0), 3)
 
		cv2.imshow("Image", img)
		cv2.waitKey(1)
		
 
if __name__ == "__main__":
	main()



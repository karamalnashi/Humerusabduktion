import json

import cv2
import paho.mqtt.client as mqttclient
import numpy as np
import time
import Pose_Module as pm

import os


path_current= os.path.abspath(os.getcwd())


## Reading video

#cap = cv2.VideoCapture(r"../videos/test.MOV") #capture by a video file
cap = cv2.VideoCapture(0) # capture by your own camera
hasFrame, framee =cap.read()
frameeWidth= framee.shape[1]
frameeHeight= framee.shape[0]
os.path.abspath(os.getcwd())





#vid_writer= cv2.VideoWriter(path_current+ '\\prediction\hand_angle.avi', cv2.VideoWriter_fourcc('M','J','P','G'),5, (framee.shape[1],framee.shape[0]))
detector = pm.poseDetector()
count = 0
count1=0
dir = 0
dir1 = 0
pTime = 0
db = 1    #aktuellem Datenbankeintrag
x=0
z=1
 

broker_address = "l51d159d-internet-facing-6e9635f0905aed75.elb.us-east-1.amazonaws.com"
port = 1883
user = "test"
password = "test"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("client is error")


def on_message(client, userdata, message):
    print("message recieved = " + str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)


Messagerecieved = False
connected = False

client = mqttclient.Client("MQTT")
client.on_message = on_message
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.connect(broker_address, port=port)

client.loop_start()
client.subscribe("ebrain/#")

while True:
	success, img = cap.read()
	img = cv2.resize(img, (1280, 720))
	# img = cv2.imread("AiTrainer/test.jpg")
	img = detector.findPose(img, False)
	lmList = detector.findPosition(img, False)
	##print(lmList)

########################################################################
	if len(lmList) != 0:
		# Right Arm
		angle , difference = detector.findAngle(img, 14, 12, 24)
		# # Left Arm
		angle1 , difference1 = detector.findAngle(img, 13, 11, 23)
########################################################################
		## Read text file
		#Minimum value
		f = open(r"../precalibration/test1.txt", "r")
		minimum = min(f)
		value_min= int(minimum.replace(',', ''))
		f.close()
		# Maximum value
		f = open(r"../precalibration/test1.txt", "r")
		maximum= max(f)
		value_max= int(maximum.replace(',', ''))
		value_max = value_max + 10
		f.close()
		#print("the maximum value",value_max)
#########################################################################

		per = np.interp(angle, (value_min, value_max), (0, 100))
		bar = np.interp(angle, (value_min, value_max), (650, 100))
		#count for Right
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

		per1 = np.interp(angle1, (value_min, value_max), (0, 100))
		bar1 = np.interp(angle1, (value_min, value_max), (650, 100))
		# -------------------------------------------------------------------
		# count for link
		color = (255, 0, 255)
		if per1 == 100:
			color = (0, 255, 0)
			if dir1 == 0:
				count1+= 0.5
				dir1 = 1
		if per1 == 0:
			color = (0, 255, 0)
			if dir1 == 1:
				count1 += 0.5
				dir1 = 0
		#print(count)
###############################################################################
		if db ==0.25 :
			dba=33
		elif db == 0.5:
			dba =45
		elif db ==0.75:
			dba=58
		else:
			dba=72


		def procedure():
			start_time = time.time()
			seconds = 3

			while True:
				current_time = time.time()
				elapsed_time = current_time - start_time

				if elapsed_time > seconds:
					break

		# Right Arm
		if db==	1:
			if angle<20 and angle1<25:
				z=1

			if angle > 20 and angle1<25 and z==1:
					if angle > 75:
						img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
						cv2.putText(img, str("Bitte bewege deine rechte Hand nach unten"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[0]
						y0 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y0)
					elif angle<65:
						# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
						cv2.putText(img, str("Bitte bewege deine rechte Hand nach oben"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[1]
						y1 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y1)
					elif 65<angle<70:
						# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
						cv2.putText(img, str("und noch etwas weiter"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[2]
						y2 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y2)
					else:
						cv2.putText(img, str("einen Moment da bleiben und dabei entspannen"), (20, 50), cv2.FONT_HERSHEY_PLAIN,
									3,(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[3]
						y3 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y3)
						z=0
		# -------------------------------------------------------------------
		# Left Arm
			elif angle < 30 and angle1> 25 and z==1:
					if angle1 > 75:
						img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
						cv2.putText(img, str("Bitte bewege deine linke Hand nach unten"), (20, 50),
								cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[4]
						y4 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y4)
					elif angle1 < 65 :
							# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
						cv2.putText(img, str("Bitte bewege deine linke Hand nach oben"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[5]
						y5 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y5)
					elif 65<angle1<70:
						# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
						cv2.putText(img, str("und noch etwas weiter"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[6]
						y6 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y6)
					else:
						cv2.putText(img, str("noch einen Moment da bleiben und dabei entspannen"), (20, 50), cv2.FONT_HERSHEY_PLAIN,
									3,(255, 0, 0), 3)
						cv2.imshow("Image", img)
						f = open('data.json')
						data = json.load(f)
						x = data[7]
						y7 = json.dumps(x)
						client.publish("ebrain/DialogEngine1/interaction", y7)
						z=0
			elif z==1:
					cv2.putText(img, str("Nur eine Hand bewegen"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[8]
					y8 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y8)
					z=1
				#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

			# ///////////Wenn der Patient nicht alleine trainieren kann///////////
		else:
			if angle<25 and angle1<25:
				z=1
			if angle > 25 and angle1 < 25 and z==1:
				if angle > 75:
					img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
					cv2.putText(img, str("Bitte bewege deine rechte Hand nach unten"), (20, 50),
								cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[9]
					y9 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y9)
				elif dba-5< angle < dba:
					# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
					cv2.putText(img, str("und noch etwas weiter"), (20, 50),
								cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[10]
					y10 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y10)
					y = 0
					x=0

				elif dba< angle < dba+5:
						j = 30
						while j>=0 and x==0:
								ret, img = cap.read()
								img = cv2.resize(img, (1280, 720))
								if j>10:

										cv2.putText(img, str("Gut,und noch etwas weiter, wenn es geht"), (20, 50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
										cv2.putText(img,str(j//10),(250,250), cv2.FONT_HERSHEY_PLAIN, 15,(255,255,255),10,cv2.LINE_AA)
										f = open('data.json')
										data = json.load(f)
										x = data[11]
										y11= json.dumps(x)
										client.publish("ebrain/DialogEngine1/interaction", y11)

								elif j<=9:

										cv2.putText(img, str("Ihr Helfer darf jetzt den Rest ergaenzen"),  (20, 50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
								cv2.imshow("Image", img)
								cv2.waitKey(125)
								f = open('data.json')
								data = json.load(f)
								x = data[12]
								y12 = json.dumps(x)
								client.publish("ebrain/DialogEngine1/interaction", y12)
								j = j - 1
								if j ==0:
									x = 1
								z=0

			# -------------------------------------------------------------------
			# Left Arm
			elif angle < 25 and angle1 > 25 and z==1:
				if angle1 > 75:
					img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
					cv2.putText(img, str("Bitte bewege deine linke Hand nach unten"), (20, 50),
								cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[13]
					y13 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y13)
				elif dba-5< angle1 < dba:
					# img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
					cv2.putText(img, str("und noch etwas weiter"), (20, 50),
								cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					x = 0
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[14]
					y14 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y14)
				elif dba < angle1 < dba + 5:
					j = 30
					while j >= 0 and x == 0:
						ret, img = cap.read()
						img = cv2.resize(img, (1280, 720))
						if j > 10:

							cv2.putText(img, str("Gut,und noch etwas weiter, wenn es geht"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
							cv2.putText(img, str(j // 10), (250, 250), cv2.FONT_HERSHEY_PLAIN, 15, (255, 255, 255), 10,
										cv2.LINE_AA)
							f = open('data.json')
							data = json.load(f)
							x = data[15]
							y15 = json.dumps(x)
							client.publish("ebrain/vDialogEngine1/interaction", y15)

						elif j <= 9:

							cv2.putText(img, str("Ihr Helfer darf jetzt den Rest ergaenzen"), (20, 50),
									cv2.FONT_HERSHEY_PLAIN, 3,
									(255, 0, 0), 3)
							f = open('data.json')
							data = json.load(f)
							x = data[16]
							y16 = json.dumps(x)
							client.publish("ebrain/DialogEngine1/interaction", y16)
						cv2.imshow("Image", img)
						cv2.waitKey(125)

						j = j - 1
						if j == 0:
							x = 1
						z=0

			elif z==1:
					cv2.putText(img, str("Nur eine Hand bewegen"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
								(255, 0, 0), 3)
					cv2.imshow("Image", img)
					f = open('data.json')
					data = json.load(f)
					x = data[17]
					y17 = json.dumps(x)
					client.publish("ebrain/DialogEngine1/interaction", y17)
					z==1

###############################################################################

	# Draw Bar Right
		cv2.rectangle(img, (100, 100), (175, 650), 3)
		cv2.rectangle(img, (100, int(bar)), (175, 650), color, cv2.FILLED)
		cv2.putText(img, f'{int(per)} %', (100, 75), cv2.FONT_HERSHEY_PLAIN, 2,
					color, 4)

		# Draw Curl Count Right
		#cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
		cv2.putText(img,"R: "+ str(int(count)), (50, 720), cv2.FONT_HERSHEY_PLAIN, 5,
					(255, 0, 0), 5)
	# -------------------------------------------------------------------
		# Draw Bar link
		cv2.rectangle(img, (1100, 100 ), (1175, 650), color, 3)
		cv2.rectangle(img, (1100	, int(bar1)), (1175, 650), color, cv2.FILLED)
		cv2.putText(img, f'{int(per1)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 2,
					color, 4)

	# Draw Curl Count link
		#cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
		cv2.putText(img,"L: "+ str(int(count1)), (1050, 720), cv2.FONT_HERSHEY_PLAIN, 5,
					(255, 0, 0), 5)
###############################################################################
		cTime = time.time()
		fps = 1 / (cTime - pTime)
		pTime = cTime
	#cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
				#(255, 0, 0), 5)
	#vid_writer.write(img)


	# calcuates the z axis i.e. the posture of the hand_angle


		if difference >0.35:
			img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
			cv2.putText(img, str("please correct posture"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
					(255, 0, 0), 5)
			cv2.imshow("Image", img)
			f = open('data.json')
			#data = json.load(f)
			#x = data[18]
			#y18 = json.dumps(x)
			#client.publish("ebrain/DialogEngine1/interaction", y18)
			print(difference)

		else:

			cv2.imshow("Image", img)

		cv2.waitKey(1)


		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()

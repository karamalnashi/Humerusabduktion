import json
import math
import os
import paho.mqtt.client as mqttclient
import cv2
import time
import numpy as np
import pyttsx3
import Pose_Module_Finger as htm
detector = htm.handDetector(detectionCon=0.7)

class Mqtt():

    def __init__(self,mqtt_start: bool=False ,def_triener: bool=False, mqtt_host:str="localhost" , mqtt_port: int =1883 , mqtt_user:str="mqtt", mqtt_password:str="test",mqtt_keep_alive:int=60):
        self._mqtt_host=mqtt_host
        self._mqtt_port=mqtt_port
        self._mqtt_keep_alive=mqtt_keep_alive
        self._mqtt_cleint= mqttclient.Client("MQTT")
        self._mqtt_cleint.username_pw_set(mqtt_user, password=mqtt_password)
        self._mqtt_cleint.on_connect=self.on_connect
        self._mqtt_cleint.on_message=self.on_message

        self.end_While=False
        self.def_triener=def_triener
        self.cap = cv2.VideoCapture(0)  # capture by your own camera
        path_current = os.path.abspath(os.getcwd())
        hasFrame, framee = self.cap.read()
        #frameeWidth = framee.shape[1]
        #frameeHeight = framee.shape[0]
        os.path.abspath(os.getcwd())
        if mqtt_start:
            self.start_mqtt()


    def start_mqtt(self):
        self._mqtt_cleint.connect_async(self._mqtt_host,port=self._mqtt_port,keepalive=self._mqtt_keep_alive)
        self._mqtt_cleint.loop_start()
        self._mqtt_cleint.subscribe("ebrain/#")

    def stop_mqtt(self):
        self._mqtt_cleint.loop_stop()

    def stop_Ubung(self):
        print("die arbeit ist Fertig")
        f = open('data_finger.json')
        data = json.load(f)
        i = data[3]
        j = json.dumps(i)
        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", j)
        self.stop_mqtt()

    def convert_To_Voice(self,data):
        Data = json.loads(data)
        say = Data["content"]["say"]
        print(say)
        text_speech = pyttsx3.init()
        text_speech.say(say)
        text_speech.runAndWait()

    def on_connect(self, client, userdata, flags, rc):
            assert client == self._mqtt_cleint
            if rc == 0:
                print("client is connected")
                client.subscribe("ebrain/#")
                global connected
                connected = True,
            else:
                print("client is error")

    def on_message(self ,client, userdata, message):
            assert client == self._mqtt_cleint
            print("message recieved = " + str(message.payload.decode("utf-8")))
            print("message topic=", message.topic)
            msg = message.payload.decode("utf-8")

            try:
                self.layout_type = msg["content"]["layout_type"]
                if self.layout_type == "end":
                    self.stop_mqtt()
                    self.end_While = True
            except:
                print("keine content")


            self.convert_To_Voice(msg)

#####################################     CLASS TRIEN   ###############################################################################################

class trien_Finger(Mqtt):
    length, volBar,volPer,dir, color=0,0,0,0,(0, 255, 0)
    t, t1 = 100, 100
    count = 0
    def __init__(self, mqtt_start: bool = False, def_triener: bool = False, mqtt_host: str = "localhost",
                 mqtt_port: int = 1883, mqtt_user: str = "mqtt", mqtt_password: str = "test",
                 mqtt_keep_alive: int = 60,exercise_number="",side="",count="",patient_movement_range="",time_pause=""):

        super(trien_Finger,self).__init__()
        self.time_p=time_pause/2
        self.side=side
        self.exercise_number=exercise_number
        self.count_Pa=int(count)
        self.patient_movement_range=float(patient_movement_range)
        print(self.side)
        print(self.exercise_number)
        print(self.count_Pa)
        print(self.patient_movement_range)

        self.x1 = None
        self.x2 = None
        self.cx = None
        self.y1 = None
        self.y2 = None
        self.cy = None

        if def_triener:
            self.start_mqtt()
            self.TrienerLoop()



    def TrienerLoop(self):

        self.Check_Side()

        while (True):
            success, img = self.cap.read()
            img = cv2.resize(img, (1280, 720))
            img = detector.findHands(img)
            lmList = detector.findPosition(img,False)

            ### Beginning of training
            if len(lmList) != 0:

                self.count_Calculator(lmList)

                if self.end_While == True:
                    self.stop_mqtt()
                    break
                if self.count == self.count_Pa:
                    self.stop_Ubung()
                    break

                if self.length < 40:
                    cv2.circle(img, (self.cx, self.cy), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, str("Ihres Daumens wieder weit weg"), (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)
                    # cv2.imshow("Image", img)
                    f = open('data_finger.json')
                    data = json.load(f)
                    x = data[0]
                    y1 = json.dumps(x)
                    if self.t > 99:
                        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y1)
                        self.timer(self.time_p)
                        self.t = 0
                    else:
                        self.t = self.t + 1
                        print(self.t)
                        self.t1 = 100
                elif self.length > 110:
                    cv2.circle(img, (self.cx, self.cy), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, str("Ihres Daumens an Ihre Hand heran"), (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)
                    # cv2.imshow("Image", img)
                    f = open('data_finger.json')
                    data = json.load(f)
                    x = data[1]
                    y2 = json.dumps(x)
                    if self.t1 > 99:
                        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y2)
                        self.timer(self.time_p)
                        self.t1 = 0
                    else:
                        self.t1 = self.t1 + 1
                        print(self.t1)
                        self.t = 100
                self.draw(img)
                # ###################### # ######################
            else:
                print("keine")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



        self.cap.release()
        cv2.destroyAllWindows()

    def count_Calculator(self,lmList):
        self.x1, self.y1 = lmList[4][1], lmList[4][2]
        self.x2, self.y2 = lmList[6][1], lmList[6][2]
        self.cx, self.cy = (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

        self.length = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        self.volBar = np.interp(self.length, [50, 110], [400, 150])
        self.volPer = np.interp(self.length,[50, 110],[0, 100])


        self.color = (255, 0, 255)
        if self.volPer == 100:
            self.color = (0, 255, 0)
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1
        if self.volPer == 0:
            self.color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
    def Check_Side(self):
        success, img = self.cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        try:
            thumb_tip = lmList[4][1]
            print(thumb_tip)
            pinky_tip = lmList[20][1]
            print(pinky_tip)
            if self.side == "left":
                if thumb_tip < pinky_tip:
                    pass
                else:
                    print("Bitte drehen Sie Ihre Hand")
                    f = open('data_finger.json')
                    data = json.load(f)
                    x = data[2]
                    y3 = json.dumps(x)
                    self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y3)
                    time.sleep(6)
            elif self.side == "right":
                if thumb_tip < pinky_tip:
                    print("Bitte drehen Sie Ihre Hand")
                    f = open('data_finger.json')
                    data = json.load(f)
                    x = data[2]
                    y3 = json.dumps(x)
                    self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y3)
                    time.sleep(6)
                else:
                    pass
            else:
                print("keine Hand-side")
        except:
            print("list index out of range")

    def timer(self,time_pause):
        while time_pause:
            time.sleep(1)
            print(time_pause )
            time_pause-= 1
        self.timer_end=True


    def draw(self,img):
        cv2.circle(img, (self.x1, self.y1), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (self.x2, self.y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (self.x1, self.y1), (self.x2, self.y2), (255, 0, 255), 3)
        cv2.circle(img, (self.cx, self.cy), 7, (255, 0, 255), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(self.volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(self.volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)
        cv2.putText(img, "count: " + str(int(self.count)), (150, 450), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 2)


        cv2.imshow("Img", img)



if __name__ == "__main__":
    print("Hello world!")
else:
    mqtt=Mqtt()


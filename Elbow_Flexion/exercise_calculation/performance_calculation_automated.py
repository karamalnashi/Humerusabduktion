import cv2
import numpy as np
import pyttsx3
import paho.mqtt.client as mqttclient
import pyttsx3
import json
import Pose_Module as pm
import os
#from mqtt import mqttCon
# cap = cv2.VideoCapture(r"../videos/test.MOV") #capture by a video file
cap = cv2.VideoCapture(0)  # capture by your own camera
path_current = os.path.abspath(os.getcwd())
hasFrame, framee = cap.read()
frameeWidth = framee.shape[1]
frameeHeight = framee.shape[0]
os.path.abspath(os.getcwd())
detector = pm.poseDetector()
#mqtt = mqttCon()

db = 1  # aktuellem Datenbankeintrag / 1 , 0.75, 0.5 , 0,25
arm = 1  # linke-Arm =0 , rechte-Arm

broker_address = "localhost"
port = 1883
user = "mqtt"
password = "test"


class Run:


        def __init__(self,mqtt_start: bool = True):
            super(Run, self).__init__()
            self.person_dec=self.person_dec
            self.on_message=self.on_message()
            self.star=self.start
            self.client=self.client
            self.on_connect=self.on_connect
            self.convert=self.convert



        def person_dec(self):
            cap = cv2.VideoCapture(0)
            while True:
                success, img = cap.read()
                img = cv2.resize(img, (1280, 720))
                # img = cv2.imread("AiTrainer/test.jpg")
                result = detector.findPerson(img)
                print(result)
                if result == True:
                    break
            return result

        def on_connect(self,client, userdata, flags, rc):

            if rc == 0:
                print("client is connected")
                global connected
                connected = True
            else:
                print("client is error")


        def on_message(self, client, userdata, message):
            print("message recieved = " + str(message.payload.decode("utf-8")))
            print("message topic=", message.topic)

            if message.topic == "ebrain/start":
                person_result = self.person_dec()
                if person_result == True:
                    print("okkkkkkkkkkkkk")
                    f = open('data.json')
                    data = json.load(f)
                    x = data[19]
                    y = json.dumps(x)
                    client.publish("ebrain/DialogEngine1/interaction", y)
                    # pass
                    # time.sleep(4)
                    # startStope.start(message.topic)
                    # startStope.start(message.topic)
                else:
                    print("neiiiiiiiiiin")


            elif message.topic == "ebrain/ja":
                self.start(message.topic)

            elif message.topic == "ebrain/DialogEngine1/interaction":
                print(message.topic)
                print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")

        Messagerecieved = False
        connected = False
        client = mqttclient.Client("MQTT")
        client.on_message = on_message
        client.username_pw_set(user, password=password)
        client.on_connect = on_connect
        client.connect(broker_address, port=port)
        client.loop_start()
        client.subscribe("ebrain/#")




        cap = cv2.VideoCapture(0)  # capture by your own camera
        path_current = os.path.abspath(os.getcwd())
        hasFrame, framee = cap.read()
        frameeWidth = framee.shape[1]
        frameeHeight = framee.shape[0]
        os.path.abspath(os.getcwd())

        def convert(self, data1):
            data = json.loads(data1)
            say = data["content"]["say"]
            print(say)
            text_speech = pyttsx3.init()
            text_speech.say(say)
            text_speech.runAndWait()


        def start(self,status):
            count, count1, dir, dir1, pTime, back, x, z = 0, 0, 0, 0, 0, 0, 0, 1
            t, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
            cap = cv2.VideoCapture(0)
            y=status

            #def convert(data1):
                #data = json.loads(data1)
                #say = data["content"]["say"]
                #print(say)
                #text_speech = pyttsx3.init()
                #text_speech.say(say)
                #text_speech.runAndWait()

            #def on_connect(client, userdata, flags, rc):
                #if rc == 0:
                    #print("client is connected")
                    #global connected
                    #connected = True
                #else:
                    #print("client is error")

            #def on_message(client, userdata, message):
                #print("message recieved = " + str(message.payload.decode("utf-8")))
                #print("message topic=", message.topic)
                #msg=message.payload.decode("utf-8")
                #convert(msg)

            Messagerecieved = False
            #connected = False
            #client = mqttclient.Client("MQTT")
            #client.on_message = on_message
            #client.username_pw_set(user, password=password)
            #client.on_connect = on_connect
            #client.connect(broker_address, port=port)

            #client.loop_start()
            #client.subscribe("ebrain/#")

            while y !="ebrain/end":
                success, img = cap.read()
                img = cv2.resize(img, (1280, 720))
                # img = cv2.imread("AiTrainer/test.jpg")
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)
                f = open(r"../precalibration/test1.txt", "r")
                minimum = min(f)
                value_min = int(minimum.replace(',', ''))
                f.close()
                # Maximum value
                f = open(r"../precalibration/test1.txt", "r")
                maximum = max(f)
                value_max = int(maximum.replace(',', ''))
                value_max = value_max + 10
                f.close()

                if db == 0.25:
                    dba = 33
                elif db == 0.5:
                    dba = 45
                elif db == 0.75:
                    dba = 58
                else:
                    dba = 72

                # ######################  linke-arm  #################################
                if arm == 0:
                    if len(lmList) != 0:
                        # # Left Arm
                        angle1, difference1 = detector.findAngle(img, 13, 11, 23)

                        per1 = np.interp(angle1, (value_min, value_max), (0, 100))
                        bar1 = np.interp(angle1, (value_min, value_max), (650, 100))
                        # -------------------------------------------------------------------
                        # count for link
                        color = (255, 0, 255)
                        if per1 == 100:
                            color = (0, 255, 0)
                            if dir1 == 0:
                                count1 += 0.5
                                dir1 = 1
                        if per1 == 0:
                            color = (0, 255, 0)
                            if dir1 == 1:
                                count1 += 0.5
                                dir1 = 0
                        ########################################################
                        if db == 1:
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
                                if t > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y4)
                                    t = 0
                                else:
                                    t = t + 1
                                    print(t)
                                t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1


                            elif angle1 < 65:
                                if angle1 < 25 and back == 1:
                                    cv2.putText(img, str("Danke"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[18]
                                    y18 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y18)
                                    cv2.imshow("Image", img)
                                    back = 0
                                elif angle1 < 65 and back == 0:
                                    # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                    cv2.putText(img, str("Bitte bewege deine linke Hand nach oben"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    cv2.imshow("Image", img)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[5]
                                    y5 = json.dumps(x)
                                    if t1 > 99:
                                        self.client.publish("ebrain/DialogEngine1/interaction", y5)
                                        t1 = 0
                                    else:
                                        t1 = t1 + 1
                                        print(t1)
                                    t, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100

                            elif 65 < angle1 < 70 and back == 0:
                                # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[6]
                                y6 = json.dumps(x)
                                if t2 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y6)
                                    t2 = 0
                                else:
                                    t2 = t2 + 1
                                    print(t2)
                                t, t1, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                            elif 70 < angle1 <= 75 and back == 0:
                                cv2.putText(img, str("noch einen Moment da bleiben und dabei entspannen"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN,
                                            3, (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[7]
                                y7 = json.dumps(x)
                                if t3 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y7)
                                    t3 = 0
                                else:
                                    t3 = t3 + 1
                                    print(t3)
                                t, t1, t2, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1

                        # ///////////Wenn der Patient nicht alleine trainieren kann///////////
                        else:
                            if angle1 < 25:
                                if back == 1:
                                    cv2.putText(img, str("Danke"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[18]
                                    y18 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y18)
                                    cv2.imshow("Image", img)
                                    back = 0
                                else:
                                    cv2.putText(img, str("Bitte bewege deine linke Hand nach oben"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    cv2.imshow("Image", img)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[5]
                                    y5 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y5)

                            elif angle1 > 70:
                                img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
                                cv2.putText(img, str("Bitte bewege deine linke Hand nach unten"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[8]
                                y13 = json.dumps(x)
                                if t4 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y13)
                                    t4 = 0
                                else:
                                    t4 = t4 + 1
                                    print(t4)
                                t, t1, t2, t3, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1
                            elif dba - 5 < angle1 < dba and back == 0:
                                # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                u = 0
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[14]
                                y14 = json.dumps(x)
                                if t5 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y14)
                                    t5 = 0
                                else:
                                    t5 = t5 + 1
                                    print(t5)
                                t, t1, t2, t3, t4, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                            elif dba < angle1 < dba + 5 and back == 0:
                                j = 30
                                while j >= 0 and u == 0:
                                    ret, img = cap.read()
                                    img = cv2.resize(img, (1280, 720))
                                    if j > 10:

                                        cv2.putText(img, str("Gut,und noch etwas weiter, wenn es geht"), (20, 50),
                                                    cv2.FONT_HERSHEY_PLAIN, 3,
                                                    (255, 0, 0), 3)
                                        cv2.putText(img, str(j // 10), (250, 250), cv2.FONT_HERSHEY_PLAIN, 15,
                                                    (255, 255, 255),
                                                    10,
                                                    cv2.LINE_AA)
                                        f = open('data.json')
                                        data = json.load(f)
                                        x = data[15]
                                        y15 = json.dumps(x)
                                        if t6 > 99:
                                            self.client.publish("ebrain/vDialogEngine1/interaction", y15)
                                            t6 = 0
                                        else:
                                            t6 = t6 + 1
                                        t, t1, t2, t3, t5, t4, t7, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                    elif j <= 9:

                                        cv2.putText(img, str("Ihr Helfer darf jetzt den Rest ergaenzen"), (20, 50),
                                                    cv2.FONT_HERSHEY_PLAIN, 3,
                                                    (255, 0, 0), 3)
                                        f = open('data.json')
                                        data = json.load(f)
                                        x = data[16]
                                        y16 = json.dumps(x)
                                        if t7 > 99:
                                            self.client.publish("ebrain/DialogEngine1/interaction", y16)
                                            t7 = 0
                                        else:
                                            t7 = t7 + 1
                                        t, t1, t2, t3, t5, t6, t4, t8, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                    cv2.imshow("Image", img)
                                    cv2.waitKey(125)

                                    j = j - 1
                                    if j == 0:
                                        x = 1

                    # -------------------------------------------------------------------
                    # Draw Bar link
                    cv2.rectangle(img, (1100, 100), (1175, 650), 3)
                    cv2.rectangle(img, (1100, int(bar1)), (1175, 650), color, cv2.FILLED)
                    cv2.putText(img, f'{int(per1)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 2,
                                color, 4)

                    # Draw Curl Count link
                    # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "L: " + str(int(count1)), (1050, 720), cv2.FONT_HERSHEY_PLAIN, 5,
                                (255, 0, 0), 5)

                    if difference1 > 0.35:
                        img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
                        cv2.putText(img, str("please correct posture"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                                    (255, 0, 0), 5)
                        cv2.imshow("Image", img)
                        f = open('data.json')
                        # data = json.load(f)
                        # x = data[17]
                        # y18 = json.dumps(x)
                        # client.publish("ebrain/DialogEngine1/interaction", y18)
                        # print(difference1)

                    else:

                        cv2.imshow("Image", img)


                # ######################  linke-arm  #################################
                else:
                    if len(lmList) != 0:
                        # Right Arm
                        angle, difference = detector.findAngle(img, 14, 12, 24)
                        per = np.interp(angle, (value_min, value_max), (0, 100))
                        bar = np.interp(angle, (value_min, value_max), (650, 100))
                        # count for Right
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

                        if db == 1:
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
                                if t8 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y0)
                                    t8 = 0
                                else:
                                    t8 = t8 + 1
                                    print(t8)
                                t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1

                            elif angle < 65:
                                if angle < 25 and back == 1:
                                    cv2.putText(img, str("Danke"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[18]
                                    y18 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y18)
                                    cv2.imshow("Image", img)
                                    back = 0
                                elif angle < 65 and back == 0:
                                    # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                    cv2.putText(img, str("Bitte bewege deine rechte Hand nach oben"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    cv2.imshow("Image", img)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[1]
                                    y1 = json.dumps(x)
                                    if t9 > 99:
                                        self.client.publish("ebrain/DialogEngine1/interaction", y1)
                                        t9 = 0
                                    else:
                                        t9 = t9 + 1
                                        print(t9)
                                    t, t1, t2, t3, t5, t6, t7, t4, t8, t10, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100


                            elif 65 < angle < 70 and back == 0:
                                # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[2]
                                y2 = json.dumps(x)
                                if t10 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y2)
                                    t10 = 0
                                else:
                                    t10 = t10 + 1
                                    print(t10)
                                t, t1, t2, t3, t5, t6, t7, t4, t9, t8, t11, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                            else:
                                cv2.putText(img, str("einen Moment da bleiben und dabei entspannen"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN,
                                            3, (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[3]
                                y3 = json.dumps(x)
                                if t11 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y3)
                                    t11 = 0
                                else:
                                    t11 = t11 + 1
                                    print(t11)
                                t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t8, t12, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1

                        # ///////////Wenn der Patient nicht alleine trainieren kann///////////
                        else:
                            if angle < 25:
                                if back == 1:
                                    cv2.putText(img, str("Danke"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[18]
                                    y18 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y18)
                                    cv2.imshow("Image", img)
                                    back = 0
                                else:
                                    cv2.putText(img, str("Bitte bewege deine rechte Hand nach oben"), (20, 50),
                                                cv2.FONT_HERSHEY_PLAIN, 3,
                                                (255, 0, 0), 3)
                                    cv2.imshow("Image", img)
                                    f = open('data.json')
                                    data = json.load(f)
                                    x = data[1]
                                    y1 = json.dumps(x)
                                    self.client.publish("ebrain/DialogEngine1/interaction", y1)

                            elif angle > 70:
                                img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
                                cv2.putText(img, str("Bitte bewege deine rechte Hand nach unten"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[13]
                                y13 = json.dumps(x)
                                if t12 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y13)
                                    t12 = 0
                                else:
                                    t12 = t12 + 1
                                    print(t12)
                                t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t11, t8, t13, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                back = 1
                            elif dba - 5 < angle < dba and back == 0:
                                # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
                                cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 0, 0), 3)
                                u = 0
                                cv2.imshow("Image", img)
                                f = open('data.json')
                                data = json.load(f)
                                x = data[14]
                                y14 = json.dumps(x)
                                if t13 > 99:
                                    self.client.publish("ebrain/DialogEngine1/interaction", y14)
                                    t13 = 0
                                else:
                                    t13 = t13 + 1
                                    print(t13)
                                t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t11, t12, t8, t14, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                            elif dba < angle < dba + 5 and back == 0:
                                j = 30
                                while j >= 0 and u == 0:
                                    ret, img = cap.read()
                                    img = cv2.resize(img, (1280, 720))
                                    if j > 10:

                                        cv2.putText(img, str("Gut,und noch etwas weiter, wenn es geht"), (20, 50),
                                                    cv2.FONT_HERSHEY_PLAIN, 3,
                                                    (255, 0, 0), 3)
                                        cv2.putText(img, str(j // 10), (250, 250), cv2.FONT_HERSHEY_PLAIN, 15,
                                                    (255, 255, 255),
                                                    10,
                                                    cv2.LINE_AA)
                                        f = open('data.json')
                                        data = json.load(f)
                                        x = data[15]
                                        y15 = json.dumps(x)
                                        if t14 > 99:
                                            self.client.publish("ebrain/vDialogEngine1/interaction", y15)
                                            t14 = 0
                                        else:
                                            t14 = t14 + 1
                                            print(t14)
                                        t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t11, t12, t13, t8, t15 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100

                                    elif j <= 9:

                                        cv2.putText(img, str("Ihr Helfer darf jetzt den Rest ergaenzen"), (20, 50),
                                                    cv2.FONT_HERSHEY_PLAIN, 3,
                                                    (255, 0, 0), 3)
                                        f = open('data.json')
                                        data = json.load(f)
                                        x = data[16]
                                        y16 = json.dumps(x)
                                        if t15 > 99:
                                            self.client.publish("ebrain/DialogEngine1/interaction", y16)
                                            t15 = 0
                                        else:
                                            t15 = t15 + 1
                                            print(t15)
                                        t, t1, t2, t3, t5, t6, t7, t4, t9, t10, t11, t12, t13, t14, t8 = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                                    cv2.imshow("Image", img)
                                    cv2.waitKey(125)

                                    j = j - 1
                                    if j == 0:
                                        x = 1

                    # Draw Bar Right
                    cv2.rectangle(img, (100, 100), (175, 650), 3)
                    cv2.rectangle(img, (100, int(bar)), (175, 650), color, cv2.FILLED)
                    cv2.putText(img, f'{int(per)} %', (100, 75), cv2.FONT_HERSHEY_PLAIN, 2,
                                color, 4)

                    # Draw Curl Count Right
                    # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "R: " + str(int(count)), (50, 720), cv2.FONT_HERSHEY_PLAIN, 5,
                                (255, 0, 0), 5)
                    if difference > 0.35:
                        img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
                        cv2.putText(img, str("please correct posture"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                                    (255, 0, 0), 5)
                        cv2.imshow("Image", img)
                        f = open('data.json')
                        # data = json.load(f)
                        # x = data[18]
                        # y18 = json.dumps(x)
                        # client.publish("ebrain/DialogEngine1/interaction", y18)
                        print(difference)

                    else:

                        cv2.imshow("Image", img)

                cv2.waitKey(1)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break

        cap.release()
        cv2.destroyAllWindows()


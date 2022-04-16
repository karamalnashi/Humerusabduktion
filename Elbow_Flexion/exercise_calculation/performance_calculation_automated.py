import cv2
import numpy as np
import paho.mqtt.client as mqttclient
import pyttsx3
import json
import Pose_Module as pm
import os
detector = pm.poseDetector()



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
        frameeWidth = framee.shape[1]
        frameeHeight = framee.shape[0]
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
        f = open('data.json')
        data = json.load(f)
        i = data[9]
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

            if message.topic == "ebrain/end":
                self.stop_mqtt()
                self.end_While=True

            self.convert_To_Voice(msg)

#####################################     CLASS TRIEN   ###############################################################################################

class trien(Mqtt):
    count,  back, u, x, z = 0, 0,0, 0, 1
    per, dir,bar, color=0,0,0,(0, 255, 0)
    t, t1, t2, t3, t4, t5, t6, t7 = 100, 100, 100, 100, 100, 100, 100, 100 #In order to avoid re-sending messages
    AngelPatientSituation =0
    f = open(r"../precalibration/test1.txt", "r")
    minimum = min(f)
    value_min = int(minimum.replace(',', ''))
    # Maximum value
    f = open(r"../precalibration/test1.txt", "r")
    maximum = max(f)
    value_max = int(maximum.replace(',', ''))
    value_max = value_max + 10
    f.close()


    def __init__(self, mqtt_start: bool = False, def_triener: bool = False, mqtt_host: str = "localhost",
                 mqtt_port: int = 1883, mqtt_user: str = "mqtt", mqtt_password: str = "test",
                 mqtt_keep_alive: int = 60,exercise_number="",side="",count="",patient_movement_range=""):

        super(trien,self).__init__()
        self.side=side
        self.exercise_number=exercise_number
        self.count_Pa=int(count)
        self.patient_movement_range=float(patient_movement_range)
        print(self.side)
        print(self.exercise_number)
        print(self.count_Pa)
        print(self.patient_movement_range)

        if def_triener:
            self.start_mqtt()
            self.TrienerLoop()

        # حسبهن بالنسبه للمانيموم والماكسموم
        if self.patient_movement_range == 0.25:
            self.AngelPatientSituation = 33
        elif self.patient_movement_range == 0.5:
            self.AngelPatientSituation = 45
        elif self.patient_movement_range == 0.75:
            self.AngelPatientSituation = 58
        elif self.patient_movement_range == 1:
            self.AngelPatientSituation = 72

    def TrienerLoop(self):
        while (True):
            success, img = self.cap.read()
            img = cv2.resize(img, (1280, 720))
            # img = cv2.imread("AiTrainer/test.jpg")
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if self.side == "left":
                calculation_Points_P1=13
                calculation_Points_P2=11
                calculation_Points_P3=23
            elif self.side == "right":
                calculation_Points_P1=14
                calculation_Points_P2=12
                calculation_Points_P3=24
            else:
                print("There is no hand Side")
            ### Beginning of training
            if len(lmList) != 0:
                angle, difference, position = detector.findAngle(img, calculation_Points_P1, calculation_Points_P2,
                                                                 calculation_Points_P3)
                self.count_Calculator(angle)

                if self.end_While == True:
                    self.stop_mqtt()
                    break
                if self.count == self.count_Pa:
                    self.stop_Ubung()
                    break
                # ###################### # ######################
                if self.patient_movement_range == 1:
                    if angle > 75:
                        self.ang(img)

                    elif angle < 65:
                        if angle < 25 and self.back == 1:
                            self.ang1(img)
                        elif angle < 65 and self.back == 0:
                            self.ang2(img)

                    elif 65 < angle < 70 and self.back == 0:
                        self.ang3(img)

                    elif 70 < angle <= 75 and self.back == 0:
                        self.ang4(img)

                    # ///////////Wenn der Patient nicht alleine trainieren kann///////////
                else:
                    if angle < 25 and self.back == 1:
                        self.ang5(img)
                    elif angle < 25 and self.back == 0:
                        self.ang6(img)
                    elif angle > 70:
                        self.ang7(img)
                    elif self.AngelPatientSituation - 5 < angle < self.AngelPatientSituation and self.back == 0:
                        self.ang8(img)
                    elif self.AngelPatientSituation < angle < self.AngelPatientSituation + 5 and self.back == 0:
                        self.ang9()

                # -------------------------------------------------------------------
                self.draw(img)

                if difference > 0.35:
                    self.differenceErorr(img,difference)
                else:
                    cv2.imshow("Image", img)

            else:
                print("keinee")


        self.cap.release()
        cv2.destroyAllWindows()

    def count_Calculator(self,angle):
        self.per = np.interp(angle, (self.value_min, self.value_max), (0, 100))
        self.bar = np.interp(angle, (self.value_min, self.value_max), (650, 100))
        self.color = (255, 0, 255)

        # # Left Arm
        if self.per == 100:
            self.color = (0, 255, 0)
            if self.dir == 0:
                self.count = self.count + 0.5
                self.dir = 1
        elif self.per == 0:
            self.color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0

     # if patientSituation == 1 and angle > 75
    def ang(self,img):
        img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
        cv2.putText(img, str("Bitte bewege deine linke Hand nach unten"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[1]
        y = json.dumps(x)
        if self.t > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t = 0
        else:
            self.t = self.t + 1
            print(self.t)
        self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7= 100, 100, 100, 100, 100, 100, 100
        self.back = 1

    # if patientSituation == 1 and angle < 25 and back == 1
    def ang1(self,img):
        cv2.putText(img, str("Danke"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        f = open('data.json')
        data = json.load(f)
        x = data[7]
        y = json.dumps(x)
        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
        cv2.imshow("Image", img)
        self.back = 0

    # if patientSituation == 1 and angle < 65 and back == 0
    def ang2(self,img):
        # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
        cv2.putText(img, str("Bitte bewege deine Hand nach oben"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[0]
        y = json.dumps(x)
        if self.t1 > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t1 = 0
        else:
            self.t1 = self.t1 + 1
            print(self.t1)
        self.t, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7 = 100, 100, 100, 100, 100, 100, 100

    # if patientSituation == 1 and 65 < angle < 70 and back == 0
    def ang3(self,img):
        # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
        cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[2]
        y = json.dumps(x)
        if self.t2 > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t2 = 0
        else:
            self.t2 = self.t2 + 1
            print(self.t2)
        self.t, self.t1, self.t3, self.t4, self.t5, self.t6, self.t7 = 100, 100, 100, 100, 100, 100,100

    # if patientSituation == 1 and 70 < angle<= 75 and back == 0
    def ang4(self,img):
        cv2.putText(img, str("noch einen Moment da bleiben und dabei entspannen"),
                    (20, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[3]
        y = json.dumps(x)
        if self.t3 > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t3 = 0
        else:
            self.t3 = self.t3 + 1
            print(self.t3)
        self.t, self.t1, self.t2, self.t4, self.t5, self.t6, self.t7 = 100, 100, 100, 100, 100, 100, 100
        self.back = 1

    # if patientSituation != 1 and angle < 25 and back == 1
    def ang5(self,img):
        cv2.putText(img, str("Danke"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        f = open('data.json')
        data = json.load(f)
        x = data[7]
        y = json.dumps(x)
        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
        cv2.imshow("Image", img)
        self.back = 0

    # if patientSituation != 1 and angle < 25 and back == 0
    def ang6(self,img):
        cv2.putText(img, str("Bitte bewege deine Hand nach oben"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[0]
        y = json.dumps(x)
        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)

    # if patientSituation != 1 and angle > 70
    def ang7(self,img):
        img = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
        cv2.putText(img, str("Bitte bewege deine  Hand nach unten"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[1]
        y = json.dumps(x)
        if self.t4 > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t4 = 0
        else:
            self.t4 = self.t4 + 1
            print(self.t4)
        self.t, self.t1, self.t2, self.t3, self.t5, self.t6, self.t7 = 100, 100, 100, 100, 100, 100, 100
        self.back = 1

    # if patientSituation != 1  AngelPatientSituation - 5 < angle < AngelPatientSituation and back==0
    def ang8(self,img):
        # img = cv2.applyColorMap(img, cv2.COLORMAP_DEEPGREEN)
        cv2.putText(img, str("und noch etwas weiter"), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        self.u = 0
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[2]
        y = json.dumps(x)
        if self.t5 > 99:
            self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
            self.t5 = 0
        else:
            self.t5 =self.t5 + 1
            print(self.t5)
        self.t, self.t1, self.t2, self.t3, self.t4, self.t6, self.t7 = 100, 100, 100, 100, 100, 100, 100

    # if patientSituation != 1  AngelPatientSituation < angle < AngelPatientSituation + 5 and back==0
    def ang9(self):
        j = 30
        while j >= 0 and self.u == 0:
            ret, img = self.cap.read()
            img = cv2.resize(img, (1280, 720))
            if j > 10:

                cv2.putText(img, str("Gut,und noch etwas weiter, wenn es geht"),
                            (20, 50),
                            cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)
                cv2.putText(img, str(j // 10), (250, 250), cv2.FONT_HERSHEY_PLAIN, 15,
                            (255, 255, 255),
                            10,
                            cv2.LINE_AA)
                f = open('data.json')
                data = json.load(f)
                x = data[5]
                y = json.dumps(x)
                if self.t6 > 99:
                    self._mqtt_cleint.publish("ebrain/vDialogEngine1/interaction", y)
                    self.t6 = 0
                else:
                    self.t6 = self.t6 + 1
                self.t, self.t1, self.t2, self.t3, self.t5, self.t4, self.t7 = 100, 100, 100, 100, 100, 100, 100
            elif j <= 9:

                cv2.putText(img, str("Ihr Helfer darf jetzt den Rest ergaenzen"),
                            (20, 50),
                            cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)
                f = open('data.json')
                data = json.load(f)
                x = data[4]
                y = json.dumps(x)
                if self.t7 > 99:
                    self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
                    self.t7 = 0
                else:
                    self.t7 = self.t7 + 1
                self.t, self.t1, self.t2, self.t3, self.t5, self.t6, self.t4 = 100, 100, 100, 100, 100, 100, 100
            cv2.imshow("Image", img)
            cv2.waitKey(125)

            j = j - 1
            if j == 0:
                self.u = 1

    def draw(self,img):
        # Draw Bar link
        cv2.rectangle(img, (1100, 100), (1175, 650), 3)
        cv2.rectangle(img, (1100, int(self.bar)), (1175, 650), self.color, cv2.FILLED)
        cv2.putText(img, f'{int(self.per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 2,
                    self.color, 4)

        # Draw Curl Count link
        # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "L: " + str(self.count), (1050, 720), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

    def differenceErorr(self,img,difference):
        img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
        cv2.putText(img, str("please correct posture"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        cv2.imshow("Image", img)
        f = open('data.json')
        data = json.load(f)
        x = data[6]
        y= json.dumps(x)
        self._mqtt_cleint.publish("ebrain/DialogEngine1/interaction", y)
        print(difference)


if __name__ == "__main__":
    print("Hello world!")
else:
    mqtt=Mqtt()



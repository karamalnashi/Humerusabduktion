import paho.mqtt.client as mqttclient
import cv2
import json
import Pose_Module as pm
from performance_calculation_automated import trien
from Control import trien_Finger

broker_address = "192.168.1.7"
#port = 1883
#broker_address = "localhost"
port = 1883
user = ""
password = ""
detector = pm.poseDetector()
class Mqtt_conniction():
    def __init__(self):

        self.layout_type=""
        self.exercise_number=""
        self.side = ""
        self.count = ""
        self.patient_movement_range = ""
        self.client1 = mqttclient.Client("MQTT")
        self.client1.on_message = self.on_message
        self.client1.username_pw_set(user,password)
        self.client1.on_connect = self.on_connect
        self.client1.connect(broker_address, port)
        self.client1.subscribe("ebrain/#")
        self.client1.loop_forever()


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
        cap.release()
        cv2.destroyAllWindows()
        return result




    def on_connect(self,client1, userdata, flags, rc):

        if rc == 0:
            print("client 1 is connected")
            client1.subscribe("ebrain/#")
            global connected
            connected = True
        else:
            print("client is error")

    def on_message(self,client1, userdata, message):
        print("message recieved 1= " + str(message.payload.decode("utf-8")))
        print("message topic 12=", message.topic)
        msg = message.payload.decode("utf-8")
        Data = json.loads(msg)
        if "content" in Data:
            self.layout_type=Data["content"]["layout_type"]
            self.exercise_number = Data["content"]["abt_configuration_dict"]["exercise_number"]
            self.side = Data["content"]["abt_configuration_dict"]["side"]
            self.count = Data["content"]["abt_configuration_dict"]["count"]
            self.patient_movement_range = Data["content"]["abt_configuration_dict"]["patient_movement_range"]
            self.time_pause=Data["content"]["abt_configuration_dict"]["time_pause"]
        #print(self.side)
        if self.layout_type == "start":

            person_result = self.person_dec()
            if person_result == True:
                f = open('data.json')
                data = json.load(f)
                x = data[8]
                y = json.dumps(x)
                client1.publish("ebrain/DialogEngine1/interaction", y)
            else:
                print("es gibt kein Person")
                f = open('data.json')
                data = json.load(f)
                x = data[10]
                y = json.dumps(x)
                client1.publish("ebrain/DialogEngine1/interaction", y)


        elif self.layout_type == "ja":
            if self.exercise_number==1:
                print("erste ubung")
                t = trien(mqtt_start=True, def_triener=True,exercise_number=self.exercise_number,side=self.side,count=self.count,patient_movement_range=self.patient_movement_range, time_pause=self.time_pause)
            elif self.exercise_number==2:
                print("zweite ubung")
                t=trien_Finger(mqtt_start=True, def_triener=True,exercise_number=self.exercise_number,side=self.side,count=self.count,patient_movement_range=self.patient_movement_range)



        elif self.layout_type == "":
            print(message.topic)



mqtt=Mqtt_conniction()

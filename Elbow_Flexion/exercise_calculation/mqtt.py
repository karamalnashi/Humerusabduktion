import paho.mqtt.client as mqttclient
import cv2
import json
import Pose_Module as pm
from performance_calculation_automated import Run

broker_address = "localhost"
port = 1883
user = "mqtt"
password = "test"
run=Run()
detector = pm.poseDetector()

def person_dec():
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


def on_connect(client1, userdata, flags, rc):

    if rc == 0:
        print("client 1 is connected")
        global connected
        connected = True
    else:
        print("client is error")


def on_message(client1, userdata, message):
    print("message recieved = " + str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)

    if message.topic == "ebrain/start":

        person_result =person_dec()
        if person_result==True:
            print("ok")
            f = open('data.json')
            data = json.load(f)
            x = data[19]
            y = json.dumps(x)
            client1.publish("ebrain/DialogEngine1/interaction", y)
        else:
            print("es gibt kein Person")


    elif message.topic == "ebrain/ja":
        run.start(message.topic)


    elif message.topic == "ebrain/DialogEngine1/interaction":
        print(message.topic)





Messagerecieved = False
connected = False
client1 = mqttclient.Client("MQTT")
client1.on_message = on_message
client1.username_pw_set(user, password=password)
client1.on_connect = on_connect
client1.connect(broker_address, port=port)
client1.subscribe("ebrain/#")
client1.loop_forever()

import paho.mqtt.client as mqttclient
import cv2
import json
import time
import Pose_Module as pm
from performance_calculation_automated import Run

broker_address = "localhost"
port = 1883
user = "mqtt"
password = "test"
startStope=Run()
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



    if message.topic == "ebrain/start":
        person_result =person_dec()
        if person_result==True:
            print("okkkkkkkkkkkkk")
            f = open('data.json')
            data = json.load(f)
            x = data[19]
            y = json.dumps(x)
            client.publish("ebrain/DialogEngine1/interaction", y)
            #pass
            #time.sleep(4)
            #startStope.start(message.topic)
            #startStope.start(message.topic)
        else:
            print("neiiiiiiiiiin")


    elif message.topic == "ebrain/ja":
        startStope.start(message.topic)

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



while True :

    client.loop_start()
    client.subscribe("ebrain/#")
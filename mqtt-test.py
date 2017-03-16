import paho.mqtt.client as mqtt
import sys
import time
import random
import json

broker_add = '10.0.0.1'
sensor_name = 'sensor1'

def on_connect(mqttc, obj, flags, rc):
    print "Connected to %s:%s" % (mqttc._host, mqttc._port)

def on_message(mqttc, obj, msg):
    print "message received"
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    mqttc.disconnect()

def on_publish(mqttc, obj, mid):
    print "message published: "+str(mid)

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == '__main__':

	mqttc = mqtt.Client()

	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe

	mqttc.connect(broker_add, 1883, keepalive=60)
	mqttc.subscribe(sensor_name, 2)

	new_s_value = random.randint(1, 1000)
	new_sensor_t = {'value': str(new_s_value)}
	the_msg_str = json.dumps(new_sensor_t)
	mqttc.publish(sensor_name,the_msg_str)

	mqttc.loop_forever()

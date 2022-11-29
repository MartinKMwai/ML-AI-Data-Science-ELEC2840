import paho.mqtt.publish as publish

hostname = "test.mosquitto.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic666 = "PC000/traffic_light/emergency"
	

while True:
	emergency_status = (str)(input())
	print (emergency_status)
	publish.single(topic666, payload=(emergency_status), qos=0,
		hostname=hostname,
		port=port)

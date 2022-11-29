import paho.mqtt.publish as publish

hostname = "test.mosquitto.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic1 = "WWDITS/LAZSLO"  # '/' is used as the delimiter for sub-topics
topic2 = "WWDITS/NADJA"
topic3 = "WWDITS/NANDOR"
topic4 = "WWDITS/COLLIN ROBINSON"



publish.single(topic1, payload="Hello there, my name is Lazlo and I love topiary stuff", qos=0,
	hostname=hostname,
	port=port)

publish.single(topic2, payload="I, Nadja, left the council out of my own volition. ", qos=0,
	hostname=hostname,
	port=port)

publish.single(topic3, payload="I am Nandor the Relentless and I love pillaging stuff", qos=0,
	hostname=hostname,
	port=port)


publish.single(topic4, payload="I bore to live, I don't live to bore ", qos=0,
	hostname=hostname,
	port=port)

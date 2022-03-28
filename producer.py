import time
import json 
import requests

from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode('utf-8'))
topic_name = "binance_topic"

request = 'https://api.binance.com/api/v3/klines'
params = dict({
    'symbol':'BTCUSDT',
    'interval':'1m',
    'limit':'100'
})

while 1:
    response = rep = requests.get(request, params=params)
    data = rep.json()
    print(data)
    producer.send(topic_name, data)
    time.sleep(60)

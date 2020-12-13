from kafka import KafkaConsumer
from os import environ
from pymongo import MongoClient
import json

client = MongoClient(environ['MONGO_CONNECT'])

db = client[environ['DATABASE_NAME']]
col = db[environ['COLLECTION_NAME']]

topic_name = 'articles'
group_id = 'article_consumers'
consumer = KafkaConsumer(
    topic_name,
    group_id=group_id,
    auto_offset_reset='earliest',
    bootstrap_servers=[environ['KAFKA_BOOTSTRAP_SERVER']])

for message in consumer:
    article = json.loads(message.value.decode(encoding='utf-8'))
    key = message.key.decode(encoding='utf-8')
    article['_id'] = key
    inserted = col.replace_one({ '_id': article['_id'] }, article, upsert=True)
    print(inserted, flush=True)

consumer.close()

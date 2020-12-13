
from os import environ
from kafka import KafkaProducer
from app.models import Article

class ArticleProducer():
    "Class variable to serve each instance of this producer to avoid creating multiple connections with kafka"
    producer = KafkaProducer(bootstrap_servers=[environ['KAFKA_BOOTSTRAP_SERVER']])
    topic_name = 'articles'

    def send(self, article: Article):
        self.producer.send(self.topic_name,
            key=bytes(article.filename, encoding='utf-8'),
            value=bytes(article.dumps(), encoding='utf-8')
            )

 

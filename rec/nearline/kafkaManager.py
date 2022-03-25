from kafka import KafkaProducer
from kafka.errors import KafkaError


class KafkaManager:
    def __init__(self, server, topic):
        self._server = server
        self.producer = None
        self.topic = topic

    def connect(self):
        if self.producer is None:
            producer = KafkaProducer(bootstrap_servers=self._server)
            self.producer = producer

    def close(self):
        if self.producer is not None:
            self.producer.close()
            self.producer = None

    def send(self, msg):
        if self.producer is not None:
            if not isinstance(msg, bytes):
                msg = msg.encode("utf-8")
            try:
                f = self.producer.send(topic=self.topic, value=msg)
                f.get(timeout=10)
            except KafkaError:
                print(KafkaError)
        else:
            print("error")


def get_kafka_producer(port, topic):
    producer = KafkaManager("localhost:%d" % port, topic)
    producer.connect()
    return producer


kafkaInc = get_kafka_producer(9092, "rec3")

# get_kafka_producer(9092, "rec3").send("1,140,2021-04-18 20:05:03")
# print(get_kafka_producer(9092, "rec3"))

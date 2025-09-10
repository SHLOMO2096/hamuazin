import os

PATH = "C:\\Users\\shlomo\\Downloads\\podcasts"
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "podcasts")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BROKER_LOCALHOST_LISTENER", "localhost:9092")
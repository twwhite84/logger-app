from kafka import KafkaConsumer

SERVER: str = "aiven-homework-take-home-test.l.aivencloud.com:15556"
TOPIC_NAME: str = "default_topic"
API_VERSION: tuple[int, int, int] = (0, 10, 2)
CERTS_DIR: str = "certs"


# To read logs you can just run this file in a new terminal tab and it will poll
# Aiven Kafka for updates. Ctrl + C or Mac equivalent to shut it down
def consume() -> None:

    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=SERVER,
        security_protocol="SSL",
        ssl_cafile=f"{CERTS_DIR}/ca.pem",
        ssl_certfile=f"{CERTS_DIR}/service.cert",
        ssl_keyfile=f"{CERTS_DIR}/service.key",
        auto_offset_reset="earliest",
    )

    print("Press CTRL+C to quit")
    while True:
        for message in consumer.poll(2000).values():
            for item in message:
                print(f"{item.value.decode("utf-8")}\n")


if __name__ == "__main__":
    consume()

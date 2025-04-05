# To read logs you can just run this file in a new terminal tab and it will poll
# your Kafka service for updates. Ctrl + C or Mac equivalent to shut it down.

import sys
from kafka import KafkaConsumer


class KafkaReader:
    def __init__(self, server_url: str, topic_name: str, certs_dir: str) -> None:
        self.SERVER: str = server_url
        self.TOPIC_NAME: str = topic_name
        self.CERTS_DIR: str = certs_dir
        self.API_VERSION: tuple[int, int, int] = (0, 10, 2)

    def consume(self) -> None:
        consumer = KafkaConsumer(
            self.TOPIC_NAME,
            bootstrap_servers=self.SERVER,
            security_protocol="SSL",
            ssl_cafile=f"{self.CERTS_DIR}/ca.pem",
            ssl_certfile=f"{self.CERTS_DIR}/service.cert",
            ssl_keyfile=f"{self.CERTS_DIR}/service.key",
            auto_offset_reset="earliest",
        )

        print("Press CTRL+C to quit")
        while True:
            for message in consumer.poll(2000).values():
                for item in message:
                    print(f"{item.value.decode("utf-8")}\n")


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv) > 4:
        print("ERROR: INCORRECT ARGUMENTS")
        print("Use this pattern: KafkaReader.py <server_url> <topic_name> <certs_dir>")
    else:
        server_url: str = sys.argv[1]
        topic_name: str = sys.argv[2]
        certs_dir: str = sys.argv[3]

        try:
            kafka_reader = KafkaReader(server_url, topic_name, certs_dir)
        except Exception as ex:
            print(f"ERROR: \n{ex}")
            sys.exit(1)

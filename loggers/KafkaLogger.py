from kafka import KafkaProducer
from ILogger import ILogger, StatusType
from typing import Dict
import datetime


class KafkaLogger(ILogger):
    # API version has been set at 0.12.2, app doesn't work for me without specifying it
    # According to below StackOverlow site, 0.12.2 is a baseline for compatibility
    # https://stackoverflow.com/questions/57076780/how-to-determine-api-version-of-kafka

    def __init__(self, server_url: str, topic_name: str, certs_dir: str) -> None:
        self.SERVER: str = server_url
        self.TOPIC_NAME: str = topic_name
        self.CERTS_DIR: str = certs_dir
        self.API_VERSION: tuple[int, int, int] = (0, 10, 2)

        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.SERVER,
                security_protocol="SSL",
                ssl_cafile=f"{self.CERTS_DIR}/ca.pem",
                ssl_certfile=f"{self.CERTS_DIR}/service.cert",
                ssl_keyfile=f"{self.CERTS_DIR}/service.key",
                api_version=self.API_VERSION,
            )
        except Exception as ex:
            raise Exception("COULD NOT CREATE KAFKA PRODUCER", ex)

        self.count: int = 0

    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        try:
            output: str = str(f"time: \t\t{datetime.datetime.now()}")
            for key in logdata.keys():
                output += (
                    f"\n{key}:\t\t{logdata[key]}"
                    if key in ["url", "error", "regex"]
                    else f"\n{key}:\t{logdata[key]}"
                )

            output_bytes = output.encode()
            self.producer.send("default_topic", output_bytes)
            self.producer.flush()

        except Exception as ex:
            raise Exception("COULD NOT SEND TO LOGGER", ex)

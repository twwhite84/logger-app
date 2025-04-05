from abc import ABCMeta, abstractmethod
from typing import Dict
from enum import Enum
from colored import Fore, Style
from kafka import KafkaProducer
import datetime


class StatusType(Enum):
    SUCCESS = 1
    WARNING = 2
    FAILURE = 3


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        pass


class ConsoleLogger(ILogger):
    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        if status_type == StatusType.SUCCESS:
            print(Fore.green)
        elif status_type == StatusType.FAILURE:
            print(Fore.red)

        print(f"time: \t\t{datetime.datetime.now()}")
        for key in logdata.keys():
            (
                print(f"{key}:\t\t{logdata[key]}")
                if key in ["url", "error", "regex"]
                else print(f"{key}:\t{logdata[key]}")
            )
        print(Style.reset)
        print(
            "--------------------------------------------------------------------------------"
        )


class DiskLogger(ILogger):
    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        output: str = str(datetime.datetime.now())
        with open("output.txt", mode="a") as f:
            for key in logdata.keys():
                output += (
                    f"\n{key}:\t\t\t{logdata[key]}"
                    if key in ["url", "error", "regex"]
                    else f"\n{key}:\t{logdata[key]}"
                )
            f.write(output + "\n\n")


class KafkaLogger(ILogger):
    # API version has been set at 0.12.2, app doesn't work for me without specifying it
    # https://stackoverflow.com/questions/57076780/how-to-determine-api-version-of-kafka

    def __init__(self) -> None:
        self.SERVER: str = "aiven-homework-take-home-test.l.aivencloud.com:15556"
        self.TOPIC_NAME: str = "default_topic"
        self.API_VERSION: tuple[int, int, int] = (0, 10, 2)
        self.CERTS_DIR: str = "certs"

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

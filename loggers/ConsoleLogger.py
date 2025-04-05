from ILogger import ILogger, StatusType
from colored import Fore, Style
from typing import Dict
import datetime


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

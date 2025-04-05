from ILogger import ILogger, StatusType
from typing import Dict
import datetime


class DiskLogger(ILogger):
    def __init__(self, log_dir: str):
        self.log_dir = log_dir

    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        output: str = str(datetime.datetime.now())
        with open(f"{self.log_dir}/output.txt", mode="a") as f:
            for key in logdata.keys():
                output += (
                    f"\n{key}:\t\t\t{logdata[key]}"
                    if key in ["url", "error", "regex"]
                    else f"\n{key}:\t{logdata[key]}"
                )
            f.write(output + "\n\n")

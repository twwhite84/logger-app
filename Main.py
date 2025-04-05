import sys
import threading
import time
import requests
from typing import List, Dict, Union, cast
from Loggers import *
from ConfigReader import ConfigReader
import re


def pingSite(
    site: Dict[str, Union[str | None]],
    loggers: List[ILogger],
    lock: threading.Lock,
    period: int,
) -> None:
    while True:
        time.sleep(period)
        url: str = cast(str, site["url"])
        regex: Union[str | None] = site["regex"]
        logdata: Dict[str, str] = {}
        try:
            r = requests.get(url, timeout=3)

            # check response text against optional regex
            if regex:
                if not re.fullmatch(regex, r.text):
                    raise ValueError("RESPONSE BODY INVALID BY REGEX")

            logdata = {
                "url": url,
                "regex": regex if regex else "None",
                "response_time": str(round(r.elapsed.microseconds / 1_000_000, 3))
                + "s",
                "status_code": str(r.status_code),
            }
            with lock:
                for logger in loggers:
                    logger.log(logdata, StatusType.SUCCESS)

        # log any error
        except Exception as ex:
            try:
                logdata = {
                    "url": url,
                    "regex": regex if regex else "None",
                    "error": str(*ex.args),
                }
                with lock:
                    for logger in loggers:
                        logger.log(logdata, StatusType.FAILURE)
            except Exception as ex:
                raise Exception(ex)


def main() -> None:
    try:
        # validate config file
        if len(sys.argv) <= 1:
            raise ValueError("PLEASE SPECIFY A JSON CONFIG FILE AS ARGUMENT")
        filename: str = sys.argv[1]
        cr: ConfigReader = ConfigReader()
        cr.load(filename)
        sites: List[Dict[str, Union[str | None]]] = cr.getSites()

        # set up loggers
        lock: threading.Lock = threading.Lock()
        threads: list[threading.Thread] = []
        freq_s: int = 10
        loggers: List[ILogger] = [ConsoleLogger()]

        # start check cycle and logging
        for site in sites:
            threads.append(
                threading.Thread(target=pingSite, args=[site, loggers, lock, freq_s])
            )
            threads[-1].start()

    except Exception as ex:
        print(*ex.args)
        quit()


if __name__ == "__main__":
    main()

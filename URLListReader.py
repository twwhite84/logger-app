import json
import jsonschema
import jsonschema.exceptions
import validators
from typing import cast, List, Dict, Union


class URLError(ValueError):
    def __init__(self, url: str) -> None:
        super().__init__(url)


class URLListReader:
    def __init__(self) -> None:
        self.sites: List[Dict[str, Union[str | None]]] = []
        self.schema = {
            "type": "object",
            "properties": {
                "sites": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "url": {"type": "string"},
                                    "regex": {"type": "string"},
                                },
                                "required": ["url"],
                            }
                        ]
                    },
                }
            },
            "required": ["sites"],
        }

    def getSites(self) -> List[Dict[str, Union[str | None]]]:
        return self.sites

    def load(self, filename: str) -> None:
        validator = jsonschema.Draft4Validator(schema=self.schema)

        try:

            with open(filename) as f:

                # open and decode the config file, validating against json schema
                decoded = json.load(f)
                validator.validate(decoded)

                # validate the url
                sites: List[Dict[str, str]] = cast(
                    List[Dict[str, str]], decoded["sites"]
                )
                for site in sites:
                    url = site["url"].strip()
                    if not (validators.url(url)):
                        raise URLError(url)

                    if "regex" in site.keys():
                        regex = site["regex"]
                        self.sites.append({"url": url, "regex": regex})
                    else:
                        self.sites.append({"url": url, "regex": None})

        except FileNotFoundError as ex:
            raise Exception("CONFIG FILE ERROR: FILE NOT FOUND\n", ex)

        except jsonschema.exceptions.ValidationError as ex:
            raise Exception("CONFIG FILE ERROR: INVALID SCHEMA\n", ex)

        except URLError as ex:
            raise Exception("CONFIG FILE ERROR: INVALID URL\n", ex)

        except Exception as ex:
            raise Exception(ex)

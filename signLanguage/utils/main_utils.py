import os
import sys
import yaml

from signLanguage.exception import SignException
from signLanguage.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as yaml_file:
            logging.info(f"Reading YAML file: {file_path}")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise SignException(e, sys) from e


def write_yaml_file(
    file_path: str,
    content: object,
    replace: bool = False
) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(file_path, "w") as yaml_file:
            yaml.dump(
                content,
                yaml_file,
                default_flow_style=False
            )

        logging.info(f"YAML file written successfully: {file_path}")

    except Exception as e:
        raise SignException(e, sys) from e
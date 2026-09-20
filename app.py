import sys

from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.pipeline.training_pipeline import TrainPipeline


def main():

    try:

        logging.info(
            "Application started."
        )

        pipeline = TrainPipeline()

        pipeline.run_pipeline()

        logging.info(
            "Application completed successfully."
        )

    except Exception as e:

        logging.error(
            f"Application failed: {e}"
        )

        raise SignException(e, sys) from e


if __name__ == "__main__":
    main()
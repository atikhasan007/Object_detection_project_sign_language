import sys

from signLanguage.exception import SignException
from signLanguage.logger import logging

from signLanguage.pipeline.training_pipeline import TrainPipeline


def main():

    try:

        logging.info(
            "================================================"
        )
        logging.info(
            "Application started."
        )
        logging.info(
            "================================================"
        )

        # Create Training Pipeline
        pipeline = TrainPipeline()

        logging.info(
            "TrainPipeline object created successfully."
        )

        # Run complete pipeline
        pipeline.run_pipeline()

        logging.info(
            "================================================"
        )
        logging.info(
            "Application completed successfully."
        )
        logging.info(
            "================================================"
        )

    except Exception as e:

        logging.error(
            "================================================"
        )

        logging.error(
            f"Application failed: {e}"
        )

        logging.error(
            "================================================"
        )

        raise SignException(e, sys) from e


if __name__ == "__main__":
    main()
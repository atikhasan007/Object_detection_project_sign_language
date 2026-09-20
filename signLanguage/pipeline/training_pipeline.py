import sys

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.components.data_ingestion import DataIngestion

from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifacts_entity import DataIngestionArtifact


class TrainPipeline:

    def __init__(self):

        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:

            logging.info(
                "Entered the start_data_ingestion method "
                "of TrainPipeline class"
            )

            logging.info(
                "Starting data ingestion..."
            )

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info(
                "Data ingestion completed successfully."
            )

            logging.info(
                "Exited the start_data_ingestion method "
                "of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:

            logging.error(
                f"Data ingestion pipeline failed: {e}"
            )

            raise SignException(e, sys) from e

    def run_pipeline(self) -> None:

        try:

            logging.info(
                "========== Training Pipeline Started =========="
            )

            data_ingestion_artifact = (
                self.start_data_ingestion()
            )

            logging.info(
                f"Data Ingestion Artifact: "
                f"{data_ingestion_artifact}"
            )

            logging.info(
                "========== Training Pipeline Completed =========="
            )

        except Exception as e:

            logging.error(
                f"Training pipeline failed: {e}"
            )

            raise SignException(e, sys) from e
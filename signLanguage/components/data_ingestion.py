import os
import sys

import gdown
from zipfile import ZipFile, BadZipFile

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:

    def __init__(
        self,
        data_ingestion_config: DataIngestionConfig = None
    ):
        try:

            if data_ingestion_config is None:
                data_ingestion_config = DataIngestionConfig()

            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SignException(e, sys) from e

    # ---------------------------------------------------------
    # Download Dataset
    # ---------------------------------------------------------
    def download_data(self) -> str:

        try:

            dataset_url = (
                self.data_ingestion_config.data_download_url
            )

            logging.info(
                f"Dataset URL received: {repr(dataset_url)}"
            )

            # Check URL
            if not dataset_url or not dataset_url.strip():

                raise ValueError(
                    "DATA_DOWNLOAD_URL is empty. "
                    "Please check "
                    "signLanguage/constant/training_pipeline.py"
                )

            # Create download directory
            zip_download_dir = (
                self.data_ingestion_config.data_ingestion_dir
            )

            os.makedirs(
                zip_download_dir,
                exist_ok=True
            )

            # Dataset file path
            zip_file_path = os.path.join(
                zip_download_dir,
                "dataset.zip"
            )

            logging.info(
                f"Dataset will be downloaded to: "
                f"{zip_file_path}"
            )

            # Remove old file if exists
            if os.path.exists(zip_file_path):

                logging.info(
                    "Old dataset.zip found. Removing it..."
                )

                os.remove(zip_file_path)

            # -------------------------------------------------
            # Google Drive Download
            # -------------------------------------------------

            logging.info(
                "Starting Google Drive dataset download..."
            )

            gdown.download(
                url=dataset_url,
                output=zip_file_path,
                quiet=False
            )

            # -------------------------------------------------
            # Check downloaded file
            # -------------------------------------------------

            if not os.path.exists(zip_file_path):

                raise FileNotFoundError(
                    "Dataset download failed. "
                    f"File was not created: {zip_file_path}"
                )

            file_size = os.path.getsize(
                zip_file_path
            )

            if file_size == 0:

                raise ValueError(
                    "Downloaded dataset.zip is empty."
                )

            logging.info(
                f"Dataset downloaded successfully."
            )

            logging.info(
                f"Dataset path: {zip_file_path}"
            )

            logging.info(
                f"Dataset size: {file_size} bytes"
            )

            return zip_file_path

        except Exception as e:

            logging.error(
                f"Error occurred while downloading dataset: {e}"
            )

            raise SignException(
                e,
                sys
            ) from e

    # ---------------------------------------------------------
    # Extract ZIP File
    # ---------------------------------------------------------
    def extract_zip_file(
        self,
        zip_file_path: str
    ) -> str:

        try:

            feature_store_path = (
                self.data_ingestion_config
                .feature_store_file_path
            )

            # Create feature store directory
            os.makedirs(
                feature_store_path,
                exist_ok=True
            )

            logging.info(
                f"Preparing to extract: {zip_file_path}"
            )

            # Check ZIP exists
            if not os.path.exists(zip_file_path):

                raise FileNotFoundError(
                    f"ZIP file not found: "
                    f"{zip_file_path}"
                )

            # Check extension
            if not zip_file_path.lower().endswith(".zip"):

                raise ValueError(
                    f"Downloaded file is not a ZIP file: "
                    f"{zip_file_path}"
                )

            logging.info(
                f"Extracting dataset into: "
                f"{feature_store_path}"
            )

            # Extract ZIP
            with ZipFile(
                zip_file_path,
                "r"
            ) as zip_ref:

                zip_ref.extractall(
                    feature_store_path
                )

            logging.info(
                "Dataset extracted successfully."
            )

            logging.info(
                f"Feature store path: "
                f"{feature_store_path}"
            )

            return feature_store_path

        except BadZipFile as e:

            logging.error(
                "Downloaded file is not a valid ZIP file."
            )

            raise SignException(
                "Downloaded file is not a valid ZIP file. "
                "Please check your Google Drive dataset.",
                sys
            ) from e

        except Exception as e:

            logging.error(
                f"Error occurred while extracting dataset: {e}"
            )

            raise SignException(
                e,
                sys
            ) from e

    # ---------------------------------------------------------
    # Initiate Data Ingestion
    # ---------------------------------------------------------
    def initiate_data_ingestion(
        self
    ) -> DataIngestionArtifact:

        logging.info(
            "Entered initiate_data_ingestion method "
            "of DataIngestion class."
        )

        try:

            # Step 1: Download dataset
            zip_file_path = (
                self.download_data()
            )

            # Step 2: Extract dataset
            feature_store_path = (
                self.extract_zip_file(
                    zip_file_path
                )
            )

            # Step 3: Create artifact
            data_ingestion_artifact = (
                DataIngestionArtifact(
                    data_zip_file_path=zip_file_path,
                    feature_store_path=feature_store_path
                )
            )

            logging.info(
                "Data ingestion completed successfully."
            )

            logging.info(
                f"Data ingestion artifact: "
                f"{data_ingestion_artifact}"
            )

            logging.info(
                "Exited initiate_data_ingestion method "
                "of DataIngestion class."
            )

            return data_ingestion_artifact

        except Exception as e:

            logging.error(
                f"Data ingestion failed: {e}"
            )

            raise SignException(
                e,
                sys
            ) from e
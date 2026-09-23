import os
import sys

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.entity.config_entity import DataValidationConfig

from signLanguage.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):

        try:

            logging.info(
                "Initializing DataValidation..."
            )

            self.data_ingestion_artifact = (
                data_ingestion_artifact
            )

            self.data_validation_config = (
                data_validation_config
            )

            logging.info(
                "DataValidation initialized successfully."
            )

        except Exception as e:

            raise SignException(e, sys) from e

    # ============================================================
    # VALIDATE FILES
    # ============================================================

    def validate_all_files_exist(self) -> bool:

        try:

            logging.info(
                "Entered validate_all_files_exist method."
            )

            # ----------------------------------------------------
            # Get Feature Store Path
            # ----------------------------------------------------

            feature_store_path = (
                self.data_ingestion_artifact.feature_store_path
            )

            logging.info(
                f"Feature Store Path: {feature_store_path}"
            )

            # ----------------------------------------------------
            # Get Required Files
            # ----------------------------------------------------

            required_file_list = (
                self.data_validation_config.required_file_list
            )

            logging.info(
                f"Required Files/Folders: "
                f"{required_file_list}"
            )

            # ----------------------------------------------------
            # Check Feature Store Directory
            # ----------------------------------------------------

            if not os.path.exists(feature_store_path):

                raise FileNotFoundError(
                    f"Feature store path does not exist: "
                    f"{feature_store_path}"
                )

            # ----------------------------------------------------
            # Get Extracted Files/Folders
            # ----------------------------------------------------

            all_files = os.listdir(
                feature_store_path
            )

            logging.info(
                "================================================"
            )

            logging.info(
                "EXTRACTED FILES/FOLDERS:"
            )

            for file_name in all_files:

                logging.info(
                    f"FOUND IN FEATURE STORE: {file_name}"
                )

            logging.info(
                "================================================"
            )

            # ----------------------------------------------------
            # Validate Required Files
            # ----------------------------------------------------

            validation_status = True

            logging.info(
                "Starting required file validation..."
            )

            for file_name in required_file_list:

                file_path = os.path.join(
                    feature_store_path,
                    file_name
                )

                if os.path.exists(file_path):

                    logging.info(
                        f"REQUIRED ITEM FOUND: {file_name}"
                    )

                else:

                    logging.error(
                        f"REQUIRED ITEM MISSING: {file_name}"
                    )

                    validation_status = False

            # ----------------------------------------------------
            # Validation Result
            # ----------------------------------------------------

            logging.info(
                "================================================"
            )

            logging.info(
                f"FINAL VALIDATION STATUS: "
                f"{validation_status}"
            )

            logging.info(
                "================================================"
            )

            # ----------------------------------------------------
            # Create Validation Directory
            # ----------------------------------------------------

            os.makedirs(
                self.data_validation_config.data_validaton_dir,
                exist_ok=True
            )

            logging.info(
                f"Validation directory created: "
                f"{self.data_validation_config.data_validaton_dir}"
            )

            # ----------------------------------------------------
            # Create Status File
            # ----------------------------------------------------

            with open(
                self.data_validation_config.valid_status_file_dir,
                "w"
            ) as file:

                file.write(
                    f"validation_status: "
                    f"{validation_status}"
                )

            logging.info(
                f"Validation status file created: "
                f"{self.data_validation_config.valid_status_file_dir}"
            )

            return validation_status

        except Exception as e:

            logging.error(
                f"File validation failed: {e}"
            )

            raise SignException(e, sys) from e

    # ============================================================
    # INITIATE DATA VALIDATION
    # ============================================================

    def initiate_data_validation(
        self
    ) -> DataValidationArtifact:

        try:

            logging.info(
                "================================================"
            )

            logging.info(
                "Entered initiate_data_validation method."
            )

            # ----------------------------------------------------
            # Validate Dataset
            # ----------------------------------------------------

            status = (
                self.validate_all_files_exist()
            )

            logging.info(
                f"Data Validation Result: {status}"
            )

            # ----------------------------------------------------
            # Create Data Validation Artifact
            # ----------------------------------------------------

            data_validation_artifact = (
                DataValidationArtifact(
                    validation_status=status
                )
            )

            logging.info(
                f"Data Validation Artifact created: "
                f"{data_validation_artifact}"
            )

            # ----------------------------------------------------
            # Final Validation Result
            # ----------------------------------------------------

            if status:

                logging.info(
                    "Data validation completed successfully."
                )

            else:

                logging.warning(
                    "Data validation failed."
                )

            # ----------------------------------------------------
            # Exit
            # ----------------------------------------------------

            logging.info(
                "Exited initiate_data_validation method."
            )

            return data_validation_artifact

        except Exception as e:

            logging.error(
                f"Data Validation failed: {e}"
            )

            raise SignException(e, sys) from e
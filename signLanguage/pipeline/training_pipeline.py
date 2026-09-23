import sys

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.components.data_ingestion import DataIngestion
from signLanguage.components.data_validation import DataValidation

from signLanguage.components.model_trainer import ModelTrainer

from signLanguage.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

from signLanguage.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)


class TrainPipeline:

    def __init__(self):
        try:

            logging.info(
                "Initializing TrainPipeline..."
            )

            self.data_ingestion_config = DataIngestionConfig()

            self.data_validation_config = DataValidationConfig()

            self.model_trainer_config = ModelTrainerConfig()

            logging.info(
                "TrainPipeline initialized successfully."
            )

        except Exception as e:

            logging.error(
                f"Error while initializing TrainPipeline: {e}"
            )

            raise SignException(e, sys) from e

    # =========================================================
    # DATA INGESTION
    # =========================================================

    def start_data_ingestion(
        self
    ) -> DataIngestionArtifact:

        try:

            logging.info(
                "Entered start_data_ingestion method."
            )

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            logging.info(
                "DataIngestion object created successfully."
            )

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info(
                "Data Ingestion completed successfully."
            )

            logging.info(
                f"Data Ingestion Artifact: "
                f"{data_ingestion_artifact}"
            )

            return data_ingestion_artifact

        except Exception as e:

            logging.error(
                f"Data Ingestion failed: {e}"
            )

            raise SignException(e, sys) from e

    # =========================================================
    # DATA VALIDATION
    # =========================================================

    def start_data_validation(
        self,
        data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:

        try:

            logging.info(
                "Entered start_data_validation method."
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            logging.info(
                "DataValidation object created successfully."
            )

            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )

            logging.info(
                "Data Validation completed successfully."
            )

            logging.info(
                f"Data Validation Artifact: "
                f"{data_validation_artifact}"
            )

            return data_validation_artifact

        except Exception as e:

            logging.error(
                f"Data Validation failed: {e}"
            )

            raise SignException(e, sys) from e

    # =========================================================
    # MODEL TRAINER
    # =========================================================

    def start_model_trainer(self) -> ModelTrainerArtifact:

        try:

            logging.info(
                "Entered start_model_trainer method."
            )

            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config
            )

            logging.info(
                "ModelTrainer object created successfully."
            )

            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )

            logging.info(
                "Model Training completed successfully."
            )

            logging.info(
                f"Model Trainer Artifact: "
                f"{model_trainer_artifact}"
            )

            return model_trainer_artifact

        except Exception as e:

            logging.error(
                f"Model Training failed: {e}"
            )

            raise SignException(e, sys) from e

    # =========================================================
    # RUN PIPELINE
    # =========================================================

    def run_pipeline(self) -> None:

        try:

            logging.info(
                "================================================"
            )

            logging.info(
                "TRAINING PIPELINE STARTED"
            )

            logging.info(
                "================================================"
            )

            # =================================================
            # STEP 1: DATA INGESTION
            # =================================================

            logging.info(
                "STEP 1: Starting Data Ingestion..."
            )

            data_ingestion_artifact = (
                self.start_data_ingestion()
            )

            logging.info(
                "STEP 1: Data Ingestion completed."
            )

            logging.info(
                f"Data Ingestion Artifact: "
                f"{data_ingestion_artifact}"
            )

            # =================================================
            # STEP 2: DATA VALIDATION
            # =================================================

            logging.info(
                "STEP 2: Starting Data Validation..."
            )

            data_validation_artifact = (
                self.start_data_validation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            logging.info(
                "STEP 2: Data Validation completed."
            )

            logging.info(
                f"Data Validation Artifact: "
                f"{data_validation_artifact}"
            )

            # =================================================
            # STEP 3: MODEL TRAINING
            # =================================================

            logging.info(
                "STEP 3: Checking Data Validation Status..."
            )

            logging.info(
                f"Validation status = "
                f"{data_validation_artifact.validation_status}"
            )

            if data_validation_artifact.validation_status:

                logging.info(
                    "STEP 3: Starting Model Training..."
                )

                model_trainer_artifact = (
                    self.start_model_trainer()
                )

                logging.info(
                    "STEP 3: Model Training completed."
                )

                logging.info(
                    f"Model Trainer Artifact: "
                    f"{model_trainer_artifact}"
                )

            else:

                logging.error(
                    "Data validation failed. "
                    "Model training will not start."
                )

                raise SignException(
                    "Data validation failed. "
                    "The data is not in the correct format.",
                    sys
                )

            # =================================================
            # PIPELINE COMPLETED
            # =================================================

            logging.info(
                "================================================"
            )

            logging.info(
                "TRAINING PIPELINE COMPLETED"
            )

            logging.info(
                "================================================"
            )

        except Exception as e:

            logging.error(
                "================================================"
            )

            logging.error(
                f"Training Pipeline failed: {e}"
            )

            logging.error(
                "================================================"
            )

            raise SignException(e, sys) from e
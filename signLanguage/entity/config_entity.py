import os
from dataclasses import dataclass, field
from datetime import datetime

from signLanguage.constant.training_pipeline import (
    ARTIFACTS_DIR,
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_FEATURE_STORE_DIR,
    DATA_DOWNLOAD_URL,
    DATA_VALIDATION_DIR_NAME,
    DATA_VALIDATION_STATUS_FILE,
    DATA_VALIDATION_ALL_REQUIRED_FILES,
    MODEL_TRAINER_BATCH_SIZE,
    MODEL_TRAINER_DIR_NAME,
    MODEL_TRAINER_NO_EPOCHS,
    MODEL_TRAINER_PRETRAINED_WEIGHT_NAME
)


TIMESTAMP: str = datetime.now().strftime(
    "%m_%d_%Y_%H_%M_%S"
)


@dataclass
class TrainingPipelineConfig:

    artifacts_dir: str = os.path.join(
        ARTIFACTS_DIR,
        TIMESTAMP
    )


training_pipeline_config = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:

    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir,
        DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir,
        DATA_INGESTION_FEATURE_STORE_DIR
    )

    data_download_url: str = DATA_DOWNLOAD_URL


@dataclass
class DataValidationConfig:

    data_validaton_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir,
        DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_dir: str = os.path.join(
        data_validaton_dir,
        DATA_VALIDATION_STATUS_FILE
    )

    required_file_list: list = field(
        default_factory=lambda:
        DATA_VALIDATION_ALL_REQUIRED_FILES.copy()
    )


@dataclass
class ModelTrainerConfig:

    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir,
        MODEL_TRAINER_DIR_NAME
    )

    weight_name: str = MODEL_TRAINER_PRETRAINED_WEIGHT_NAME

    no_epoch: int = MODEL_TRAINER_NO_EPOCHS

    batch_size: int = MODEL_TRAINER_BATCH_SIZE
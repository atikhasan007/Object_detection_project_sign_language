ARTIFACTS_DIR: str = "artifacts"

# Data Ingestion constants
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

# Google Drive file ID
DATA_DOWNLOAD_URL: str = (
    "https://drive.google.com/uc?export=download&id="
    "1X9UN-R6-OG_EJ_RrkAbJCV0V22Ubokds"
)


"""
Data Validation related constants start with DATA_VALIDATION
"""

DATA_VALIDATION_DIR_NAME = "data_validation"

DATA_VALIDATION_STATUS_FILE = "status.txt"

DATA_VALIDATION_ALL_REQUIRED_FILES = [
    "train",
    "test",
    "valid",
    "data.yaml"
]
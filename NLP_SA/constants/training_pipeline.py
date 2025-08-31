import os

# --------------------------------- Common Constants and Variables ---------------------------------

"""
Defining COMMON CONSTANT VARIABLES FOR TRAINING PIPELINE
"""

TARGET_COLUMN: str = 'label'
PIPELINE_NAME: str = 'SentimentAnalysis'
ARTIFACT_DIR: str = 'artifacts'

FILE_NAME: str = 'rawdata.csv'
TRAIN_FILE_NAME: str = 'train.csv'
VAL_FILE_NAME: str = 'val.csv'
FINAL_TEST_FILE_NAME:str = 'final_test.csv'

SCHEMA_FILE_PATH: str = os.path.join('data_schema', 'schema.yaml')

SAVED_MODEL_DIR: str = os.path.join("saved_models")
MODEL_FILE_NAME: str = "model.pkl"


# ---------------------------------- Data Ingestion Constants and Directories ------------------------------

"""
DATA INGESTION related constants start with DATA_INGESTION_
"""

# S3 bucket and key for Amazon Review Full dataset
DATA_INGESTION_S3_BUCKET: str = 'fast-ai-nlp'
DATA_INGESTION_S3_KEY: str = 'amazon_review_full_csv.tgz'

# Local directories for storing intermediate data
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'             # Root directory for data ingestion artifacts
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'     # Subdir for raw CSV from extracted files
DATA_INGESTION_INGESTED_DIR: str = 'ingested'               # Subdir for train/test split data

# Paths for downloaded and extracted files
DATA_INGESTION_LOCAL_TGZ_PATH: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, 'amazon_review_full_csv.tgz')
DATA_INGESTION_RAW_DATA_DIR: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, 'amazon_review_full_csv')
#DATA_INGESTION_PROCESSED_DATA_DIR = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, 'processed')

# Paths for feature store CSV and train/test CSVs
DATA_INGESTION_FEATURE_STORE_FILE_PATH: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR, 'feature_store.csv')
DATA_INGESTION_TRAIN_FILE_PATH: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
DATA_INGESTION_VAL_FILE_PATH: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, DATA_INGESTION_INGESTED_DIR, VAL_FILE_NAME)
DATA_INGESTION_FINAL_TEST_FILE_PATH: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, DATA_INGESTION_INGESTED_DIR, FINAL_TEST_FILE_NAME)

# Train-test split ratio
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

import os, sys
from datetime import datetime
from NLP_SA.exception.exception import CustomException
from NLP_SA.logger.log import logging
from NLP_SA.constants import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")):
        logging.info("Initializing TrainingPipelineConfig...")
        try:
            self.pipeline_name = training_pipeline.PIPELINE_NAME
            self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
            logging.info("TrainingPipelineConfig initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize TrainingPipelineConfig.", exc_info=True)
            raise CustomException(e, sys)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            logging.info("Initializing DataIngestionConfig...")

            self.data_ingestion_dir: str = os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_INGESTION_DIR_NAME
            )
            logging.info(f"Data ingestion directory set to: {self.data_ingestion_dir}")

            self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                'feature_store.csv'
            )
            logging.info(f"Feature store path: {self.feature_store_file_path}")

            self.training_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TRAIN_FILE_NAME
            )
            self.val_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.VAL_FILE_NAME
            )

            self.final_test_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.FINAL_TEST_FILE_NAME
            )

            logging.info(f"Train file path: {self.training_file_path}")
            logging.info(f"Valid file path: {self.val_file_path}")
            logging.info(f"Test (final) file path: {self.final_test_file_path}")

            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            logging.info(f"Train/Test split ratio: {self.train_test_split_ratio}")

            # S3 download info
            self.s3_bucket_name: str = training_pipeline.DATA_INGESTION_S3_BUCKET
            self.s3_key: str = training_pipeline.DATA_INGESTION_S3_KEY
            logging.info(f"S3 bucket: {self.s3_bucket_name}, S3 key: {self.s3_key}")

            # Local download & extraction paths
            self.local_tgz_path: str = os.path.join(self.data_ingestion_dir, 'amazon_review_full_csv.tgz')
            self.extracted_dir: str = os.path.join(self.data_ingestion_dir, 'amazon_review_full_csv')
            logging.info(f"TGZ file local path: {self.local_tgz_path}")
            logging.info(f"Extracted data directory: {self.extracted_dir}")

            logging.info("DataIngestionConfig initialized successfully.")

        except Exception as e:
            logging.error("Failed to initialize DataIngestionConfig.", exc_info=True)
            raise CustomException(e, sys)
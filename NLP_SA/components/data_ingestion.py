import os
import sys
import tarfile
import csv
import pandas as pd
from sklearn.model_selection import train_test_split

from NLP_SA.logger.log import logging
from NLP_SA.exception.exception import CustomException
from NLP_SA.constants import training_pipeline
from NLP_SA.entity.config_entity import DataIngestionConfig
from NLP_SA.entity.artifact_entity import DataIngestionArtifact
from NLP_SA.utils.s3_utils import download_from_s3


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            self.config = config
            logging.info("Initialized DataIngestion class.")
        except Exception as e:
            logging.error("Failed to initialize DataIngestion class.")
            raise CustomException(e, sys)

    def download_data(self) -> None:
        try:
            logging.info("Starting data download from S3 (S3 utils)...")
            download_from_s3(
                bucket=self.config.s3_bucket_name,
                key=self.config.s3_key,
                local_path=self.config.local_tgz_path
            )
            logging.info(f"Downloaded file to {self.config.local_tgz_path}")
        except Exception as e:
            logging.error("Failed to download data from S3.")
            raise CustomException(e, sys)

    def extract_tgz(self) -> None:
        try:
            logging.info("Extracting .tgz file...")
            os.makedirs(self.config.extracted_dir, exist_ok=True)
            with tarfile.open(self.config.local_tgz_path, "r:gz") as tar:
                tar.extractall(path=self.config.extracted_dir)
            logging.info(f"Extraction complete → {self.config.extracted_dir}")
        except Exception as e:
            logging.error("Failed to extract tgz file.")
            raise CustomException(e, sys)

    def load_train_data(self) -> pd.DataFrame:
        try:
            logging.info("Loading extracted train.csv to DataFrame...")
            csv_path = os.path.join(self.config.extracted_dir, 'amazon_review_full_csv', 'train.csv')
            df = pd.read_csv(
                csv_path,
                header=None,
                names=['label', 'title', 'text'],
                sep=',',
                quoting=csv.QUOTE_ALL,  # or csv.QUOTE_MINIMAL if this doesn't work
                doublequote=True,
                escapechar=None,
                engine='python'  # more tolerant parser for complex CSV
            )

            # Merge title and text into a single "text" field
            df["text"] = df["title"].fillna('') + ". " + df["text"].fillna('')
            df = df[["label", "text"]]

            # Convert labels from 1–5 to 0–4 (optional, helpful for classification)
            df["label"] = df["label"] - 1

            logging.info(f"Train data shape: {df.shape}")
            return df
        except Exception as e:
            logging.error("Failed to load train.csv.")
            raise CustomException(e, sys)

    def load_test_data(self) -> pd.DataFrame:
        try:
            logging.info("Loading extracted test.csv (final holdout) to DataFrame...")
            csv_path = os.path.join(self.config.extracted_dir, 'amazon_review_full_csv', 'test.csv')

            df = pd.read_csv(
                csv_path,
                header=None,
                names=['label', 'title', 'text'],
                sep=',',
                quoting=csv.QUOTE_ALL,  # or csv.QUOTE_MINIMAL if this doesn't work
                doublequote=True,
                escapechar=None,
                engine='python'  # more tolerant parser for complex CSV
            )

            df["text"] = df["title"].fillna('') + ". " + df["text"].fillna('')
            df = df[["label", "text"]]
            df["label"] = df["label"] - 1

            logging.info(f"Final test data shape: {df.shape}")
            return df
        except Exception as e:
            logging.error("Failed to load test.csv.")
            raise CustomException(e, sys)

    def save_feature_store(self, df: pd.DataFrame) -> None:
        try:
            os.makedirs(os.path.dirname(self.config.feature_store_file_path), exist_ok=True)
            df.to_csv(self.config.feature_store_file_path, index=False)
            logging.info(f"Feature store saved at {self.config.feature_store_file_path}")
        except Exception as e:
            raise CustomException(e, sys)

    def split_and_save(self, df: pd.DataFrame) -> None:
        try:
            logging.info("Splitting data into train and validation sets...")
            train_df, val_df = train_test_split(
                df, test_size=self.config.train_test_split_ratio, random_state=42, stratify=df["label"]
            )

            ingestion_dir = os.path.dirname(self.config.training_file_path)
            os.makedirs(ingestion_dir, exist_ok=True)

            train_df.to_csv(self.config.training_file_path, index=False)
            val_df.to_csv(self.config.val_file_path, index=False)

            logging.info(f"Train data saved to {self.config.training_file_path}")
            logging.info(f"Validation data saved to {self.config.val_file_path}")
        except Exception as e:
            raise CustomException(e, sys)

    def save_final_test(self, df: pd.DataFrame) -> None:
        try:
            os.makedirs(os.path.dirname(self.config.final_test_file_path), exist_ok=True)
            df.to_csv(self.config.final_test_file_path, index=False)
            logging.info(f"Final test data saved to {self.config.final_test_file_path}")
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion process...")

            # Step 1: Download and extract
            self.download_data()
            self.extract_tgz()

            # Step 2: Load train + test CSVs
            train_df = self.load_train_data()
            final_test_df = self.load_test_data()

            # Step 3: Save full feature store (entire training CSV)
            self.save_feature_store(train_df)

            # Step 4: Split train into train/val
            self.split_and_save(train_df)

            # Step 5: Save final test
            self.save_final_test(final_test_df)

            # Step 6: Return artifact
            artifact = DataIngestionArtifact(
                trained_file_path=self.config.training_file_path,
                val_file_path=self.config.val_file_path,
                final_test_file_path=self.config.final_test_file_path,
                is_ingested=True,
                message="Data ingestion completed successfully."
            )

            logging.info("Data ingestion pipeline completed successfully.")
            return artifact

        except Exception as e:
            logging.error("Data ingestion failed.", exc_info=True)
            raise CustomException(e, sys)
from NLP_SA.exception.exception import CustomException
from NLP_SA.logger.log import logging

from NLP_SA.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from NLP_SA.components.data_ingestion import DataIngestion
import sys

if __name__ == "__main__":
    try:
        logging.info("Starting ONLY data splitting process (skip download & extraction)...")

        # Hardcode the existing artifact timestamp folder you want to reuse:
        existing_timestamp = "20250831_175830"  # <--- set your folder here


        # Step 1: Load pipeline and data ingestion config
        pipeline_config = TrainingPipelineConfig(timestamp=existing_timestamp)
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=pipeline_config)
        data_ingestion = DataIngestion(config=data_ingestion_config)

        # SKIP: data_ingestion.download_data()
        # SKIP: data_ingestion.extract_tgz()

        # Step 2: Load the already extracted data
        train_df = data_ingestion.load_train_data()
        test_df = data_ingestion.load_test_data()

        # Step 3: Save the full feature store
        data_ingestion.save_feature_store(train_df)

        # Step 4: Split train → train + val
        data_ingestion.split_and_save(train_df)

        # Step 5: Save final test set
        data_ingestion.save_final_test(test_df)

        logging.info("Completed ONLY data splitting successfully.")

    except CustomException as ce:
        logging.error("Pipeline failed due to a custom exception.")
        print(str(ce))
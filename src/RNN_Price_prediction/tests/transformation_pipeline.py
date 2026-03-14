import os
import sys

sys.path.append(os.getcwd())

from logger import *
from src.RNN_Price_prediction.components.data_transformation import DataTransformation
from src.RNN_Price_prediction.config.configuration import ConfigurationManager

def main():
    try:
        logging.info("Starting Data Transformation Pipeline")
        
        config_manager = ConfigurationManager()
        transform_config = config_manager.get_data_transformation_config()
        ingestion_config = config_manager.get_data_ingestion_config()
        
        if not ingestion_config.raw_data_path.exists():
            logging.error(f"Raw data not found at {ingestion_config.raw_data_path}. Run ingestion_pipeline.py first.")
            return

        data_transformation = DataTransformation(config=transform_config)
        
        data_transformation.initiate_data_transformation(data_path=str(ingestion_config.raw_data_path))
        
        logging.info("Data Transformation Pipeline completed successfully")
        print("\nSUCCESS: Data Transformation Pipeline completed.")
        
    except Exception as e:
        if 'logging' in globals():
            logging.error(f"Data Transformation Pipeline failed: {e}")
        print(f"\nERROR: Data Transformation Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()

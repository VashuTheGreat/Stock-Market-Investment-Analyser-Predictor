import os
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

from logger import *
from src.RNN_Price_prediction.components.model_trainer import ModelTrainer
from src.RNN_Price_prediction.config.configuration import ConfigurationManager

def main():
    try:
        logging.info("Starting Model Training Pipeline")
        
        config_manager = ConfigurationManager()
        trainer_config = config_manager.get_model_trainer_config()
        transform_config = config_manager.get_data_transformation_config()
        
        if not transform_config.transformed_data_path.exists():
            logging.error(f"Transformed data not found at {transform_config.transformed_data_path}. Run transformation_pipeline.py first.")
            return

        model_trainer = ModelTrainer(config=trainer_config)
        
        model_trainer.initiate_model_trainer(transformed_data_path=str(transform_config.transformed_data_path))
        
        logging.info("Model Training Pipeline completed successfully")
        print("\nSUCCESS: Model Training Pipeline completed.")
        
    except Exception as e:
        if 'logging' in globals():
            logging.error(f"Model Training Pipeline failed: {e}")
        print(f"\nERROR: Model Training Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()

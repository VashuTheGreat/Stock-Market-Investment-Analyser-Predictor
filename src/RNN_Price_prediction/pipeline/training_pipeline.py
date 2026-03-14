import sys
from src.RNN_Price_prediction.config.configuration import ConfigurationManager
from src.RNN_Price_prediction.components.data_ingestion import DataIngestion
from src.RNN_Price_prediction.components.data_transformation import DataTransformation
from src.RNN_Price_prediction.components.model_trainer import ModelTrainer
from src.RNN_Price_prediction.components.model_evaluation import ModelEvaluation
from logger import logging
from exception import MyException

class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    async def run_pipeline(self, tickers: list):
        try:
            logging.info("Starting training pipeline...")
            
            # 1. Ingestion
            ingestion_config = self.config_manager.get_data_ingestion_config()
            ingestion = DataIngestion(config=ingestion_config)
            raw_data_path = await ingestion.initiate_data_ingestion(tickers=tickers)
            
            # 2. Transformation
            transformation_config = self.config_manager.get_data_transformation_config()
            transformation = DataTransformation(config=transformation_config)
            transformed_data_path, _ = transformation.initiate_data_transformation(str(raw_data_path))
            
            # 3. Training
            trainer_config = self.config_manager.get_model_trainer_config()
            trainer = ModelTrainer(config=trainer_config)
            model_path = trainer.initiate_model_trainer(str(transformed_data_path))
            
            # 4. Evaluation (New)
            evaluation_config = self.config_manager.get_model_evaluation_config()
            evaluation = ModelEvaluation(config=evaluation_config)
            evaluation.generate_performance_plot()
            
            logging.info("Training pipeline completed successfully.")
            return model_path

        except Exception as e:
            raise MyException(e, sys)

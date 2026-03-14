import yaml
from pathlib import Path
from src.RNN_Price_prediction.entity.config_entity import (DataIngestionConfig, 
                                                               DataTransformationConfig, 
                                                               ModelTrainerConfig,
                                                               PredictionConfig,
                                                               ModelEvaluationConfig)
from src.RNN_Price_prediction.contants import *

class ConfigurationManager:
    def __init__(self, 
                 config_filepath = Path("src/RNN_Price_prediction/config/config.yaml"),
                 params_filepath = Path("src/RNN_Price_prediction/config/params.yaml")):
        
        self.config = self.read_yaml(config_filepath)
        self.params = self.read_yaml(params_filepath)

        self.create_directories([self.config['artifacts_root']])

    def read_yaml(self, path_to_yaml: Path) -> dict:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content

    def create_directories(self, path_to_directories: list, verbose=True):
        import os
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config['data_ingestion']
        self.create_directories([config['root_dir']])

        return DataIngestionConfig(
            root_dir=Path(config['root_dir']),
            raw_data_path=Path(config['raw_data_path'])
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config['data_transformation']
        self.create_directories([config['root_dir']])

        return DataTransformationConfig(
            root_dir=Path(config['root_dir']),
            transformed_data_path=Path(config['transformed_data_path']),
            scaler_path=Path(config['scaler_path'])
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config['model_trainer']
        params = self.params
        self.create_directories([config['root_dir']])

        return ModelTrainerConfig(
            root_dir=Path(config['root_dir']),
            trained_model_path=Path(config['trained_model_path']),
            transformed_data_path=Path(self.config['data_transformation']['transformed_data_path']),
            hidden_size=params['hidden_size'],
            num_layers=params['num_layers'],
            output_size=params['output_size'],
            learning_rate=params['learning_rate'],
            epochs=params['epochs'],
            batch_size=params['batch_size'],
            window_size=params['window_size'],
            performance_plot_path=Path(config['performance_plot_path'])
        )

    def get_prediction_config(self) -> PredictionConfig:
        params = self.params
        return PredictionConfig(
            trained_model_path=Path(self.config['model_trainer']['trained_model_path']),
            scaler_path=Path(self.config['data_transformation']['scaler_path']),
            hidden_size=params['hidden_size'],
            num_layers=params['num_layers'],
            output_size=params['output_size'],
            window_size=params['window_size'],
            forecast_plot_path=Path(self.config['model_evaluation']['forecast_plot_path'])
        )

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config['model_evaluation']
        params = self.params
        self.create_directories([config['root_dir']])

        return ModelEvaluationConfig(
            root_dir=Path(config['root_dir']),
            trained_model_path=Path(self.config['model_trainer']['trained_model_path']),
            transformed_data_path=Path(self.config['data_transformation']['transformed_data_path']),
            scaler_path=Path(self.config['data_transformation']['scaler_path']),
            performance_plot_path=Path(self.config['model_trainer']['performance_plot_path']),
            forecast_plot_path=Path(config['forecast_plot_path']),
            hidden_size=params['hidden_size'],
            num_layers=params['num_layers'],
            output_size=params['output_size'],
            window_size=params['window_size'],
            learning_rate=params['learning_rate'],
            epochs=params['epochs'],
            batch_size=params['batch_size']
        )

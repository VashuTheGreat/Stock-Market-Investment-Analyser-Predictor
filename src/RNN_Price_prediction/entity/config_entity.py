from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_data_path: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    transformed_data_path: Path
    scaler_path: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    trained_model_path: Path
    transformed_data_path: Path
    hidden_size: int
    num_layers: int
    output_size: int
    learning_rate: float
    epochs: int
    batch_size: int
    window_size: int
    performance_plot_path: Path

@dataclass(frozen=True)
class PredictionConfig:
    trained_model_path: Path
    scaler_path: Path
    hidden_size: int
    num_layers: int
    output_size: int
    window_size: int
    forecast_plot_path: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    trained_model_path: Path
    transformed_data_path: Path
    scaler_path: Path
    performance_plot_path: Path
    forecast_plot_path: Path
    hidden_size: int
    num_layers: int
    output_size: int
    window_size: int
    learning_rate: float
    epochs: int
    batch_size: int
    learning_rate: float
    epochs: int
    batch_size: int

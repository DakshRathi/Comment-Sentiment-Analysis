import logging
import pandas as pd
import yaml
from typing import Dict, Any
from pathlib import Path
import joblib


PARAMS_PATH = Path(__file__).parent.parent / "params.yaml"


class Logger:
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """
        Initialize the logger.

        Parameters
        ----------
        name : str
            The name of the logger.
        level : int, optional
            The logging level. Defaults to logging.INFO.

        Returns
        -------
        None
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add handler to the logger
        self.logger.addHandler(console_handler)


    def info(self, message: str) -> None:
        """
        Log a message with severity 'INFO'.

        Parameters
        ----------
        message : str
            The message to log.

        Returns
        -------
        None
        """
        self.logger.info(message)


    def debug(self, message: str) -> None:
        """
        Log a message with severity 'DEBUG'.

        Parameters
        ----------
        message : str
            The message to log.

        Returns
        -------
        None
        """
        self.logger.debug(message)


    def warning(self, message: str) -> None:
        """
        Log a message with severity 'WARNING'.

        Parameters
        ----------
        message : str
            The message to log.

        Returns
        -------
        None
        """
        self.logger.warning(message)


    def error(self, message: str) -> None:
        """
        Log a message with severity 'ERROR'.

        Parameters
        ----------
        message : str
            The message to log.

        Returns
        -------
        None
        """
        self.logger.error(message)


    def critical(self, message: str) -> None:
        """
        Log a message with severity 'CRITICAL'.

        Parameters
        ----------
        message : str
            The message to log.

        Returns
        -------
        None
        """
        self.logger.critical(message)


def load_data(logger: Logger, file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        The path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.
    """
    try:
        logger.info(f"Loading data from {file_path}")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"No data found in file: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        raise


def load_params(logger: Logger, file_path: str = PARAMS_PATH) -> Dict:
    """
    Load parameters from a YAML file.

    Parameters
    ----------
    file_path : str
        The path to the YAML file containing the parameters.

    Returns
    -------
    Dict
        The loaded parameters as a dictionary.
    """
    try:
        logger.info(f"Loading parameters from {file_path}")
        with open(file_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.info("Parameters loaded successfully.")
        return params
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_path}")
        raise e
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file: {file_path}")
        raise e
    
    
def save_data(logger: Logger, data: pd.DataFrame, data_path: Path, filename: str) -> None:
    """
    Save a pandas DataFrame to a given directory.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame to save.
    data_path : Path
        The directory to save the DataFrame to.
    filename : str
        The name of the file to save the DataFrame as.

    Returns
    -------
    None
    """
    try:
        full_path = data_path / filename
        logger.info(f"Saving data")
        data_path.mkdir(parents=True, exist_ok=True)
        data.to_csv(full_path, index=False)
        logger.info(f"Data saved successfully to {full_path}.")
    except Exception as e:
        logger.error(f"Error saving data to {full_path}: {e}")
        raise e
    

def save_model(logger: Logger, model: Any, model_path: Path, modelname: str) -> None:
    """
    Save a model to a given directory.

    Parameters
    ----------
    model : Any
        The model to save.
    model_path : Path
        The directory to save the model to.
    modelname : str
        The name of the model to save the model as.

    Returns
    -------
    None
    """
    try:
        logger.info(f"Saving model {modelname}")
        model_path.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path / f'{modelname}.joblib')
        logger.info(f"{modelname} saved successfully to {model_path}.")
    except Exception as e:
        logger.error(f"Error saving {modelname} to {model_path}: {e}")
        raise e

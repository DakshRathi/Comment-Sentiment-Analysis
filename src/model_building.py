import logging
import lightgbm as lgb
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple
from utils import Logger, load_params, load_data, save_model

# Initialize logger
logger = Logger('model_building', logging.INFO)

def prepare_training_data(X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare training data by verifying features and the target variable.

    Parameters
    ----------
    X : pd.DataFrame
        The training data containing features.
    y : pd.Series
        The target variable.

    Returns
    -------
    X : pd.DataFrame
        Verified features for training the model.
    y : pd.Series
        Verified target variable.
    """
    logger.info("Preparing training data...")
    try:
        # Confirm that data shapes are consistent
        if X.shape[0] != y.shape[0]:
            raise ValueError("Mismatch between feature rows and target rows")

        logger.info("Data preparation completed successfully.")
        return X, y
    except Exception as e:
        logger.error(f"Error during data preparation: {str(e)}")
        raise 

def train_model(X: pd.DataFrame, y: pd.Series, model_params: Dict) -> lgb.LGBMClassifier:
    """
    Train the LightGBM model.

    Parameters
    ----------
    X : pd.DataFrame
        Features for the training.
    y : pd.Series
        Target variable for the training.
    model_params : Dict
        Parameters for the LightGBM model.

    Returns
    -------
    lgb.LGBMClassifier
        The trained LightGBM model.
    """
    try:
        logger.info("Training model...")
        model = lgb.LGBMClassifier(**model_params)
        model.fit(X, y)
        logger.info("LightGBM model trained successfully.")
        return model
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

def main() -> None:
    """
    Execute the model building pipeline.

    The pipeline involves loading the preprocessed data, training the model,
    and saving the trained model to a specified directory.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    try:
        logger.info("Starting model building pipeline...")

        # Load the parameters
        params = load_params(logger)['model_building']

        # Define data path
        path = Path(__file__).parent.parent / 'data' / 'processed'

        # Load features and target separately
        X = load_data(logger, path / 'train_tfidf.csv')
        y = load_data(logger, path / 'train_target.csv')['category'].astype(int)

        # Prepare features and target variable
        X, y = prepare_training_data(X, y)

        # Train the model
        model = train_model(X, y, params)

        # Save the model
        save_model(logger, model, path.parent.parent / 'models', 'lgbm_model')

        logger.info("Model building pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Error in model building pipeline: {str(e)}")
        raise

if __name__ == '__main__':
    main()
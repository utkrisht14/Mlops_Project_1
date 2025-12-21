import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint
import mlflow
from config.paths_config import ARTIFACTS_DIR

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        """
        :param train_path: Processed train path
        :param test_path: Processed test path
        """
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist  =  LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS


    def load_and_split_data(self):
        try:
            logger.info(f"Loading data: {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data: {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data splitted sucefully for Model Training")

            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Failed to load data", e)


    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Intializing our model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our Hyperparamter tuning.")

            random_search = RandomizedSearchCV(
                estimator = lgbm_model,
                param_distributions = self.params_dist,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs = self.random_search_params["n_jobs"],
                verbose = self.random_search_params["verbose"],
                random_state = self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            logger.info("Starting hyperparameter tuning.")

            # Fit the random_search method
            random_search.fit(X_train, y_train)

            logger.info("Hyperparamter tuning completed")

            # Get the best parameters
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best params: {best_params}")

            return best_lgbm_model

        except Exception as e:
            raise CustomException("Failed to tune hyperparameters", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info(f"Evaluating model.")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1 Score : {f1}")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }

        except Exception as e:
            logger.error(f"Error while evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)


    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info("Saving model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Saved model: {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error while saving model: {e}")
            raise CustomException("Failed to save model", e)

    def run(self):
        try:
            mlflow.set_tracking_uri(f"file:///{ARTIFACTS_DIR}/mlruns")
            mlflow.set_experiment("hotel_reservation_prediction")

            with mlflow.start_run():
                logger.info("Starting Model training pipeline")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()

                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)

                self.save_model(best_lgbm_model)

                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

        except Exception as e:
            logger.exception("Error in model training pipeline")
            raise CustomException("Failed during model training pipeline", e)


if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()








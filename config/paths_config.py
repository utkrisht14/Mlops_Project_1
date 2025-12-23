import os

# Absolute project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

################ DATA ################

ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")

RAW_DIR = os.path.join(ARTIFACTS_DIR, "raw")
PROCESSED_DIR = os.path.join(ARTIFACTS_DIR, "processed")
MODELS_DIR = os.path.join(ARTIFACTS_DIR, "models")

RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")

################ MODEL ################

MODEL_OUTPUT_PATH = os.path.join(
    PROJECT_ROOT,
    "artifacts",
    "models",
    "lgbm_model.pkl"
)

################ CONFIG ################

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.yaml")

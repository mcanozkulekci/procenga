from pipeline import _create_pipeline
from tfx.orchestration.local import local_dag_runner
import tempfile
import urllib.request
from absl import logging
import os
import pandas as pd

PIPELINE_NAME = "coin-simple"

# Output directory to store artifacts generated from the pipeline.
PIPELINE_ROOT = os.path.join('pipelines', PIPELINE_NAME)
# Path to a SQLite DB file to use as an MLMD storage.
METADATA_PATH = os.path.join('metadata', PIPELINE_NAME, 'metadata.db')
# Output directory where created models from the pipeline will be exported.
SERVING_MODEL_DIR = os.path.join('serving_model', PIPELINE_NAME)


logging.set_verbosity(logging.INFO)  # Set default logging level.

df = pd.read_csv("BTCUSDT_1h.csv", header=1)
df.to_csv('tfx-data/denis.csv')

DATA_ROOT = "tfx-data"
_data_filepath = os.path.join(DATA_ROOT, "denis.csv")
_trainer_module_file = 'coin_trainer.py'


local_dag_runner.LocalDagRunner().run(
    _create_pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        data_root=DATA_ROOT,
        module_file=_trainer_module_file,
        serving_model_dir=SERVING_MODEL_DIR,
        metadata_path=METADATA_PATH))

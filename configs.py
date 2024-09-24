from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

DATA_FOLDER = "data"
DATA_BACKUPS_FOLDER = "data_backups"
IMGS_FOLDER = "images"

TAGS_FILE = "tags.json"
TAGS_USED_FOR_TRAINING_FILE = "tags_for_model_training.json"
ID_FILE = "id.txt"
SHUFFLED_ID_FILE = "shuffled_id.json"
MODEL_FILE = "model.joblib"
UNSORTED_IMGS_FILE = "unsorted.json"
IMAGES_CSV_FILE = "images.csv"

URL = "https://rule34.xxx/index.php?page=post&s=view&id={id}"

KEY = os.getenv("KEY")

from dotenv import load_dotenv
import os

load_dotenv()


def get_dataset_file():
    file = os.getenv('DATASET_ZIP')
    return file

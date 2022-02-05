import hashlib
import io
import json
import os
import zipfile
from typing import List
import pandas as pd


def to_csv(data: List[dict]):
    df = pd.DataFrame.from_records(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    return stream


def to_xls(data: List[dict]):
    df = pd.DataFrame.from_records(data)
    stream = io.BytesIO()
    df.to_excel(stream, index=False)
    return stream


def json_to_dict(file) -> dict:
    with open(file, encoding='utf8') as json_file:
        return json.load(json_file)


def get_files(rootdir):
    files_list = []
    for subdir, directory, files in os.walk(rootdir):
        for file in files:
            if not file.startswith('.') and file.endswith('.json'):
                files_list.append(os.path.join(subdir, file))
    return files_list


def extract_zip(folder_name, zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(folder_name)


def hash_password(password: str) -> str:
    password = hashlib.md5(password.encode('utf-8'))
    return password.hexdigest()


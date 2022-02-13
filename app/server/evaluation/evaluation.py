import os
import time
import numpy as np
from sklearn.metrics import recall_score, f1_score, precision_score
from dotenv import load_dotenv

from app.server.utils.Utils import extract_zip, get_files, json_to_dict

load_dotenv()


def get_base_model():
    folder_name = os.getenv('BASE_MODEL_FOLDER')
    file_list = get_files(folder_name)
    file_list.sort()
    return file_list


def get_recall_score(base, to_compare):
    return recall_score(base, to_compare, average='micro')


def get_f1_score(base, to_compare):
    return f1_score(base, to_compare, average='micro', zero_division=1)


def get_precision_score(base, to_compare):
    return precision_score(base, to_compare, average='micro')


def get_values_from_dict(data):
    result = []
    for key, value in data.items():
        result.append(value)
    return result


def evaluation(method, file):
    folder_name: str = os.getenv('UPLOADED_METHODS_FOLDER') + str(method['name']) + str(round(time.time()))
    extract_zip(folder_name, file)
    file_list = get_files(folder_name)
    file_list.sort()
    base_model = get_base_model()

    f_score = []
    r_score = []
    p_score = []

    for file, base in zip(file_list, base_model):
        data = json_to_dict(file)
        base_data = json_to_dict(base)

        result = get_values_from_dict(data)
        base_result = get_values_from_dict(base_data)

        f_score.append(get_f1_score(base_result, result))
        r_score.append((get_recall_score(base_result, result)))
        p_score.append((get_precision_score(base_result, result)))

    method['results'] = {
        'f1_score': np.mean(f_score),
        'recall_score': np.mean(r_score),
        'precision_score': np.mean(p_score)
    }
    return method

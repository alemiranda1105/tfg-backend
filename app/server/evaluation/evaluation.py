import time
import numpy as np
from sklearn.metrics import recall_score, f1_score, precision_score

from app.server.utils.Utils import extract_zip, get_files, json_to_dict


def get_recall_score(to_compare):
    return recall_score(to_compare, to_compare, average='micro')


def get_f1_score(to_compare):
    return f1_score(to_compare, to_compare, average='micro', zero_division=1)


def get_precision_score(to_compare):
    return precision_score(to_compare, to_compare, average='micro')


def evaluation(method, file):
    folder_name: str = '/Users/alemiranda/Desktop/tfg/uploaded_methods/' + str(method['name']) + str(round(time.time()))
    extract_zip(folder_name, file)
    file_list = get_files(folder_name)
    f_score = []
    r_score = []
    p_score = []
    for file in file_list:
        data = json_to_dict(file)
        result = []
        for key, value in data.items():
            result.append(value)
        f_score.append(get_f1_score(result))
        r_score.append((get_recall_score(result)))
        p_score.append((get_precision_score(result)))
    method['results'].append({'f1_score': np.mean(f_score)})
    method['results'].append({'recall_score': np.mean(r_score)})
    method['results'].append({'precision_score': np.mean(p_score)})
    return method

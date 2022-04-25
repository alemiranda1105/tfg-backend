import os
import numpy as np
from sklearn.metrics import recall_score, f1_score, precision_score
from dotenv import load_dotenv

from server.utils.Utils import extract_zip, get_files, json_to_dict, compress_zip, delete_folder

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


def get_values(data):
    result = []
    fields = []
    for key, value in data.items():
        result.append(value)
        fields.append(key)
    return result, fields


def evaluation(method, file):
    method['results_by_category'] = {}

    # File processing
    folder_name = os.getenv('UPLOADED_METHODS_FOLDER') + str(method['name'])
    method['file_dir'] = folder_name
    extract_zip(folder_name, file)

    # sorts file list to get in order
    file_list = get_files(folder_name)
    file_list.sort()

    # files by each folder
    files_by_template = int(len(file_list) / 9)

    base_model = get_base_model()

    # aux variables
    i = 0
    template = 1

    base_result = []
    test_result = []

    raw_base_result = {}
    raw_test_result = {}

    fields = []

    # Results
    results_template_field = {}

    f1_field = {}
    f1_template = {}

    recall_field = {}
    recall_template = {}

    precision_field = {}
    precision_template = {}

    # Load results from all the files and initialize variables
    for file, base in zip(file_list, base_model):
        test_data = json_to_dict(file)
        base_data = json_to_dict(base)

        base_values, fields = get_values(base_data)
        base_result.append(base_values)

        test_result.append(get_values(test_data)[0])
        i += 1
        if i == files_by_template:
            method['results_by_category'][str(template)] = {
                'f1_score': 0.0,
                'recall_score': 0.0,
                'precision_score': 0.0
            }
            raw_base_result[template] = {}
            raw_test_result[template] = {}
            results_template_field[str(template)] = {}
            for f in fields:
                raw_base_result[template][f] = []
                raw_test_result[template][f] = []
                results_template_field[str(template)][f] = []
            i = 0
            template += 1

    template = 1
    i = 0
    # Base result format
    for file in base_result:
        for res, field in zip(file, fields):
            raw_base_result[template][field].append(res)
        i += 1
        if i >= files_by_template:
            template += 1
            i = 0
    i = 0
    template = 1
    # Test result format
    for file in test_result:
        for res, field in zip(file, fields):
            raw_test_result[template][field].append(res)
        i += 1
        if i >= files_by_template:
            template += 1
            i = 0

    # Evaluation
    for k, v in raw_base_result.items():
        f1_template[k] = []
        recall_template[k] = []
        precision_template[k] = []

        # actual field and res of this field
        # By field
        for f, res in v.items():
            if k <= 1:
                f1_field[f] = []
                recall_field[f] = []
                precision_field[f] = []
            f1s = get_f1_score(res, raw_test_result[k][f])
            recs = get_recall_score(res, raw_test_result[k][f])
            pres = get_precision_score(res, raw_test_result[k][f])

            # By template and field
            results_template_field[str(k)][f].append(
                {
                    "name": 'f1_score',
                    "result": f1s
                }
            )
            results_template_field[str(k)][f].append(
                {
                    "name": 'recall_score',
                    "result": recs
                },
            )
            results_template_field[str(k)][f].append(
                {
                    "name": 'precision_score',
                    "result": pres
                }
            )

            f1_field[f].append(f1s)
            recall_field[f].append(recs)
            precision_field[f].append(pres)

        # the array is filled with the total score of the fields
        # By template
        for f, res in f1_field.items():
            f1_template[k].append(res[k-1])
        for f, res in recall_field.items():
            recall_template[k].append(res[k-1])
        for f, res in precision_field.items():
            precision_template[k].append(res[k-1])

    # Means calculation
    for t, res in f1_template.items():
        method['results_by_category'][str(t)]['f1_score'] = np.round(np.mean(res), decimals=4)
    for t, res in recall_template.items():
        method['results_by_category'][str(t)]['recall_score'] = np.round(np.mean(res), decimals=4)
    for t, res in precision_template.items():
        method['results_by_category'][str(t)]['precision_score'] = np.round(np.mean(res), decimals=4)

    method['results_by_category_field'] = results_template_field

    method['results_by_field'] = []
    for f in fields:
        method['results_by_field'].append({
            'name': f,
            'results': {
                'f1_score': np.round(np.mean(f1_field[f]), decimals=4),
                'recall_score': np.round(np.mean(f1_field[f]), decimals=4),
                'precision_score': np.round(np.mean(f1_field[f]), decimals=4),
            }
        })

    method['results'] = {
        'f1_score': np.round(np.mean(list(f1_template.values())), decimals=4),
        'recall_score': np.round(np.mean(list(recall_template.values())), decimals=4),
        'precision_score': np.round(np.mean(list(precision_template.values())), decimals=4)
    }

    compress_zip(folder_name, method['file_dir'])

    return method

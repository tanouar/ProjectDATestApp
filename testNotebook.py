import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import tempfile
import chardet
import json

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def is_valid_notebook(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
            json_content = json.loads(content)
            return all(key in json_content for key in ["cells", "metadata", "nbformat", "nbformat_minor"])
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False

def execute_notebooks_in_directory(directory, timeout=600):
    notebooks = [os.path.join(root, file)
                 for root, _, files in os.walk(directory)
                 for file in files if file.endswith('.ipynb') and not file.startswith('._')]
    
    log_data = []
    ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    
    for notebook_path in notebooks:
        encoding = detect_encoding(notebook_path)
        if not is_valid_notebook(notebook_path, encoding):
            log_data.append({'notebook': notebook_path, 'status': 'INVALID', 'log': 'Invalid notebook format'})
            continue
        with open(notebook_path, 'r', encoding=encoding) as f:
            nb = nbformat.read(f, as_version=4)
            try:
                ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
                log_data.append({'notebook': notebook_path, 'status': 'PASS', 'log': 'Executed successfully'})
            except Exception as e:
                log_data.append({'notebook': notebook_path, 'status': 'FAIL', 'log': str(e)})
    
    return log_data

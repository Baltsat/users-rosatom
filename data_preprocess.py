import json
import os

def class_identifier(path):
    """Добавляет columns - 'n_cluster' где отображает номер кластера, относительно других.
    path -- путь json-файла"""
    
    with open(path, encoding='utf-8-sig') as f:
        q = json.load(f)
        answers = q['answers']
        clusters = {}
        num_cluster = 0
        
        for batch in answers:
            if batch['cluster'] in clusters:
                cl = clusters[batch['cluster']]
            else:
                clusters[batch['cluster']] = num_cluster
                cl = num_cluster
                num_cluster += 1
            
            batch['n_cluster'] = cl
        
    return q

# ТРЕНИРОВОЧНЫЕ ДАННЫЕ
output_file = r'data/train_data.json'

data = []

for file in os.scandir('data/labeled/'):
    json_file = class_identifier(file.path)
    data.append(json_file)

with open(output_file, encoding='utf-8-sig', mode='w') as f:
    f.write(json.dumps(data, indent=4))


# ТЕСТОВЫЕ ДАННЫЕ
output_file = r'data/test_data.json'

data = []

for file in os.scandir('data/all/'):
    with open(file, encoding='utf-8-sig') as f:
        q = json.load(f)
    
    data.append(q)

with open(output_file, encoding='utf-8-sig', mode='w') as f:
    f.write(json.dumps(data, indent=4))
import json
import os

def class_identifier(path):
    """
    Добавляет в ключ 'answers' для каждого элемента ключ - 'n_cluster' где отображает номер кластера, относительно других.
    Также добавляет в ключ 'clusters' - количество кластеров. 
    Args:
        path: путь json-файла

    Return:
        dict: Словарь в формате json с добавленными ключами.
    """
    
    with open(path, encoding='utf-8-sig') as f:
        json_file = json.load(f)
        answers = json_file['answers']
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
        
        json_file['clusters'] = num_cluster
        
    return json_file


def merge_duplicate_answers(json_data):
    '''
    Объединяет дублирующиеся ответы и суммирует их количество.
    Args:
        json_data type: dict[list[dict]]: Cловарь с ключом 'asnwers' и вложенными в нём списком словарей с ключами: 'answer' и 'count'.

    Return:
        list: Новый список словарей с уникальными записями 'answer' и их суммированными значениями 'count'.
    '''
    unique_answers = {}
    
    for item in json_data['answers']:
        answer = item['answer']
        count = item['count']
        
        if answer in unique_answers:
            unique_answers[answer] += count
        else:
            unique_answers[answer] = count
    
    answers = [{'answer': answer, 'count': count} for answer, count in unique_answers.items()]
    
    return answers


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
        json_file = json.load(f)
        json_file['answers'] = merge_duplicate_answers(json_file)

        data.append(json_file)
    
    data.append(json_file)

with open(output_file, encoding='utf-8-sig', mode='w') as f:
    f.write(json.dumps(data, indent=4))
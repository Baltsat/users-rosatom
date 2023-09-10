<img width="657" alt="image" src="https://github.com/Baltsat/users-rosatom/assets/42536677/90141bd4-a8b7-47cd-b73a-c2cb65ad6ee9">  
![logo](https://github.com/Baltsat/users-rosatom/assets/42536677/8b3b5aa5-b56b-4c83-8681-6ca52d15f972)


# Улучшение представлений результатов в сервисе «Мой голос» от команды Users

Мы предлагаем решение для точного объединения ответов пользователей по смыслу в сервисе "Мой Голос" с помощью передового подхода к обработке текста Bert и визуализации результатов через веб-интерфейс на основе Streamlit. Решение выделяется тем, что устойчиво к ошибкам и опечаткам пользователей, а также учитывает даже латентные смысловые средства: эмоджи и пунктуацию.

Технические особенности:
Использование мультиязычного BERT для создания векторных представлений текста
Многоуровневая кластеризация: UMAP -> HDBSCAN -> CountVectorizer -> TF-IDF
- Эмоциональная окраска текста с помощью XLM Roberta, обученного на комментариях пользователей 
- Интерфейс на основе Streamlit


# Пример решения
![demo](https://github.com/Baltsat/users-rosatom/blob/main/data/gf.gif)

# Установка
- `git clone https://github.com/Baltsat/users-rosatom.git`
Необходим Python версии 3.9 и выше.
`pip install -r requirements.txt`
# Запуск
```bash
streamlit run main.py
```

# Используемое решение

* Для исходных данных проводится предобработка ответов: удаление пунктуации, фильтрация ненормативной лексики, лемматизация.
* На обработанных данных файнтюнены модели глубокого обучения, в частности, TweetNLP, XLM ROBERTA SENTIMENT MULTILINGUAL CLASSIFICATION, BertTopic.


* Визуализация кластеризации происходит посредством Streamlit. 

# Уникальность:

Наше уникальное решение объединяет передовой подход к обработке текста с помощью модели Bert, визуализацию результатов через интерфейс Streamlit и способность обрабатывать особенности русского и английского языка, что обеспечивает точность и простоту использования в сервисе "Мой Голос".

# Стек используемых технологий:

`Python3`, `git`, `GitHub` - инструменты разработки

`HF Transformers`, `TweetNLP`, `BertTopic` - библиотеки глубокого обучения

`Scikit-Learn`, `UMAP`, `KMeans` - фреймворки машинного обучения  

`Plotly`, `Streamlit`, `AltChart` - инструменты визуализации  


# Сравнение моделей

| Model  Description                                                | F1 Macro | Time    |
|--------------------------------------------------------|----------|---------|
| NaiveModel         каждое слово = новый кластер                                     | 0.81     | 10 ms   |
| LevensteinSimilarityModel    Если ответы схожие более, чем на 63% = образуют один кластер                          | 0.87     | 102 ms  |
| LevenshteinSimilatity + Processing Lemmatization, delete punct | 0.89     | 1 s     |
| SelfClusterModel#1 + SentimentTransformer (Bert-Multilingual + PCA + KMeans ) + (TweetNLP + xlm-roberta-multilingual) | 0.92     |         |
| SelfClusterModel#2                                     | 0.94     | 6 s     |
| SelfClusterModel#2 + SentimentTransformer              | 0.97     |         |







# Проводимые исследования

- `research_models_visualization.ipynb` - исследования с моделями градиентного бустинга
- `data_preprocess.ipynb` - предобработка данных 

# Документация Django API

Этот проект использует Django и Django Rest Framework для создания API. API предоставляет доступ к информации о вопросах и ответах (QA) и содержит следующие эндпойнты:

### Эндпойнт `/api/qaitems` Этот эндпойнт предоставляет доступ к данным о вопросах и ответах (QA). Он поддерживает следующие методы

-  `GET`: Получение списка всех элементов QA.

- `POST`: Создание нового элемента QA.

### Структура данных

Структура базы данных включает в себя следующие поля
- `question`: Текст вопроса.
- `answer`: Текст ответа.
- `sentiment`: Сентимент элемента.
- `j`: Значение J.
- `cluster_id`: Идентификатор кластера.
- `topic_name`: Название темы.

### Установка и запуск

Чтобы установить и запустить проект, выполните следующие шаги:
1. Клонируйте репозиторий с помощью `git clone`.
2. Создайте и активируйте виртуальное окружение.
3. Установите зависимости, выполнив команду `pip install -r requirements.txt`.
4. Примените миграции базы данных с помощью `python manage.py migrate`.
5. Запустите сервер с помощью `python manage.py runserver`.

## Примеры использования

Примеры запросов к API:
- Получение всех элементов QA: 
http://localhost:8000/api/qaitems/


# Разработчики
| Имя                  | Роль           | Контакт               |
|----------------------|----------------|-----------------------|
| Константин Балцат    | Data Analyse | [t.me/baltsat](https://t.me/baltsat)       |
| ---                  | ---            | ---                   |
| Александр Серов      | Machine Learning | [t.me/thegoldian](https://t.me/thegoldian) |
| ---                  | ---            | ---                   |
| Артем Тарасов        | Full stack | [t.me/tarasovxx](https://t.me/tarasovxx)   |
| ---                  | ---            | ---                   |
| Ванданов Сергей      | Machine Learning | [t.me/rapid76](https://t.me/@rapid76)      |
| ---                  | ---            | ---                   |
| Даниил Галимов       | Data Analyse | [t.me/Dan_Gan](https://t.me/Dan_Gan)  |
| ---                  | ---            | ---                   |




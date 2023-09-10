
![logo](https://github.com/Baltsat/users-rosatom/assets/42536677/8b3b5aa5-b56b-4c83-8681-6ca52d15f972)


# Улучшение представлений результатов в сервисе «Мой голос» от команды Users

Мы предлагаем решение для точного объединения ответов пользователей по смыслу в сервисе "Мой Голос" с помощью передового подхода к обработке текста Bert и визуализации результатов через веб-интерфейс на основе Streamlit. Решение выделяется тем, что устойчиво к ошибкам и опечаткам пользователей, а также учитывает даже латентные смысловые средства: эмоджи и пунктуацию.

Технические особенности:
Использование мультиязычного BERT для создания векторных представлений текста
Многоуровневая кластеризация: UMAP -> HDBSCAN -> CountVectorizer -> TF-IDF
Эмоциональная окраска текста с помощью XLM Roberta, обученного на комментариях пользователей- Интерфейс на основе Streamlit



# Установка
- `git clone https://github.com/Baltsat/users-rosatom.git`

# Запуск
```bash
streamlit run main.py
```

# Используемое решение

* Для исходных данных проводится предобработка ответов: удаление пунктуации, фильтрация ненонрмативной лексики, 
* В исходный датасет добавлены агрегированные статистики по субъектам РФ. Также, он обогащен дополнительными значениями из внешних источников:

  * экономические и демографические показатели по субъектам РФ;
  * статистика использования населением инфокоммуникационных технологий;
  * информация о характеристиках доступных в регионе тарифов Ростелеком;
  * данные о курсах валют, фондовых рынках и ситуации с COVID-19.

* На обработанных данных обучены модели машинного обучения, в частности, AutoML и градиентный бустинг с последующим блендингом в единый алгоритм определения потенциальных клиентов.
* Для последующей оценки полученных предсказаний, разработанный пайплайн включает в себя модуль по выводу мета информации о потенциальных клиентах. Это в совокупности представляет собой систему поддержки принятия решений.

# Уникальность:

Наше уникальное решение объединяет передовой подход к обработке текста с помощью модели Bert, визуализацию результатов через интерфейс Streamlit и способность обрабатывать особенности русского и английского языка, что обеспечивает точность и простоту использования в сервисе "Мой Голос".

# Стек используемых технологий:

`Python3`, `git`, `GitHub` - инструменты разработки

`HF Transformers`, `TweetNLP`, `BertTopic` - библиотеки глубокого обучения

`Scikit-Learn`, `UMAP` - фреймворки машинного обучения  

`Plotly`, `Streamlit` - инструменты визуализации  


# Сравнение моделей

В качестве устойчивого классификационного решения был выбран ансамбль из 5 моделей градиентного бустинга, с временем инференса 93.4 мс, так как он решает прогнозирует потенциальных клиентов с высоким (более 10% на отложенной выборке) результатом по предложенной метрике.

# Проводимые исследования

- `research/catboost.ipynb` - исследования с моделями градиентного бустинга
- `research/signal_eda.ipynb` и `research/spec_eda.ipynb` - анализ исходных данных 


# Разработчики
| Имя                  | Роль           | Контакт               |
|----------------------|----------------|-----------------------|
| Константин Балцат    | Data Analyse | [t.me/baltsat](https://t.me/baltsat)       |
| ---                  | ---            | ---                   |
| Александр Серов      | Machine Learning | [t.me/thegoldian](https://t.me/thegoldian) |
| ---                  | ---            | ---                   |
| Артем Тарасов        | Frontend | [t.me/tarasovxx](https://t.me/tarasovxx)   |
| ---                  | ---            | ---                   |
| Ванданов Сергей      | Machine Learning | [t.me/rapid76](https://t.me/@rapid76)      |
| ---                  | ---            | ---                   |
| Даниил Галимов       | Data Analyse | [t.me/Dan_Gan](https://t.me/Dan_Gan)  |
| ---                  | ---            | ---                   |

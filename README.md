[logo](https://github.com/Baltsat/users-rosatom/images/logo.png)


# Улучшение представлений результатов в сервисе «Мой голос» от команды Users

Реализован веб-сервис для семантической кластеризации результатов опросов в сервисе "Мой голос" с использованием технологий исскусственного интеллекта, визуализации результатов и представления выводов, основанных на данных.

# Установка
- `git clone https://github.com/mansasha21/sftb-rostelecom.git`

# Запуск
```bash
python train.py && python eval.py
```
// TODO: docker + streamlit

# Используемое решение

* Для исходных данных проводится обработка пропущенных значений, основанная на статистических распределениях и очистка данных от дубликатов. 
* В исходный датасет добавлены агрегированные статистики по субъектам РФ. Также, он обогащен дополнительными значениями из внешних источников:

  * экономические и демографические показатели по субъектам РФ;
  * статистика использования населением инфокоммуникационных технологий;
  * информация о характеристиках доступных в регионе тарифов Ростелеком;
  * данные о курсах валют, фондовых рынках и ситуации с COVID-19.

* На обработанных данных обучены модели машинного обучения, в частности, AutoML и градиентный бустинг с последующим блендингом в единый алгоритм определения потенциальных клиентов.
* Для последующей оценки полученных предсказаний, разработанный пайплайн включает в себя модуль по выводу мета информации о потенциальных клиентах. Это в совокупности представляет собой систему поддержки принятия решений.

# Уникальность:

Разработанный пайплайн является уникальным решением на рынке за счет использования для обучения обогащенного набор данных, разработанного алгоритма предобработки исходных данных, а также имплементированного механизма блендинга полученных моделей.

# Стек используемых технологий:

`Python3`, `git`, `GitHub` - инструменты разработки  
`LightGBM`, `LAMA`, `CatBoost`, `Scikit-Learn`, `SciPy` - фреймворки машинного обучения  
`Plotly`, `Seaborn` - инструменты визуализации  

# Сравнение моделей

В качестве устойчивого классификационного решения был выбран ансамбль из 5 моделей градиентного бустинга, с временем инференса 93.4 мс, так как он решает прогнозирует потенциальных клиентов с высоким (более 10% на отложенной выборке) результатом по предложенной метрике.

# Проводимые исследования

- `research/catboost.ipynb` - исследования с моделями градиентного бустинга
- `research/signal_eda.ipynb` и `research/spec_eda.ipynb` - анализ исходных данных 


# Разработчики
| Имя                  | Роль           | Контакт               |
|----------------------|----------------|-----------------------|
| Константин Балцат    | Data Scientist | [t.me/baltsat](https://t.me/baltsat)       |
| ---                  | ---            | ---                   |
| Александр Серов      | Data Scientist | [t.me/thegoldian](https://t.me/thegoldian) |
| ---                  | ---            | ---                   |
| Артем Тарасов        | Data Scientist | [t.me/tarasovxx](https://t.me/tarasovxx)   |
| ---                  | ---            | ---                   |
| Ванданов Сергей      | Data Scientist | [t.me/rapid76](https://t.me/@rapid76)      |
| ---                  | ---            | ---                   |
| Даниил Галимов       | Data Scientist | [t.me/Dan_Gan](https://t.me/Dan_Gan)  |
| ---                  | ---            | ---                   |

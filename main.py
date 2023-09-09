import streamlit as st
import plotly.express as px
import pandas as pd

from clustring_process import ClusteringAndProcessing
from pages_views.claster import ShowClasters

import json
import csv

st.markdown("<h1 style='text-align: center; background-color: #000045; color: #ece5f6'>Users Team</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; background-color: #000045; color: #ece5f6'>Улучшение представлений результатов в сервисе \"Мой голос\"</h4>", unsafe_allow_html=True)

# Создаем боковую панель
with st.sidebar:
    st.header("Ввод данных")

    # Вариант 1: Ввод данных вручную
    user_input = st.text_area("Введите JSON данные:")

    # Вариант 2: Загрузка файла JSON
    uploaded_file = st.file_uploader("Загрузите файл JSON", type=["json"])

    # Доп необязательное поле для ввода количествова кластеров, которые выводятся на экран
    default_clusters = 5
    cluster_count = st.number_input(
        "Количество кластеров (по умолчанию 5):",
        value=default_clusters,
        min_value=1,  # Минимальное значение
        step=1,  # Шаг изменения (только целые числа)
    )

show_data = False

# Обработка введенных данных или загруженного файла
if user_input:
    st.write("Вы ввели следующие данные:", user_input)
    show_data = True  # Устанавливаем флаг для отображения данных

if uploaded_file:
    st.write("Вы загрузили файл JSON:", uploaded_file)
    show_data = True  # Устанавливаем флаг для отображения данных

# Отображаем элементы только если флаг show_data установлен в True
if show_data:
    show_info_instance = ShowClasters()

    if user_input:
        show_info_instance.set_user_input(user_input)
        try:
            json_data = json.loads(user_input)
        except json.JSONDecodeError:
            # Обработка ошибки, если user_input не является валидной JSON строкой
            pass
    elif uploaded_file:
        show_info_instance.set_uploaded_file(uploaded_file)
        try:
            with open(uploaded_file, 'r') as file:
                json_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Обработка ошибки, если файл не найден или не содержит валидный JSON
            pass
    clustering = ClusteringAndProcessing()
    csv_data = clustering.getProcessedFileInCSV(json_data, cluster_count)
    # пусть мы сейчас выплюнули tema.csv
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    show_info_instance._display_content(df, cluster_count)


if show_data:
    data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
    st.write(fig)
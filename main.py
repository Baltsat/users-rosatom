import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from wordcloud import WordCloud

#from bertopic import BERTopic
#from sklearn.datasets import fetch_20newsgroups

from clustring_process import ClusteringAndProcessing
from pages_views.claster import ShowClasters

import json
import csv

st.markdown("<h1 style='text-align: center; background-color: #000045; color: #ece5f6'>Users Team</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; background-color: #000045; color: #ece5f6'>Улучшение представлений результатов в сервисе \"Мой голос\"</h4>", unsafe_allow_html=True)

# Создаем боковую панель
with st.sidebar:
    st.header("Ввод данных")
    i = 1
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
    implementation_choice = st.selectbox("Выберите реализацию:", ["default", "Список кластеров", "Sunburst", "Wordcloud", "Гистограмма"])


show_data = False

if (implementation_choice == "default" and (not user_input and not uploaded_file)):
    pass
else:
    if (implementation_choice == "default"):
        st.write("Данные обработаны, переключите режим на боковой панели")
    # Обработка введенных данных или загруженного файла
    if user_input:
        #st.write("Вы ввели следующие данные:", user_input)
        show_data = True  # Устанавливаем флаг для отображения данных

    if uploaded_file:
        #st.write("Вы загрузили файл JSON:", uploaded_file)
        show_data = True  # Устанавливаем флаг для отображения данных=

    json_data = None

    if show_data:
        show_info_instance = ShowClasters()

    if user_input:
        try:
            json_data = json.loads(user_input)
        except json.JSONDecodeError:
            # Обработка ошибки, если user_input не является валидной JSON строкой
            pass
    elif uploaded_file:
        # Получите байтовые данные из объекта UploadedFile
        uploaded_file_bytes = uploaded_file.read()

        # Преобразуйте байты в строку
        uploaded_file_text = uploaded_file_bytes.decode('utf-8')

        st.write("Вы загрузили файл JSON:", uploaded_file.name)
        # st.code(uploaded_file_text, language='json')  # Отобразить содержимое файла в блоке кода
        try:
            # Преобразуйте строку JSON в словарь
            json_data = json.loads(uploaded_file_text)

            # В данном месте json_data является словарем и может быть индексирован
            # Например, json_data['answers']
        except json.JSONDecodeError:
            st.write("Произошла ошибка при разборе JSON данных из файла.")

        show_data = True  # Устанавливаем флаг для отображения данных

    @st.cache_data
    def clusterRelese():
        clustering = ClusteringAndProcessing()
        csv_data = clustering.get_processed_file_in_CSV(json_data, cluster_count)
        # Здесь clustering - csv
        df = csv_data
        return df

    if (json_data):
        df = clusterRelese()

    if implementation_choice == "Список кластеров":
        # Отображаем список кластеров
        show_info_instance._display_content(df, cluster_count)

    elif implementation_choice == "Sunburst":


        cluster_counts = df['cluster_id'].value_counts().to_dict()

        labels = []
        values = []
        for cluster_id, freq in cluster_counts.items():
            labels.append(str(cluster_id))
            values.append(freq)

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                     insidetextorientation='radial'
                                     )])
        st.write(fig)
        st.write(df['question'][0])
    elif implementation_choice == "Wordcloud":
        text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
    elif implementation_choice == "Гистограмма":
        x = []
        y = []
        colors = {'neutrals': 'lightyellow', 'positives': 'lightgreen', 'negatives': 'lightcoral'}

        sent_counts = df['sentiment'].value_counts().to_dict()
        print(sent_counts)
        for sent, freq in sent_counts.items():
            x.append(sent)
            y.append(freq)
        color_list = [colors[sent] for sent in x]
        fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=color_list))])
        fig.update_layout(title="Частота значений 'sentiment'")

        st.write(fig)
        st.write(df['question'][0])


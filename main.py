import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image

#from bertopic import BERTopic
#from sklearn.datasets import fetch_20newsgroups

from clustring_process import ClusteringAndProcessing
from pages_views.claster import ShowClasters

import json
import csv

from pages_views.first_page import MainPage

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
    implementation_choice = st.selectbox("Выберите реализацию:", ["default", "Список кластеров", "Sunburst", "Wordcloud", "Гистограмма", "BubbleCluster"])


show_data = False

if (implementation_choice == "default" and (not user_input and not uploaded_file)):
    first_page_render = MainPage()
    first_page_render.visualizeMainPage()
else:
    df = None
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


    show_info_instance = None
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
    def clusterRelese(json_data):
        clustering = ClusteringAndProcessing()
        csv_data, chrts = clustering.get_processed_file_in_CSV(json_data, cluster_count)
        # Здесь clustering - csv
        df = csv_data
        return df, chrts


    chrts = None
    if json_data:
        df, chrts = clusterRelese(json_data)

    if df is not None:

        if implementation_choice == "Список кластеров":
            # Отображаем список кластеров
            show_info_instance._display_content(df, cluster_count)

        elif df is not None and implementation_choice == "Sunburst":

            cluster_counts = df['topic_name'].value_counts().to_dict()

            labels = []
            values = []
            for cluster_id, freq in cluster_counts.items():
                print(len(df['question'][0]))
                labels.append(cluster_id[len(df['question'][0]):])
                values.append(freq)

            fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                         insidetextorientation='radial'
                                         )])
            st.write(fig)
            st.write(df['question'][0])
        elif df is not None and implementation_choice == "Wordcloud":
            words_inf = df['topic_name'].value_counts().to_dict()

            words = [word[len(df['question'][0]):] for word in list(words_inf.keys())]

            print(words)
            text = ', '.join(words)

            # Create and generate a word cloud image:
            wordcloud = WordCloud(relative_scaling=0.5).generate(text)

            # Display the generated image:
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        elif df is not None and implementation_choice == "Гистограмма":
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
        elif implementation_choice == "BubbleCluster":
            tab1, tab2 = st.tabs(["Кластеризация в 2д пространстве", "Другой тип кластеризации"])

            with tab1:
                # Use the Streamlit theme.
                # This is the default. So you can also omit the theme argument.
                st.altair_chart(chrts.interactive(), theme="streamlit", use_container_width=True)
            with tab2:
                # Use the native Altair theme.
                st.altair_chart(chrts.interactive(), theme=None, use_container_width=True)
